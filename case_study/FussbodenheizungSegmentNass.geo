// Gmsh project created on Fri Jun 10 21:17:37 2022
SetFactory("OpenCASCADE");
//+
Point(1) = {0, 1, 0, 1.0};
//+
Point(2) = {1, 1, 0, 1.0};
//+
Point(3) = {1, 0, 0, 1.0};
//+
Point(4) = {0, 0, 0, 1.0};
//+
Line(1) = {1, 2};
//+
Line(2) = {4, 3};
//+
Point(5) = {0, 0.2, 0, 1.0};
//+
Point(6) = {1, 0.2, 0, 1.0};
//+
Point(7) = {0, 0.25, 0, 1.0};
//+
Point(8) = {1, 0.25, 0, 1.0};
//+
Point(9) = {1, 0.85, 0, 1.0};
//+
Point(10) = {0, 0.85, 0, 1.0};
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
Circle(14) = {0.25, 0.5, 0, 0.1, 0, 2*Pi};
//+
Circle(15) = {0.75, 0.5, 0, 0.1, 0, 2*Pi};
//+
Physical Curve("Hot Inlet", 16) = {14};
//+
Physical Curve("Cold Outlet", 17) = {15};
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
Physical Surface("Infulation Impact Noise", 23) = {3};
//+
Physical Surface("Floorboarding", 24) = {4};
//+
Physical Surface("Insulation Heat", 25) = {2};