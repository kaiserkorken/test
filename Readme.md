# Projekt Fußbodenheizung

**Contributors**:
- Enrico Stauss
- Christoph Scherer
- Peter Constien

**Codebase**:
- Github Repository: https://github.com/enrlc0/KontiSim2022_Fussbodenheizung
- Includes (as [git subtree](https://www.atlassian.com/git/tutorials/git-subtree)): [LKM NavierStokes with Fenics](https://github.com/LKM-code-base/NavierStokes-with-Fenics/tree/main)

## Development Environment
As runtime environment, we use the [Fenics Docker Image](quay.io/fenicsproject/stable).

**Setup Suggestion**:
Using the Pycharm Professional IDE (free for Students), it is possible to connect to Docker (Preferences -> Build, Execution, Deployment) and then add the docker image as a python interpreter. Don't forget to specify "python3" as path to python executeable! Now, the python console will be mounted to the Docker Container and the script will automatically be executed inside of the container runtime.

## Geometry Details

## Materials and Coefficients

## Implementation

### Creating the Mesh
For the initial draft, gmsh was used to produce a `.geo` and a `.msh` file

### Creating the `.xdmf` Files
In order to use the `external/lkm-with-navier-stokes/source/grid_generator.py` provided by LKM inside the docker container, it is neccessary that the xdmf files exist already. The latter can be created with the `external/lkm-with-navier-stokes/gmsh-collection/generate_xdmf_mesh.py` with some tweaks:
- In a local virtual environment _(outside of the docker container)_, pip install `meshio` and `h5py`
- In the terminal _(with the venv activated)_, change to the directory `external/lkm-with-navier-stokes/gmsh-collection`
- Modify line 81: `prune_z = True`-> `prune_z = False` in order for the script to be compatible with the created `.geo` and `.msh` files
- Enter `python` and execute:
  ```
  import generate_xdmf_mesh
  generate_xdmf_mesh.generate_xdmf_mesh("../../../FussbodenheizungSegmentNass.geo")
  ```
  

1. Case Study (of  segment)
2. Final Implementation
