#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import meshio
from os import path
import subprocess


__all__ = ["generate_xdmf_mesh"]


def _create_meshio_mesh(mesh, cell_type, prune_z=False):
    """Create a meshio mesh object from a meshio mesh where only cells of
    `cell_type` are taken into account."""
    # input check
    assert isinstance(mesh, meshio.Mesh)
    assert isinstance(cell_type, str)
    assert cell_type in ("line", "triangle", "tetra")
    assert isinstance(prune_z, bool)
    # extract cells
    cells = mesh.get_cells_type(cell_type)
    # extract physical regions
    assert "gmsh:physical" in mesh.cell_data_dict
    cell_data = mesh.get_cell_data("gmsh:physical", cell_type)
    # specify data name
    if "triangle" in mesh.cells_dict and "tetra" not in mesh.cells_dict:
        if cell_type == "triangle":
            data_name = "cell_markers"
        elif cell_type == "line":
            data_name = "facet_markers"
        else:
            raise RuntimeError()
    elif "triangle" in mesh.cells_dict and "tetra" in mesh.cells_dict:
        if cell_type == "tetra":
            data_name = "cell_markers"
        elif cell_type == "triangle":
            data_name = "facet_markers"
        else:
            raise RuntimeError()
    else:
        raise RuntimeError()
    # create mesh object
    out_mesh = meshio.Mesh(points=mesh.points, cells={cell_type: cells},
                           cell_data={data_name: [cell_data]})
    # remove z-component
    if prune_z:
        out_mesh.prune_z_0()
    return out_mesh


def generate_xdmf_mesh(geo_filename):
    """Script generating two xdmf-files from a geo-file. The two xdmf-files
    contain the mesh and the associated facet markers. Facet markers refer to
    the markers on entities of codimension one.

    The mesh is generated by calling gmsh to a generate an msh-file and the two
    xmdf-files are generated using the meshio package.
    """
    # input check
    assert isinstance(geo_filename, str)
    assert path.exists(geo_filename)
    filename = geo_filename[:geo_filename.index(".geo")]
    # generate msh file
    msh_filename = geo_filename.replace(".geo", ".msh")
    assert msh_filename.endswith(".msh")
    subprocess.run(["gmsh", "-3", geo_filename], check=True)
    # read msh file
    mesh = meshio.read(msh_filename)
    # determine dimension
    if "triangle" in mesh.cells_dict and "tetra" not in mesh.cells_dict:
        assert "line" in mesh.cell_data_dict["gmsh:physical"]
        dim = 2
    elif "triangle" in mesh.cells_dict and "tetra" in mesh.cells_dict:
        assert "triangle" in mesh.cell_data_dict["gmsh:physical"]
        dim = 3
    else:
        raise RuntimeError()
    # specify cell types
    if dim == 2:
        facet_type = "line"
        cell_type = "triangle"
        # prune_z = True  # Had to switch this because appearently I generated my mesh/geo without a 3D component and the script is incompatible
        prune_z = False
    elif dim == 3:
        facet_type = "triangle"
        cell_type = "tetra"
        prune_z = False
    # extract facet mesh (codimension one)
    facet_mesh = _create_meshio_mesh(mesh, facet_type, prune_z=prune_z)
    xdmf_facet_marker_filename = filename + "_facet_markers.xdmf"
    meshio.write(xdmf_facet_marker_filename, facet_mesh, data_format="XML")
    # extract facet mesh (codimension one)
    cell_mesh = _create_meshio_mesh(mesh, cell_type, prune_z=prune_z)
    xdmf_filename = geo_filename.replace(".geo", ".xdmf")
    meshio.write(xdmf_filename, cell_mesh, data_format="XML")
    # delete msh file
    subprocess.run(["rm", "-rf", msh_filename], check=True)
