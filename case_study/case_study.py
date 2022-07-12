# !/usr/bin/env python3
# -*- coding: utf-8 -*-

# General imports
import os.path
import sys
from typing import Dict, Optional, List
import numpy as np
import dolfin as dlfn
from collections import namedtuple
import matplotlib.pyplot as plt


dlfn.set_log_level(50)

# Insert project root level to path in order to be able to load the modules. Might want to do a refactoring later
sys.path.insert(0, "..")

from utils import generate_grid, boundary_conditions, convergence_test

GEO_FILE = "meshes/coarse/FussbodenheizungSegmentNass.geo"


THERMAL_CONDUCTIVITIES = {
    "copper": dlfn.Constant(384.0),
    "aluminum": dlfn.Constant(220.0),  # https://www.schweizer-fn.de/stoff/wleit_metall/wleit_metall.php
    "screed": dlfn.Constant(1.4),
    "concrete": dlfn.Constant(2.1),
    "wood": dlfn.Constant(0.2),  # Eiche: https://www.schweizer-fn.de/stoff/wleit_isolierung/wleit_isolierung.php
    "polystyrene": dlfn.Constant(
        0.032
    ),  # Styropor: https://www.energieheld.de/daemmung/daemmstoffe/styropor-eps#eigenschaften
    "pur_alukaschiert": dlfn.Constant(
        0.023
    ),  # PUR/PIR Platten Alukaschiert: https://www.baudiscount-paderborn.de/PUR-/-PIR-Daemmung-WLG-023-alukaschiert
    "cork": dlfn.Constant(0.05),  # Kork: https://www.energieheld.de/daemmung/daemmstoffe/kork
    "tile": dlfn.Constant(1.0),  # Fliesen: https://www.schweizer-fn.de/stoff/wleit_isolierung/wleit_isolierung.php
    "air": dlfn.Constant(0.0262),  # https://de.wikipedia.org/wiki/Wärmeleitfähigkeit
    "EPS": dlfn.Constant(0.04),  # Expandiertes Polystyrol https://de.wikipedia.org/wiki/Wärmeleitfähigkeit
}


class Material:
    def __init__(self, material_name):
        self.material = material_name
        self.thermal_conductivity = THERMAL_CONDUCTIVITIES[material_name]


SUBDOMAINS = {
    "Hot Inlet": Material("copper"),
    "Cold Outlet": Material("copper"),
    "Screed": Material("screed"),
    "Underfloor": Material("concrete"),
    "Insulation Heat": Material("pur_alukaschiert"),
    "Insulation Impact Noise": Material("cork"),
    "Floorboarding": Material("tile"),
    "Piping": Material("copper"),
    "Carrier": Material("EPS"),
    "Profile Sheets": Material("aluminum"),
    "Thermal Conduction Sheet": Material("aluminum"),
    "Air Gap": Material("air"),
}


def tx(x):
    """
    Just a setter method for a constant temperature.
    :param x:
    :return:
    """
    if not isinstance(x, float):
        x = float(x)
    return dlfn.Constant(x)


# Define a mapping for the Dirichlet Boundaries: {"<BOUNDARY_NAME>": tx(<BOUNDARY_TEMPERATURE>), ...}
DIRICHLET_BOUNDARIES = {}  # We currently define no dirichlet boundaries


# Define a set of physical boundary conditions
# https://www.heizungsfinder.de/fussbodenheizung/bodenbelaege/waermedurchlasswiderstand
NCC_BOUNDARY = namedtuple("NCC_boundary", ["external_temperature", "heat_transfer_coefficient"])
NCC_BOUNDARIES = {
    "Coverfloor": NCC_BOUNDARY(external_temperature=22.0, heat_transfer_coefficient=10.8),
    "Hot Inlet": NCC_BOUNDARY(external_temperature=55.0, heat_transfer_coefficient=3000.0),
    "Cold Outlet": NCC_BOUNDARY(external_temperature=50.0, heat_transfer_coefficient=3000.0),
}

