// mesh of a rectangle consisting of two materials

// geometry variables
width = 1.0;
height = 1.0;
depth = 1.0;

// number of points per edge
nx = 3;
ny = 1;
nz = 1;

// point of origin
__lst=newp;
Point(__lst) = {0,0,0};

// extrude point in x-direction
lineX[] = Extrude{width, 0, 0} { Point{__lst}; Layers{nx}; };

// extrude line in y-direction
plane01[] = Extrude{0, height / 3.0, 0} { Line{lineX[1]}; Layers{ny}; };

// extrude line in y-direction
plane02[] = Extrude{0, height / 3.0, 0} { Line{plane01[0]}; Layers{ny}; };

// extrude line in y-direction
plane03[] = Extrude{0, height / 3.0, 0} { Line{plane02[0]}; Layers{ny}; };

// extrude surfaces in z-direction
volume01[] = Extrude{0, 0, depth} { Surface{plane01[1], plane02[1], plane03[1]}; Layers{nz}; };


// define the boundary indicators
Physical Surface("left", 201) = {volume01[5], volume01[11], volume01[17]};
Physical Surface("right", 202) = {volume01[3], volume01[9], volume01[15]};
Physical Surface("bottom", 203) = {volume01[2]};
Physical Surface("top", 204) = {volume01[16]};
Physical Surface("back", 205) = {plane01[1], plane02[1], plane03[1]};
Physical Surface("front", 206) = {volume01[0], volume01[6], volume01[12]};


// define the material indicators
Physical Volume("steel", 101) = volume01[1];
Physical Volume("copper", 102) = volume01[7];
Physical Volume("aluminium", 103) = volume01[13];


