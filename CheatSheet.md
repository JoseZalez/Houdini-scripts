## Vector and 3 float

  There are different types of vectors type, a vector can be a point vector, which is transformed and rotated, 
  normal, which can only be rotated, color or none, which ar neither transformed or rotated. There are a lot more types.
  
  Attributes like position are stored as point, and vectors as rest are stored as none since we dont want the values to change.
  Vectors are modified by transforms, 3 floats are not.
  
  Theres more information [here](https://www.sidefx.com/docs/houdini/vex/functions/setattribtypeinfo.html)
  
  and the code to change the attrib type is setattribtypeinfo(geoself(), aclass, attrib, atype);
  
  as setattribtypeinfo(0, "point", "myVector", "point");  
  
## Substeping
   
   Inside dops there are 3 ways of using substeps.
   
   -Solver substeps: this will run all the microsolvers, including the source nodes as many timesteps as substeps we have.  CFL shouldnt be modified from 1.
   
   -Dop substeps: they are a special case, this are for brute forcing the sim, and should only be used when there are animated parameters inside the dopnet and we need them to be interpolated between frames (I.E: keyframing the disturbance from 3 to 0.2 in very few frames).
   
   -Gas substeps node: this one allows to run substeps in a specific connection of our dopnet. You just need to be careful since if the source is mving fast and is connected to this node, other parameters like dissipation wont be calculated in timesteps so they would dissipate in a block shape. This could be fixed if insted of using keyframes we use an expression.
   
## Split and get last element from a string
  i@__nameid = atoi(split(@name,"_")[-1]);
  
  
## Random orient

  vector axis=sample_direction_uniform(rand(@ptnum));
  
  float angle=ch("angle");
  
  p@orient=quaternion(angle,axis);

## Intersection vector and grid

  vector dir2=point(1,"dir2",0);

  @P+=v@dir1*(dot(dir2,point(1,"P",0)-@P)/dot(dir2,v@dir1));
  
  https://sites.google.com/site/fujitarium/Houdini/fx-procedural-processes/geometry-intersection

## Get transformation matrix
    vector P0 = point(0,"P",0);
    vector P1 = point(0,"P",1);
    vector P2 = point(0,"P",2);

    v@xAxis=normalize(P2-P1);
    v@zAxis=normalize(P1-P0);
    v@yAxis=normalize(cross(@zAxis,@xAxis));

    4@mytransform=set(@xAxis,@yAxis,@zAxis,@P);

    setcomp(@mytransform,0,0,3);
    setcomp(@mytransform,0,1,3);
    setcomp(@mytransform,0,2,3);
    
    ## Apply it
        matrix mytransform = point(1,"mytransform",0);
        v@P*=invert(mytransform);
        v@v*=matrix3(invert(mytransform));
        
        ~~ Using transform by attrb will also multiply custom attributes if wanted
        
## Check attribute exist
    i@hasAttrib = hasattrib(0, "point", "attribName");
    
## Remove particles below geo
    vector ray = {0,1,0};
    
    vector p;
    float u,v;
    int intersect = intersect(1,@P,ray*1e6,p,u,v);
    
    if(intersect !=-1) i@dead = 1;





## Intersection 2 lines
    
    # PYTHON
A = geo.point(0).position()
B = geo.point(1).position()
C = geo.point(2).position()
D = geo.point(3).position()

A=(A[0],A[2])
B=(B[0],B[2])
C=(C[0],C[2])
D=(D[0],D[2])

def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    
    inter=(x,y)
    
    geo.addAttrib(hou.attribType.Global, "inter", inter)
    

print line_intersection((A, B), (C, D))


### Faster implementation with vex (line 1 first input, line 2 second input)

vector dir = point(1,"P",1)-point(1,"P",0);

vector p,uv;

intersect(0,point(1,"P",0),dir,p,uv);

addpoint(0,p);


## OPENCL

### Example of importing a index attribute and using to to modify the y parameter (need to bind it)

#include "interpolate.h" 
float lerpConstant( constant float * in, int size, float pos);

kernel void scale( 
                 int P_length, 
                 global float * P ,
                 int id_length, 
                 global float * id 
)
{
    int idx = get_global_id(0);
    if (idx >= P_length)
        return;
    
    float3 pos = vload3(idx,P);
    pos.y = pos.y+(idx*.2);
    vstore3(pos,idx,P);
}
