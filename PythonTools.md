
# Scripts

* Import files
* Add parameter comments to camera
* Import multiple agent clips
* Principal shader from path
* Instace based on percentage


### Install

Simply create a new tool in your toolbar, paste the code, save and execute.

# Import files

Given a path and a file extension, gets a list of the files in that current path or subdirectories. Includes a word filter. Supports FBX, Alembic and Houdini files.

*Import as FBX* allows you to import FBX with animation in *SOP* level.

[Code](https://github.com/JoseZalez/Houdini-scripts/blob/master/Import_files.py)

![alt tag](https://i.gyazo.com/002e6248921f93cfc83b0b2a7ad9e809.png)

# Add parameter comments to camera

Selecting a camera and a node, gets the node parameters and allows you to select from a list the parameters you want to display on the camera.

Allows to *Create*, *Add* and *Reset* the parameter interface.

With the *Add* function you can add parameters from different nodes.

The parameters update automatically.

[Code](https://github.com/JoseZalez/Houdini-scripts/blob/master/Camera_comments.py)


## Usage

Simply add the code to a custom script on your toolbar, save, open it and CTRL+C your camera node, CTRL+V on the camera node box on the plugin to paste the path, do the same for the node you want the parameters from.

![alt tag](https://raw.githubusercontent.com/JoseZalez/Houdini-scripts/master/images_examples/parms_camera_ui.png)
![alt tag](https://raw.githubusercontent.com/JoseZalez/Houdini-scripts/master/images_examples/parms_camera.png)

# Import multiple agent clips

Allows you to import multiple clips to an *Agent Clip* node selecting them from a list of the path introduced, setting automatically the path and the name.

[Code](https://github.com/JoseZalez/Houdini-scripts/blob/master/Import_multiple_agent_clips.py)

## Usage

Paste your clip path into the path box and select *Import* to import the selected clips into the *Agent Clip* node, if there are already clips in the node the new ones will be just added at the end.

If your animations are in place simply check the box to set them automatically to In-Place.

### Reminder

If you select to convert the clips to In-Place remember to select a *Locomotion Node* in the *Locomotion Settings*.

![alt tag](https://raw.githubusercontent.com/JoseZalez/Houdini-scripts/master/images_examples/import_agent_clip.png)

# Batch change paths

Simple script to change your path to $HIP given a drive letter and a folder name

```
keyword = "HIP_FOLDER_NAME" #"explosion" for example
drive = "Drive letter" #"D:" for example

nodes = hou.node("/").allSubChildren()


tempPath = ""

for node in nodes:

    parms = node.parms()

    for x in parms:
        if x.parmTemplate().type().name() == "String":
        
            tempPath = x.eval()

            if tempPath.startswith(drive):
                                    
                x.set("$HIP"+tempPath.split(keyword)[1])
                
```

# Principal shader from path

Given a path with the textures, creates a principal shader with all the images connected to their respective inputs including displacement, bump and normal maps. 

Returns a message if a image input wasnt found.

[Code](https://github.com/JoseZalez/Houdini-scripts/blob/master/PrincipalShader_from_path.py)

![alt tag](https://raw.githubusercontent.com/JoseZalez/Houdini-scripts/master/images_examples/create_shader.png)



# Instace based on percentage

Creates a copy to points and Controller with the percentage of each geometry you want to copy inside a foreach loop

[Code](https://github.com/JoseZalez/Houdini-scripts/blob/master/Instance_percentage_based.py)

![alt tag](https://raw.githubusercontent.com/JoseZalez/Houdini-scripts/master/images_examples/scatter/scatter_preview.png)

## Usage

With the points where you want to copy the geometry created, select the geometry you want to copy on the points:

![alt tag](https://raw.githubusercontent.com/JoseZalez/Houdini-scripts/master/images_examples/scatter/Scatter_compiled_1.png)

Then execute the script. Select the created nodes and press Shift+L to lay out them. It will create a *for loop* network with *compile blocks* already with the setup needed and a *controller*

Connect your points to the *Input_points wrangle* and visualize the *compile_end*. Then simply use the *controller* to select the percentages you want.

![alt tag](https://raw.githubusercontent.com/JoseZalez/Houdini-scripts/master/images_examples/scatter/Scatter_compiled_2.png)


### Reminder

For now please always use percentages that add up to 100% to get the desired results.