# Define neumann boundaries
NEUMANN_BOUNDARY = namedtuple("NEUMANN_boundary", ["delta_q"])
NEUMANN_BOUNDARIES = {"Underfloor": NEUMANN_BOUNDARY(delta_q=0.0)}


POINT_COORDINATES = np.array(
    [
        [0, 0],
        [300, 0],
        [0, 87],
        [300, 87],
        [79.5, 39.5],
        [81, 39.5],
        [229.5, 39.5],
        [231, 39.5],
        [300, 62],
        [300, 32],
        [300, 30],
        [0, 62],
        [0, 32],
        [0, 30],
    ]
)


class Mesh:
    def __init__(self, geo_file=GEO_FILE):
        """
        Mesh class that stores:
            - mesh: dolfin.Mesh
            - facet_markers: dolfin.cpp.mesh.MeshFunctionSizet
            - facet_marker_map: Dict[FACET_NAME <-> FACET_ID]
            - cell_markers: dolfin.cpp.mesh.MeshFunctionSizet
            - cell_marker_map: Dict[SUBDOMAIN_NAME <-> SUBDOMAIN_ID]
            - w: maximum width of the domain
            - h: maximum height of the domain
            - dA: recomputed surface integral of the domain
            - dV: recomputed volume integral of the domain
            - n: dolfin.FacetNormal
            - space_dim: geometrical dimension of the mesh
        :param geo_file:
        """
        # Load the mesh and get the extracted facet_markers and cell_markers
        self.mesh, self.facet_markers, self.facet_marker_map, self.cell_markers, self.cell_markers_map = self.load_mesh(
            geo_file
        )

        # Compute the largest width and height of the domain
        self.width, self.height = self.get_domain_sizes()

        self.dA = dlfn.Measure("ds", domain=self.mesh, subdomain_data=self.facet_markers)
        self.dV = dlfn.Measure("dx", domain=self.mesh, subdomain_data=self.cell_markers)
        self.n = dlfn.FacetNormal(self.mesh)
        self.space_dim = self.mesh.geometry().dim()

    @staticmethod
    def load_mesh(geo_file):
        """
        Use the grid_generator from the LKM-codebase in order to read the xdmf files
        :param geo_file:
        :return: 5-tuple containing the mesh and the associated MeshFunctions for the facet_markers and cell_markers
        """
        return_values = generate_grid.get_mesh(geo_file)
        if len(return_values) == 3:
            return return_values + (None, None)
        elif len(return_values) == 5:
            return return_values

    def get_domain_sizes(self):
        """
        Compute the maximum dimensions of the domain
        :return:
        """
        max_coords = self.mesh.coordinates().max(axis=0)
        min_coords = self.mesh.coordinates().min(axis=0)
        w = max_coords[0] - min_coords[0]  # Index 0 for x coords being in the zeroth index
        h = max_coords[1] - min_coords[1]  # Index 1 for y coords being in the first index
        return w, h


def get_dirichlet(mesh: Mesh, w_h, facet_name, value):
    """
    Creates the dolfin.DirichletBC associated to the facet_name and assigns the given value
    :param mesh: dolfin.Mesh
    :param w_h: dolfin.FunctionSpace
    :param facet_name: string
    :param value: dolfin.Constant
    :return: dolfin.DirichletBC
    """
    if not value:
        raise ValueError("Missing Dirichlet BC value for " + facet_name)
    facet_id = mesh.facet_marker_map[facet_name]
    return dlfn.DirichletBC(w_h, value, mesh.facet_markers, facet_id)


