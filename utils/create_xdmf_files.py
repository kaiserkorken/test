import importlib.util
import os.path
import shutil


class EnvironmentException(BaseException):
    pass


if not shutil.which("gmsh"):
    raise EnvironmentException(
        "The runtime environment does not have gmsh installed. Don't exeucte this script inside of the Docker Container.")
if not importlib.util.find_spec("meshio"):
    raise EnvironmentException("Please install meshio (with pip)")

if not importlib.util.find_spec("h5py"):
    raise EnvironmentException("Please install h5py (with pip)")


import sys

# Choose the xdmf generator to use
XDMF_GENERATOR_OPTIONS = {
    1: './external/lkm-navier-stokes-with-fenics/source/',
    2: './external/lkm-navier-stokes-with-fenics/gmsh-collection/python/'
}
SELECTION = 1

try:
    # Add location to path and import "grid_generator"
    sys.path.insert(0, XDMF_GENERATOR_OPTIONS[SELECTION])

    if SELECTION == 1:
        import grid_tools as generate_xdmf_mesh
    elif SELECTION == 2:
        import generate_xdmf_mesh

except ModuleNotFoundError:
    raise RuntimeError("Please execute me from the root of the project being 'KontiSim2022_Fussbodenheizung'")


def main(args):
    geo_file = args[1]
    print(f"Generating xdmf files from {geo_file}")
    assert os.path.exists(geo_file), f"The file {geo_file} does not exist"
    generate_xdmf_mesh.generate_xdmf_mesh(geo_file)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
