// Gmsh project created on Fri Jun 10 21:17:37 2022

// geometry parameters [mm]
OuterDiameter = 12;
TubeWallThickness = 1.5;
TubeSpacing = 150;
ScreedThickness = 30;
InsulationHeatThickness = 30;
InsulatonImpactnoiseThickness = 2;
FloorboardingThickness = 25;
// TBD: carrier_thickness = 4;
SegmentWidth = 2 * TubeSpacing;

hges = InsulationHeatThickness + InsulatonImpactnoiseThickness + ScreedThickness + FloorboardingThickness;

// define some shortcuts
w = SegmentWidth;
h1 = InsulationHeatThickness;
h2 = h1 + InsulatonImpactnoiseThickness;
h2p5 = h2 + ScreedThickness/4;
h3 = h2 + ScreedThickness;
R = OuterDiameter/2;
r = R - TubeWallThickness;


// characteristic size
lc = hges/3;

SetFactory("OpenCASCADE");
//+
Point(1) = {0, hges, 0, lc};
//+
Point(2) = {w, hges, 0, lc};
//+
Point(3) = {w, 0, 0, lc};
//+
Point(4) = {0, 0, 0, lc};
//+
Line(1) = {1, 2};
//+
Line(2) = {4, 3};
//+
Point(5) = {0, h1, 0, lc};
//+
Point(6) = {w, h1, 0, lc};
//+
Point(7) = {0, h2, 0, lc};
//+
Point(8) = {w, h2, 0, lc};
//+
Point(9) = {w, h3, 0, lc};
//+
Point(10) = {0, h3, 0, lc};
//+
Line(3) = {5, 6};
//+
Line(4) = {8, 7};
//+
Line(5) = {10, 9};
//+
Line(6) = {2, 9};
//+
Line(7) = {9, 8};
//+
Line(8) = {8, 6};
//+
Line(9) = {6, 3};
//+
Line(10) = {1, 10};
//+
Line(11) = {10, 7};
//+
Line(12) = {7, 5};
//+
Line(13) = {5, 4};
//+
Circle(14) = {w/4, h2p5, 0, R, 0, 2*Pi};
//+
Circle(15) = {3/4 * w, h2p5, 0, R, 0, 2*Pi};
//+
Circle(16) = {w/4, h2p5, 0, r, 0, 2*Pi};
//+
Circle(17) = {3/4 * w, h2p5, 0, r, 0, 2*Pi};
//+
Curve Loop(7) = {14};
//+
Curve Loop(8) = {16};
//+
Plane Surface(5) = {7, 8};
//+
Curve Loop(9) = {15};
//+
Curve Loop(10) = {17};
//+
Plane Surface(6) = {9, 10};
//+
Physical Curve("Hot Inlet", 16) = {16};
//+
Physical Curve("Cold Outlet", 17) = {17};
//+
Physical Curve("Underfloor", 18) = {2};
//+
Physical Curve("Coverfloor", 19) = {1};
//+
Physical Curve("Periodic Boundary Left", 20) = {13, 12, 11, 10};
//+
Physical Curve("Periodic Boundary Right", 21) = {9, 8, 7, 6};
//+
Curve Loop(1) = {11, -4, -7, -5};
//+
Curve Loop(2) = {14};
//+
Curve Loop(3) = {15};
//+
Plane Surface(1) = {1, 2, 3};
//+
Physical Surface("Screed", 22) = {1};
//+
Curve Loop(4) = {13, 2, -9, -3};
//+
Plane Surface(2) = {4};
//+
Curve Loop(5) = {3, -8, 4, 12};
//+
Plane Surface(3) = {5};
//+
Curve Loop(6) = {5, -6, -1, 10};
//+
Plane Surface(4) = {6};
//+
Physical Surface("Insulation Impact Noise", 23) = {3};
//+
Physical Surface("Floorboarding", 24) = {4};
//+
Physical Surface("Insulation Heat", 25) = {2};
//+
Physical Surface("Piping", 26) = {5, 6};
