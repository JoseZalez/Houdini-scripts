# Houdini-scripts
A collection of my personal Houdini Scripts.

### Contact
 [LinkedIn] 
 
 [Vimeo]
 
 [LinkedIn]: https://www.linkedin.com/in/jose-gonzalezvfx/
 [Vimeo]: https://vimeo.com/josezalez
 
## Scripts

* Add parameter comments to camera
* Import multiple agent clips
* Import files
* Principal shader from path
* Instace based on percentage


### Install

Simply create a new tool in your toolbar, paste the code, save and execute.

### Extra information

I created 2 separate documents with a set of tips, useful scripts and an introduction to OpenCL with some examples.

 [CheatSheet](https://github.com/JoseZalez/Houdini-scripts/blob/master/CheatSheet.md)
 
 [OPENCL](https://github.com/JoseZalez/Houdini-scripts/blob/master/OPENCL.md)
 
# Add parameter comments to camera

Selecting a camera and a node, gets the node parameters and allows you to select from a list the parameters you want to display on the camera.

Allows to *Create*, *Add* and *Reset* the parameter interface.

With the *Add* function you can add parameters from different nodes.

The parameters update automatically.


## Usage

Simply add the code to a custom script on your toolbar, save, open it and CTRL+C your camera node, CTRL+V on the camera node box on the plugin to paste the path, do the same for the node you want the parameters from.

![alt tag](https://raw.githubusercontent.com/JoseZalez/Houdini-scripts/master/images_examples/parms_camera_ui.png)
![alt tag](https://raw.githubusercontent.com/JoseZalez/Houdini-scripts/master/images_examples/parms_camera.png)

# Import multiple agent clips

Allows you to import multiple clips to an *Agent Clip* node selecting them from a list of the path introduced, setting automatically the path and the name.

## Usage

Paste your clip path into the path box and select *Import* to import the selected clips into the *Agent Clip* node, if there are already clips in the node the new ones will be just added at the end.

If your animations are in place simply check the box to set them automatically to In-Place.

### Reminder

If you select to convert the clips to In-Place remember to select a *Locomotion Node* in the *Locomotion Settings*.

![alt tag](https://raw.githubusercontent.com/JoseZalez/Houdini-scripts/master/images_examples/import_agent_clip.png)

# Principal shader from path

Given a path with the textures, creates a principal shader with all the images connected to their respective inputs including displacement, bump and normal maps. 

Returns a message if a image input wasnt found.

![alt tag](https://raw.githubusercontent.com/JoseZalez/Houdini-scripts/master/images_examples/create_shader.png)

# Import files

Imports the files in a path or in the subdirectories given a path and an extension.

*Import as FBX* allows you to import FBX with animation in *SOP* level.

![alt tag](https://raw.githubusercontent.com/JoseZalez/Houdini-scripts/master/images_examples/import_files_path.png)

# Instace based on percentage

Creates a copy to points and Controller with the percentage of each geometry you want to copy inside a foreach loop

![alt tag](https://raw.githubusercontent.com/JoseZalez/Houdini-scripts/master/images_examples/scatter/scatter_preview.png)

## Usage

With the points where you want to copy the geometry created, select the geometry you want to copy on the points:

![alt tag](https://raw.githubusercontent.com/JoseZalez/Houdini-scripts/master/images_examples/scatter/Scatter_compiled_1.png)

Then execute the script. Select the created nodes and press Shift+L to lay out them. It will create a *for loop* network with *compile blocks* already with the setup needed and a *controller*

Connect your points to the *Input_points wrangle* and visualize the *compile_end*. Then simply use the *controller* to select the percentages you want.

![alt tag](https://raw.githubusercontent.com/JoseZalez/Houdini-scripts/master/images_examples/scatter/Scatter_compiled_2.png)


### Reminder

For now please always use percentages that add up to 100% to get the desired results.

## License

Public domain.
