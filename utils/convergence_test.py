# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import matplotlib.pyplot as plt
from typing import Callable, Tuple, Optional, List
import numpy as np
import dolfin as dlfn
from dolfin.function.function import Function
from dolfin.function.functionspace import FunctionSpace
from dolfin.cpp.mesh import Mesh


class ConvergenceTest:
    def __init__(
        self,
        solver_function: Callable[[str], Tuple[Function, FunctionSpace, Mesh]],
        geo_name,
        mesh_refinements,
        convergence_measures: List[str],
        out_dir: Optional[str] = None,
        points_coordinates: Optional[np.ndarray] = None,
    ):
        # Save the input parameters
        self.solver_func = solver_function
        self.geo_name = geo_name
        self.mesh_refinements = mesh_refinements
        self.convergence_measures = convergence_measures
        self.out_dir = out_dir
        if points_coordinates is not None:
            self.points_coordinates = points_coordinates

        # A mapping of existing convergence measures
        self.measures = {
            "global": self.global_convergence,
            "local": self.local_convergence,
            "facet_integral": self.facet_integral_convergence,
            "domain_integral": self.domain_integral_convergence,
        }

        # Init variables for storage of results
        self.results = None
        self.max_cell_diameters = None

        # Variables for intermediate results of specific measures
        self.previous_facet_integral = None
        self.previous_points_values = None

    def run_test(self):
        print("RUNNING A CONVERGENCE TEST FOR THE GEOMETRY: " + self.geo_name)
        max_cell_diameter = np.zeros(len(self.mesh_refinements) - 1)
        difference = np.zeros(shape=(len(self.mesh_refinements) - 1, len(self.convergence_measures)))
        previous_solutions: Optional = None
        entry = 0
        for refinement in self.mesh_refinements:
            print("COMPUTING SOLUTION FOR THE REFINEMENT: " + refinement)
            geo_file = os.path.join("meshes", refinement, self.geo_name)
            solution, function_space, mesh = self.solver_func(geo_file)
            for i, measure in enumerate(self.convergence_measures):
                assert measure in self.measures, "The given convergence measure: " + measure + " is not implemented!"
                diff = self.measures[measure](solution, function_space, mesh, previous_solutions)
                if diff is not None:
                    difference[entry, i] = diff

            max_cell_diameter[entry] = mesh.mesh.hmax()
            if previous_solutions is not None:
                entry += 1

            previous_solutions = solution

        self.max_cell_diameters = max_cell_diameter
        self.results = difference

    def save_plots(self):
        if self.out_dir:
            self.out_dir = os.path.abspath(self.out_dir)
        else:
            self.out_dir = os.getcwd()
        print("SAVING PLOTS")
        ylabels = {
            "global": "errornorm(solution - LagrangeInterpolator(previous_solution))",
            "local": "L2_norm(solution(points) - previous_solution(points))",
            "facet_integral": "facet_integral(solution) - facet_integral(previous_solution)",
            "domain_integral": "domain_integral(solution) - domain_integral(previous_solution)",
        }
        for i, measure in enumerate(self.convergence_measures):
            filename = "convergence_test_" + measure + "_" + self.geo_name + ".pdf"
            filename = os.path.join(self.out_dir, filename)

            f = plt.figure(i+1)
            print(self.max_cell_diameters.shape, self.results.shape)
            print(self.max_cell_diameters, self.results)
            plt.plot(self.max_cell_diameters, self.results[:, i], linestyle="--", marker=".", c="g")
            plt.yscale("log")
            plt.xscale("log")
            plt.xlabel(r"Maximum Cell Size (hmax)")
            plt.ylabel(ylabels[measure])
            f.savefig(filename)
            plt.cla()

    def global_convergence(self, solution, function_space, mesh, previous_solution):
        print("COMPUTING GLOBAL CONVERGENCE MEASURE")
        fun = dlfn.Function(function_space)

        difference = None
        if previous_solution is not None:
            dlfn.LagrangeInterpolator.interpolate(fun, previous_solution)
            difference = dlfn.errornorm(fun, solution)

        return difference

    def local_convergence(self, solution, function_space, mesh, previous_solution):
        print("COMPUTING LOCAL CONVERGENCE MEASURE")
        assert self.points_coordinates is not None
        # evaluate coordinate values here
        values = np.array([solution(c) for c in self.points_coordinates])

        difference = None
        if previous_solution is not None:
            difference = np.linalg.norm((values - self.previous_points_values), ord=2)

        self.previous_points_values = values

        return difference

    def facet_integral_convergence(self, solution, function_space, mesh, previous_solution):
        print("COMPUTING FACET INTEGRAL CONVERGENCE MEASURE")
        integral = 0.0
        for facet in mesh.facet_marker_map.values():
            integral += dlfn.assemble(solution * mesh.dA(subdomain_id=facet))

        difference = None
        if previous_solution is not None:
            difference = np.abs(self.previous_facet_integral - integral)

        self.previous_facet_integral = integral

        # Return difference
        return difference

    def domain_integral_convergence(self, solution, function_space, mesh, previous_solution):
        raise NotImplementedError
