## Vector and 3 float

  There are different types of vectors type, a vector can be a point vector, which is transformed and rotated, 
  normal, which can only be rotated, color or none, which ar neither transformed or rotated. There are a lot more types.
  
  Attributes like position are stored as point, and vectors as rest are stored as none since we dont want the values to change.
  Vectors are modified by transforms, 3 floats are not.
  
  Theres more information [here](https://www.sidefx.com/docs/houdini/vex/functions/setattribtypeinfo.html)
  
  and the code to change the attrib type is setattribtypeinfo(geoself(), aclass, attrib, atype);
  
  as setattribtypeinfo(0, "point", "myVector", "point");  
  
## Using abcframe in alembics 

  When using the intrinsic attribute, always set the new time parameter to be a float (1.0 instead of 1 even when declaring it as a float) or the attribute wont work.


## Substeping
   
   Inside dops there are 3 ways of using substeps.
   
   -Solver substeps: this will run all the microsolvers, including the source nodes as many timesteps as substeps we have.  CFL shouldnt be modified from 1.
   
   -Dop substeps: they are a special case, this are for brute forcing the sim, and should only be used when there are animated parameters inside the dopnet and we need them to be interpolated between frames (I.E: keyframing the disturbance from 3 to 0.2 in very few frames).
   
   -Gas substeps node: this one allows to run substeps in a specific connection of our dopnet. You just need to be careful since if the source is mving fast and is connected to this node, other parameters like dissipation wont be calculated in timesteps so they would dissipate in a block shape. This could be fixed if insted of using keyframes we use an expression.
   
## Retiming

  When retiming volumes, use the cubic interpolation with the advected blend mode. You might get flickering on .0 frames, a hack to prevent this is to offseet the start frame by +.25 for example, using now only interpolated frames.
   
## Split and get last element from a string

```
  i@__nameid = atoi(split(@name,"_")[-1]);
```
  
## Random orient
```
  vector axis=sample_direction_uniform(rand(@ptnum));
  
  float angle=ch("angle");
  
  p@orient=quaternion(angle,axis);
```
## Intersection vector and grid
```
  vector dir2=point(1,"dir2",0);

  @P+=v@dir1*(dot(dir2,point(1,"P",0)-@P)/dot(dir2,v@dir1));
```
  https://sites.google.com/site/fujitarium/Houdini/fx-procedural-processes/geometry-intersection

## Get transformation matrix

```
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
```   

### 2 point based with Normal
```
    vector P0 = point(0,"P",0);
    vector P1 = point(0,"P",1);
    vector N = point(0,"N",0);

    v@xAxis=normalize(P0-P1);
    v@zAxis=normalize(cross(@xAxis,N));
    v@yAxis=normalize(N);

    4@mytransform=set(@xAxis,@yAxis,@zAxis,@P);

    setcomp(@mytransform,0,0,3);
    setcomp(@mytransform,0,1,3);
    setcomp(@mytransform,0,2,3);
```
## Apply it
```
    matrix mytransform = point(1,"mytransform",0);
    v@P*=invert(mytransform);
    v@v*=matrix3(invert(mytransform));
```
        
~~ Using transform by attrb will also multiply custom attributes if wanted
        
## Check attribute exist

    i@hasAttrib = hasattrib(0, "point", "attribName");
    
## Remove particles below geo
```
    vector ray = {0,1,0};
    
    vector p;
    float u,v;
    int intersect = intersect(1,@P,ray*1e6,p,u,v);
    
    if(intersect !=-1) i@dead = 1;
```

## Use .chan camera data

To use .chan files automatically create a chop network, load the .chan with a file node, use an export node with the export flag on, set the channels you want to load in as "chan[1-6]" for example, the camera node in the node parameter and the attributes in order they were written in the .chan file "t[xyz] r[xyz]" ,for example.

## Get min max 

Shorter method than attribute promote.

IMPORTANT : run over detail

This method is slower than attribute promote, just in case we cant use them.

```
int pts[]=expandpointgroup(0,"*");
float min,max;

foreach(int pt;pts){

    float ptmax=point(0,"__test",pt);
    float ptmin=point(0,"__test",pt);
    
    if(pt == 0){
        min = ptmin;
        max = ptmax;
    }
    else{
        if(ptmax > max) max = ptmax;
        else if(ptmin < min) min = ptmin;
    }
}

f@min=min;
f@max=max;
```

Shorter version but really heavy, DONT USE

```
int pts[]=expandpointgroup(0,"*");
float val[];

foreach(int pt;pts){

    append(val,float(point(0,"__test",pt)));
}

f@min=min(val);
f@max=max(val);
```
### OPENCL implementation

For a way faster method check a opencl implementation https://github.com/JoseZalez/Houdini-scripts/blob/master/OPENCL.md

# Intersection 2 lines
    
## PYTHON

 ```
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
```

### Faster implementation with vex (line 1 first input, line 2 second input)

```
vector dir = point(1,"P",1)-point(1,"P",0);

vector p,uv;

intersect(0,point(1,"P",0),dir,p,uv);

addpoint(0,p);
```
Vex function planepointdistance might also work for some cases (gets the intersection based on the plane normal not the line direction)


## Get index for random shared attribute

When you have different instances with an id but there are number missing between them and you need to iterate in a wedge or something similar.

Result is much faster just using a for loop with the iteration metadata.

```
node = hou.pwd()
geo = node.geometry()

scatter_list=[]

geo.addAttrib(hou.attribType.Prim,"id", 0)

id=0


for prim in geo.prims():
    scatter_val=prim.attribValue("scatter_id")
    if scatter_val not in scatter_list:
        scatter_list.append(scatter_val)

for prim in geo.prims():
    scatter_value=prim.attribValue("scatter_id")
    id=scatter_list.index(scatter_value)
    prim.setAttribValue("id",id)
```
Extra thing if you need to write the list on detail, if its not declared as an array the list will be written as individual lists.

```
attrib = geo.addArrayAttrib(hou.attribType.Global, "scatter_id", hou.attribData.Int , tuple_size=10)
geo.setGlobalAttribValue(attrib, scatter_list)
```
Another vex solution using uniquevals, also slower than using a for loop.

```
int values [] = uniquevals(0, "prim", "index");

int prims[] = expandprimgroup(0, "*");

foreach(int prim;prims){
    int prim_value=primattrib(0,"index",prim,0);
    int scatter_id=find(values,prim_value);
    setprimattrib(0,"scatter_id",prim,scatter_id);
}
```
