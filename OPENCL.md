
# OPENCL

Welcome to the world of OpenCL.

OpenCL in houdini can take advantage of processing data much faster than vex or compiled sops on c++.

The main takeaway is that you need to prepare the inputs and error feedback couldnt be worse sometimes.

I will post here a few code examples I create from time to time.

Before using any of these kernels, you will need to go to the bindings tab and add the different atributes you will be using.

### Example of importing a index attribute and using to to modify the y parameter

In the OpenCL bindings add the parameter P as an attribute with size 3.

 ```
#include "interpolate.h" 
float lerpConstant( constant float * in, int size, float pos);

kernel void kernelName( 
                 int P_length, 
                 global float * P
)
{
    int idx = get_global_id(0);
    if (idx >= P_length)
        return;
       
    float3 pos = vload3(idx,P);
    pos.y = pos.y+(idx*.2);
    vstore3(pos,idx,P);

 }
```

### Get min and max

Following the vex scripts from my cheatsheet, this is the implementation on OpenCL, its way faster than any other method.

For 10m points:

- Vex: 5s
- Attribute promote: 2.5s
- OpenCL: 0.5s

Wrangle before OpenCL node
```
f@valt=rand(@ptnum)*1651;
f@min;
f@max;
f@__scratchMin;
f@__scratchMax;
```

In the OpenCL node, add temp_max and temp_min as float parameters and the previous attributes from the wrangle.

Set val as only readable, min and max as writeable and __scratchMin and __scratchMax as both.

```
#include "interpolate.h" 
float lerpConstant( constant float * in, int size, float pos);

kernel void getminmax( 
                 float  temp_max ,
                 float  temp_min ,
                 int val_length, 
                 global float * val ,
                 int max_length, 
                 global float * max ,
                 int __scratchMax_length, 
                 global float * __scratchMax ,
                 int __scratchMin_length, 
                 global float * __scratchMin ,
                 int min_length, 
                 global float * min 
                 )
{
    int idx = get_global_id(0);
    if (idx > 0)
        return;
        
        
    temp_min=vload(0,val);
    temp_max=vload(0,val);
    
    for(int pt=0; pt<max_length;pt++){
    
        float value = vload(pt,val);
    
        if(value>temp_max)
            temp_max=value;
        if(value<temp_min)
            temp_min=value;
        
    }
        
    vstore(temp_max, 0,__scratchMax);
    vstore(temp_min, 0,__scratchMin);

}

kernel void writeBack( 
                 float  temp_max ,
                 float  temp_min ,
                 int val_length, 
                 global float * val ,
                 int max_length, 
                 global float * max ,
                 int __scratchMax_length, 
                 global float * __scratchMax ,
                 int __scratchMin_length, 
                 global float * __scratchMin ,
                 int min_length, 
                 global float * min 
                 )
{
    int idx = get_global_id(0);
    if (idx >= max_length)
        return;
        
    temp_min=vload(0,__scratchMin);
    temp_max=vload(0,__scratchMax);
        
       
    vstore(temp_min, idx, min);
    vstore(temp_max, idx ,max);

}
```

### Julia Set 

Create a grid with high subdivs and a point to control the range.

Wrangle before OpenCL node with the point connected to second input.
```
i@iter=0;

v@ext_pos=point(1,"P",0);

v@Cd=1;
```
And the an OPENCL node with ext position as ext, Cd, max_iter, iter and P.

```
#include "interpolate.h" 

inline float3 saturate(float x, float y, float z){
    float min = 0;
    float max = 1;
    float R= fmax(min,fmin(max,x));
    float G= fmax(min,fmin(max,y));
    float B= fmax(min,fmin(max,z));
    return (float3)(R,G,B);
}

inline float3 HUEtoRGB(float H){
    float R = fabs (H * 6 - 3) - 1;
    float G = 2 - fabs (H * 6 - 2);
    float B = 2 - fabs (H * 6 - 4);
    return saturate(R,G,B);
}
    
inline float3 HSVtoRGB(float3 HSV){
    float3 RGB = HUEtoRGB(HSV.x);
    return ((RGB - 1) * HSV.y + 1) * HSV.z;
}

inline int julia_func( float a,
                        float b, 
                        float iA, 
                        float iB,
                        int imax  )
                        
{
    float count = 0;
    while (count<imax){
          
        float newA = a*a - b*b + iA;
        float newB = 2*a*b + iB;
        
        a=newA;
        b=newB;

        
        count=count+1;
               
        if(a*a+b*b>2){
            break;        
        }
        
        
        }
    return count;
}

float lerpConstant( constant float * in, int size, float pos);

kernel void julia( 
                 int ext_length, 
                 global float * ext ,
                 int color_length, 
                 global float * color ,
                 int max_iter,
                 int iter_length, 
                 global int * iter ,
                 int P_length, 
                 global float * P
)
{
    int idx = get_global_id(0);
    if (idx >= color_length)
        return;


    float3 pos = vload3(idx,P);
    
    float3 extP = vload3(idx,ext);
        
    float value = julia_func(pos.x, pos.z,extP.x,extP.z,max_iter);
    
    float3 color_value = (float3)(value/max_iter,1,1);
    
    float3 cd= HSVtoRGB(color_value);
    
    vstore(value, idx ,iter);
    
    vstore3(cd, idx ,color);
}
```

