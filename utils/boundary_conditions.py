import dolfin as dlfn


# Sub domain for Periodic boundary condition
class PeriodicBoundary(dlfn.SubDomain):
    """
    Class for the injection of a periodic boundary 'constrained_domain' into the FunctionSpace.
    Modified a bit according the change proposed here: https://groups.google.com/g/fenics-support/c/eINQurdojTo/m/LI4OH0dsAgAJ
    """
    lh = 1.

    # Left boundary is "target domain" G
    def inside(self, x, on_boundary):
        # Change proposed here: https://groups.google.com/g/fenics-support/c/eINQurdojTo?pli=1
        return on_boundary and not (dlfn.near(x[0], self.lh))

    # Map right boundary (H) to left boundary (G)
    def map(self, x, y):
        y[0] = 0.
        y[1] = x[1]
        # The third component here was somehow required, we should ask Sebastian if he knows why we have to treat the mesh like a 3D mesh
        #y[2] = 0.


# Sub domain for Dirichlet boundary condition
class DirichletBoundary(dlfn.SubDomain):
    def inside(self, x, on_boundary):
        return bool((x[1] < dlfn.DOLFIN_EPS or x[1] > (1.0 - dlfn.DOLFIN_EPS)) and on_boundary)
