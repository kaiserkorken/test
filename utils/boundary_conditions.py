import dolfin as dlfn


# Sub domain for Periodic boundary condition
class PeriodicBoundary(dlfn.SubDomain):

    def __init__(self, domain_width):
        self.domain_width = domain_width

    # Left boundary is "target domain" G
    def inside(self, x, on_boundary):
        return bool(x[0] < dlfn.DOLFIN_EPS and x[0] > -dlfn.DOLFIN_EPS and on_boundary)

    # Map right boundary (H) to left boundary (G)
    def map(self, x, y):
        y[0] = x[0] - self.domain_width
        y[1] = x[1]


# Sub domain for Dirichlet boundary condition
class DirichletBoundary(dlfn.SubDomain):
    def inside(self, x, on_boundary):
        return bool((x[1] < dlfn.DOLFIN_EPS or x[1] > (1.0 - dlfn.DOLFIN_EPS)) and on_boundary)
