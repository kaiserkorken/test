import importlib.util
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

try:
    # Add location to path and import "grid_generator"
    sys.path.insert(0, '../external/lkm-navier-stokes-with-fenics/gmsh-collection/')
    import generate_xdmf_mesh
except ModuleNotFoundError:
    raise RuntimeError("Please execute me from the root of the project being 'KontiSim2022_Fussbodenheizung'")


def main(args):
    geo_file = args[1]
    print(f"Generating xdmf files from {geo_file}")
    generate_xdmf_mesh.generate_xdmf_mesh(geo_file)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
