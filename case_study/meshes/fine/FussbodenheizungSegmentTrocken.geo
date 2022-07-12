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
ThermalConductionPlateThickness = 2;
WidthProfileSheet = TubeSpacing * 2/3;

hges = InsulationHeatThickness + InsulatonImpactnoiseThickness + ScreedThickness + FloorboardingThickness;

// define some shortcuts
w = SegmentWidth;
h1 = InsulationHeatThickness;
h2 = h1 + InsulatonImpactnoiseThickness;
h3 = h2 + ScreedThickness;
h4 = h3 + ThermalConductionPlateThickness;
R = OuterDiameter/2;
h3p5 = h3 - R;
r = R - TubeWallThickness;
l1 = ThermalConductionPlateThickness;
l2 = WidthProfileSheet/2;

// characteristic size
lc = hges/3;

SetFactory("OpenCASCADE");
// POINTS MARKING HORIZONTAL LEVELS
//+ 0. horizontal
Point(3) = {w, 0, 0, lc};
//+
Point(4) = {0, 0, 0, lc};
//+ 1. horizontal
Point(5) = {0, h1, 0, lc};
//+
Point(6) = {w, h1, 0, lc};
//+ 2. horizontal
Point(7) = {0, h2, 0, lc};
//+
Point(8) = {w, h2, 0, lc};
//+ 3. horizontal
Point(15) = {0, h3, 0, lc};
//+
Point(16) = {w, h3, 0, lc};
//+ 4. horizontal
Point(9) = {w, h4, 0, lc};
//+
Point(10) = {0, h4, 0, lc};
//+ 5. horizontal
Point(1) = {0, hges, 0, lc};
//+
Point(2) = {w, hges, 0, lc};
// POINTS MARKING THE LEFT PROFILE SHEET
//+
Point(17) = {w/4-R-l1, h3-l1, 0, lc};
//+
Point(18) = {w/4+R+l1, h3-l1, 0, lc};
//+
Point(23) = {w/4-R, h3, 0, lc};
//+
Point(24) = {w/4+R, h3, 0, lc};
//+
Point(25) = {w/4-R, h3p5, 0, lc};
//+
Point(26) = {w/4-R-l1, h3p5, 0, lc};
//+
Point(27) = {w/4+R+l1, h3p5, 0, lc};
//+
Point(28) = {w/4+R, h3p5, 0, lc};
//+
Point(33) = {w/4, h3p5, 0, lc};
//+
Point(38) = {w/4-l2/3, h3-l1, 0, lc};
//+
Point(39) = {w/4-l2/3, h3, 0, lc};
//+
Point(42) = {w/4-l2, h3-l1, 0, lc};
//+
Point(43) = {w/4-l2, h3, 0, lc};
//+
Point(40) = {w/4+l2/3, h3-l1, 0, lc};
//+
Point(41) = {w/4+l2/3, h3, 0, lc};
//+
Point(44) = {w/4+l2, h3-l1, 0, lc};
//+
Point(45) = {w/4+l2, h3, 0, lc};
// POINTS MARKING THE RIGHT PROFILE SHEET
//+
Point(46) = {w*3/4-R-l1, h3-l1, 0, lc};
//+
Point(47) = {w*3/4+R+l1, h3-l1, 0, lc};
//+
Point(48) = {w*3/4-R, h3, 0, lc};
//+
Point(49) = {w*3/4+R, h3, 0, lc};
//+
Point(50) = {w*3/4-R, h3p5, 0, lc};
//+
Point(51) = {w*3/4-R-l1, h3p5, 0, lc};
//+
Point(52) = {w*3/4+R+l1, h3p5, 0, lc};
//+
Point(53) = {w*3/4+R, h3p5, 0, lc};
//+
Point(54) = {w*3/4, h3p5, 0, lc};
//+
Point(55) = {w*3/4-l2/3, h3-l1, 0, lc};
//+
Point(56) = {w*3/4-l2/3, h3, 0, lc};
//+
Point(57) = {w*3/4-l2, h3-l1, 0, lc};
//+
Point(58) = {w*3/4-l2, h3, 0, lc};
//+
Point(59) = {w*3/4+l2/3, h3-l1, 0, lc};
//+
Point(60) = {w*3/4+l2/3, h3, 0, lc};
//+
Point(61) = {w*3/4+l2, h3-l1, 0, lc};
//+
Point(62) = {w*3/4+l2, h3, 0, lc};
// HORIZONTAL LINES
//+
Line(2) = {4, 3};
//+
Line(3) = {5, 6};
//+
Line(4) = {8, 7};
//+
Line(18) = {15, 43};
//+
Line(30) = {39, 43};
//+
Line(47) = {39, 41};
//+
Line(32) = {41, 45};
//+
Line(49) = {45, 58};
//+
Line(46) = {56, 58};
//+
Line(48) = {56, 60};
//+
Line(42) = {62, 60};
//+
Line(50) = {62, 16};
//+
Line(5) = {10, 9};
//+
Line(1) = {1, 2};
// VERTICAL LINES
// LEFT
//+
Line(13) = {5, 4};
//+
Line(12) = {7, 5};
//+
Line(19) = {10, 15};
//+
Line(10) = {1, 10};
//+
Line(33) = {7, 15};
// RIGHT
//+
Line(9) = {6, 3};
//+
Line(8) = {8, 6};
//+
Line(20) = {9, 16};
//+
Line(6) = {2, 9};
//+
Line(34) = {8, 16};
//
// HEATING PIPES
//+
Circle(14) = {25, 33, 28}; // {w/4, h3p5, 0, R, 0, 2*Pi};
//+
Circle(21) = {28, 33, 25};
//+
Circle(15) = {50, 54, 53}; // {3/4 * w, h3p5, 0, R, 0, 2*Pi};
//+
Circle(36) = {53, 54, 50};
//+
Circle(16) = {w/4, h3p5, 0, r, 0, 2*Pi};
//+
Circle(17) = {3/4 * w, h3p5, 0, r, 0, 2*Pi};
//+
Curve Loop(7) = {14, 21};
//+
Curve Loop(8) = {16};
//+
Plane Surface(5) = {7, 8};
//+
Curve Loop(9) = {15, 36};
//+
Curve Loop(10) = {17};
//+
Plane Surface(6) = {9, 10};
//+
// CURVES OUTLINING THE LEFT PROFILE SHEET
Circle(22) = {27, 33, 26};
//+
BSpline(23) = {26, 17, 38};
//+
BSpline(24) = {25, 23, 39};
//+
Line(25) = {42, 43};
//+
Line(26) = {44, 45};
//+
BSpline(27) = {27, 18, 40};
//+
BSpline(28) = {28, 24, 41};
//+
Line(29) = {38, 42};
//+
Line(31) = {40, 44};
//+
// CURVES OUTLINING THE RIGHT PROFILE SHEET
Circle(35) = {52, 54, 51};
//+
BSpline(37) = {51, 46, 55};
//+
BSpline(38) = {50, 48, 56};
//+
BSpline(39) = {52, 47, 59};
//+
BSpline(40) = {53, 49, 60};
//+
Line(41) = {59, 61};
//+
Line(43) = {61, 62};
//+
Line(44) = {55, 57};
//+
Line(45) = {57, 58};
// PHYSICAL CURVES
//+
Physical Curve("Hot Inlet", 16) = {16};
//+
Physical Curve("Cold Outlet", 17) = {17};
//+
Physical Curve("Underfloor", 18) = {2};
//+
Physical Curve("Coverfloor", 19) = {1};
//+
Physical Curve("Periodic Boundary Left", 20) = {13, 12, 33, 19, 10};
//+
Physical Curve("Periodic Boundary Right", 21) = {9, 8, 34, 20, 6};
//+
// PIPES
Physical Surface("Piping", 26) = {5, 6};
//+
// INSULATION HEAT
Curve Loop(4) = {13, 2, -9, -3};
//+
Plane Surface(2) = {4};
//+
Physical Surface("Insulation Heat", 25) = {2};
//+
// INSULATION IMPACT NOISE
Curve Loop(5) = {3, -8, 4, 12};
//+
Plane Surface(3) = {5};
//+
Physical Surface("Insulation Impact Noise", 23) = {3};
//+
// SCREED (DRY)
Curve Loop(6) = {5, -6, -1, 10};
//+
Plane Surface(4) = {6};
//+
Physical Surface("Screed", 24) = {4};
//+
// THERMAL CONDUCTION SHEET
Curve Loop(11) = {5, 20, -50, 42, -48, 46, -49, -32, -47, 30, -18, -19};
//+
Plane Surface(7) = {11};
//+
Physical Surface("Thermal Conduction Sheet", 27) = {7};
//+
// PROFILE SHEETS
Curve Loop(12) = {29, 25, -30, -24, -21, 28, 32, -26, -31, -27, 22, 23};
//+
Plane Surface(8) = {12};
//+
Curve Loop(13) = {44, 45, -46, -38, -36, 40, -42, -43, -41, -39, 35, 37};
//+
Plane Surface(9) = {13};
//+
Physical Surface("Profile Sheets", 28) = {8, 9};
//+
// AIR GAPS
Curve Loop(14) = {14, 28, 47, 24};
//+
Plane Surface(10) = {14};
//+
Curve Loop(15) = {15, 40, 48, 38};
//+
Plane Surface(11) = {15};
//+
Physical Surface("Air Gap", 49) = {11, 10};
//+
// CARRIER MATERIAL//+
Curve Loop(16) = {33, 18, -25, -29, -23, -22, 27, 31, 26, 49, -45, -44, -37, -35, 39, 41, 43, 50, -34, 4};
//+
Plane Surface(12) = {16};
//+
Physical Surface("Carrier", 51) = {12};