class Solver:
    def __init__(self, mesh: Mesh, function_space: dlfn.FunctionSpace, dirichlet_boundaries: Dict):
        """
        Initialize a solver class; the final solution will be stored internally as 'w'
        :param mesh: An instance of the Mesh class
        :param function_space: The function space Vh in which the solution should be found
        :param dirichlet_boundaries: A dict containing the dirichlet facets and corresponding values
        """
        # Store the mesh instance for later access to the metrics
        self.mesh = mesh
        # Store the function space TODO: See if this remains necessary after fixing 'assemble_rhs'
        self.function_space = function_space
        # Create test and trial space
        self.u, self.v = dlfn.TrialFunction(function_space), dlfn.TestFunction(function_space)
        # Create solution function
        self.w = dlfn.Function(function_space)
        # Create a list of dirichlet boundary conditions
        self.dirichlet_bcs = [
            get_dirichlet(mesh, function_space, facet_name, value) for facet_name, value in dirichlet_boundaries.items()
        ]
        self.solution_gradient = None

    def newtons_cooling_condition(self, value: NCC_BOUNDARY):
        """
        Setter method for the physical boundary conditions according to the Newtons Cooling Theorem describing the
        mostly convective heat transfer at boundaries between solid and gas/liquid. The parameter alpha has a ton of
        dependencies and is most easily determined empirically or otherwise from EN ISO 6946.
        :param value: Name of the boundary for which the condition is going to be applied
        :type value: NCC_BOUNDARY
        :return:
        """
        return dlfn.Constant(value.heat_transfer_coefficient) * (self.u - dlfn.Constant(value.external_temperature))

    def sum_terms(
        self,
        source_term: str = "0",
        ncc_boundaries: Optional[Dict[str, NCC_BOUNDARY]] = None,
        neumann_boundaries: Optional[Dict[str, NEUMANN_BOUNDARY]] = None,
    ):
        """
        Build the sum of all terms (lhs and rhs) for later splitting up by dolfin itself.

        Construct a list of:
            - The source term
            - The Newton Cooling Condition Boundary terms
            - The Subdomain terms
        and run numpy.sum. For later addition of additional boundary condition types, add an equivalent block in here
        with a corresponding setter method.

        :param source_term:
        :param ncc_boundaries:
        :param neumann_boundaries:
        :return:
        """
        f = list()
        f.append(
            dlfn.Expression(cpp_code=source_term, element=self.function_space.ufl_element()) * self.v * self.mesh.dV
        )

        if ncc_boundaries:
            for boundary, value in ncc_boundaries.items():
                boundary_id = self.mesh.facet_marker_map[boundary]
                g = self.newtons_cooling_condition(value)
                f.append((g * self.v * self.mesh.dA(subdomain_id=boundary_id)))

        if neumann_boundaries:
            for boundary, value in neumann_boundaries.items():
                boundary_id = self.mesh.facet_marker_map[boundary]
                h = dlfn.Constant(value.delta_q)
                f.append(h * self.v * self.mesh.dA(subdomain_id=boundary_id))

        for subdomain_name, subdomain_id in self.mesh.cell_markers_map.items():
            cv = SUBDOMAINS[subdomain_name].thermal_conductivity
            f.append(cv * dlfn.inner(dlfn.grad(self.u), dlfn.grad(self.v)) * self.mesh.dV(subdomain_id=subdomain_id))

        return np.sum(f)

    def solve(
        self,
        ncc_boundaries: Optional[Dict[str, NCC_BOUNDARY]] = None,
        neumann_boundaries: Optional[Dict[str, NEUMANN_BOUNDARY]] = None,
    ):
        """
        Method that actually computes the solution for the problem
        :return:
        """

        f = self.sum_terms(ncc_boundaries=ncc_boundaries, neumann_boundaries=neumann_boundaries)
        lhs, rhs = dlfn.lhs(f), dlfn.rhs(f)

        # Solve
        dlfn.solve(lhs == rhs, self.w, self.dirichlet_bcs)

        # Return solution for direct use
        return self.w

    def get_solution_gradient(self):
        self.solution_gradient = dlfn.grad(self.w)

    def compute_heat_conduction_field(self):

        if not self.solution_gradient:
            self.get_solution_gradient()

        vh = dlfn.VectorFunctionSpace(
            mesh=self.mesh.mesh, family="DG", degree=1, constrained_domain=boundary_conditions.PeriodicBoundary()
        )
        u, v = dlfn.TrialFunction(vh), dlfn.TestFunction(vh)
        w = dlfn.Function(vh)

        hcf = [dlfn.inner(u, v) * self.mesh.dV]

        for subdomain_name, subdomain_id in self.mesh.cell_markers_map.items():
            cv = SUBDOMAINS[subdomain_name].thermal_conductivity
            hcf.append(cv * dlfn.inner(self.solution_gradient, v) * self.mesh.dV(subdomain_id=subdomain_id))
        hcf = np.sum(hcf)

        lhs, rhs = dlfn.lhs(hcf), dlfn.rhs(hcf)

        solver = dlfn.LocalSolver(lhs, rhs)
        solver.factorize()
        solver.solve_local_rhs(w)

        return w

    def save_solution(self, filename="temperature_field.pvd"):
        """
        Method to write the resulting temperature field to a file.
        :return:
        """
        self.w.rename("T", "Temperature Field")
        dlfn.File(filename) << self.w

    def save_grad(self, filename="temperature_gradient.pvd"):
        """
        Compute the gradient field of the solution and write to file
        :param filename:
        :return:
        """
        if not self.solution_gradient:
            self.get_solution_gradient()
        solution_gradient = dlfn.project(self.solution_gradient)
        solution_gradient.rename("grad(T)", "Temperature Gradient")
        dlfn.File(filename) << solution_gradient

    def save_heat_conduction(self, filename="heat_conduction.pvd"):
        """
        Computes the heat conduction vector q and saves it to a file, it might make sense to reuse the result from the
        calculation of the temperature gradient (before projecting).
        :param filename:
        :return:
        """
        heat_conduction_field = self.compute_heat_conduction_field()
        heat_conduction_field.rename("q", "Heat Conduction")
        dlfn.File(filename) << heat_conduction_field


