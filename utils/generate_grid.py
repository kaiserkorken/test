import os
import sys

# Add location to path and import "grid_generator"
sys.path.insert(0, '../external/lkm-navier-stokes-with-fenics/source/')

import grid_generator


def get_mesh(geo_file):
    """
    returns: (mesh, facet_markers, facet_marker_map)
    """
    return grid_generator._read_external_mesh(geo_file)
