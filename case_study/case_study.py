# General imports
import os
import sys
import dolfin as dlfn

# Insert project root level to path in order to be able to load the modules. Might want to do a refactoring later
sys.path.insert(0, '..')

from utils import generate_grid, boundary_conditions

GEO_FILE = "FussbodenheizungSegmentNass.geo"


def main(args):
    mesh, facet_markers, facet_marker_map = generate_grid.get_mesh(GEO_FILE)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