def solve_routine(mesh_file, with_additionals=False):
    # Instantiate the custom Mesh class (Load mesh, facet_markers and cell_markers and compute some required metrics)
    mesh = Mesh(mesh_file)
    # Set the domain specific scale (width)
    boundary_conditions.PeriodicBoundary.lh = mesh.width
    # Create a function space for test/trial/solution function
    Vh = dlfn.FunctionSpace(mesh.mesh, "CG", 2, constrained_domain=boundary_conditions.PeriodicBoundary())
    # Instantiate the custom solver class ()
    solver = Solver(mesh, Vh, DIRICHLET_BOUNDARIES)
    # Solve the problem
    print("SOLVE PROBLEM")
    solver.solve(ncc_boundaries=NCC_BOUNDARIES, neumann_boundaries=NEUMANN_BOUNDARIES)
    # Save the solution
    if with_additionals:
        print("SAVE SOLUTION")
        solver.save_solution()
        # Compute and save the gradient of the temperature field for a better understanding of the evolution
        print("COMPUTE AND SAVE GRADIENT")
        solver.save_grad()
        print("COMPUTE AND SAVE HEAT CONDUCTION FIELD")
        solver.save_heat_conduction()
    return solver.w, Vh, mesh


def main(args):
    mesh_refinements = [
        "coarse",
        "coarse_medium",
        "medium",
        "medium_fine",
        "fine",
        "fine-1",
        "fine-2",
        "fine-3",
        "fine-4",
        "fine-5",
        "fine-6",
        "fine-7",
    ]

    geometry_name_wet = "FussbodenheizungSegmentNass.geo"
    geometry_name_dry = "FussbodenheizungSegmentTrocken.geo"
    run_convergence_test = True
    run_single = False

    if run_convergence_test:
        convergence = convergence_test.ConvergenceTest(
            solver_function=solve_routine,
            geo_name=geometry_name_wet,
            mesh_refinements=mesh_refinements,
            convergence_measures=["global", "facet_integral", "local"],
            out_dir="convergence_tests",
            points_coordinates=POINT_COORDINATES,
        )
        convergence.run_test()
        convergence.save_plots()
        convergence = convergence_test.ConvergenceTest(
            solver_function=solve_routine,
            geo_name=geometry_name_dry,
            mesh_refinements=mesh_refinements,
            convergence_measures=["global", "facet_integral", "local"],
            out_dir="convergence_tests",
            points_coordinates=POINT_COORDINATES,
        )
        convergence.run_test()
        convergence.save_plots()

    if run_single:
        solve_routine("meshes/fine-3/FussbodenheizungSegmentNass.geo", with_additionals=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
