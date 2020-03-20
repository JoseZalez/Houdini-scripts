#Creates a principle shader with the texture from a path connected
#https://www.linkedin.com/in/jose-gonzalezvfx/

import os

import sys
 
from PySide2.QtWidgets import QDialog, QApplication, QLineEdit, QLabel, QPushButton, QCheckBox, QHBoxLayout, QVBoxLayout
from PySide2.QtCore import Qt

class UI(QDialog):

 
    def __init__(self, parent=None):

        super(UI, self).__init__(parent)
        main_layout = QVBoxLayout()
        self.setWindowTitle("Create shader")
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        
        #Get Houdini window style and apply to interface
        self.setStyleSheet(hou.qt.styleSheet())
        self.setProperty("houdiniStyle", True)
        
        #Create a path input
        filepath_layout = QHBoxLayout()
        lbl = QLabel("Texture path:")
        self.filepath = QLineEdit("")
        filepath_layout.addWidget(lbl)
        filepath_layout.addWidget(self.filepath)
        filepath_layout.setSpacing(10)
 
        #Create an extension input
        shadername_layout = QHBoxLayout()
        lbl = QLabel("Shader name:")
        self.shadername = QLineEdit("")
        shadername_layout.addWidget(lbl)
        shadername_layout.addWidget(self.shadername)
        shadername_layout.setSpacing(10)
 
        #Set a button to start
        self.button = QPushButton('Create')
 
        #Add all the layout together
        main_layout.addLayout(filepath_layout, stretch=1)
        main_layout.addLayout(shadername_layout, stretch=1)
        main_layout.addWidget(self.button)
        self.setLayout(main_layout)
        
        #Start the main code
        self.button.clicked.connect(self.createshader)

    def createshader(self):

            #Store the path and the extension strings previously input by the user
            path = self.filepath.text()
            shadername = self.shadername.text()

            #Checks if the user closed the path, if not it closes it
            if not path.endswith("\\"):
                path=path + "\\"
                
            shader = hou.node('mat').createNode('principledshader',shadername)

            textures = os.listdir(path)
            
            
            for files in textures:
                    
                texture_path = path+files
                
                texture = hou.node('mat').createNode('texture',files)
                
                
                texture.parm("map").set(texture_path)

                name = files.lower()
                
                if "color" in name or "diff" in name:
                
                    shader.setInput(1,texture,0)
                    texture.moveToGoodPosition()
                    
                    
                elif "rough" in name:
                
                    shader.setInput(6,texture,0)
                    texture.moveToGoodPosition()
                    
                elif "metal" in name:
                
                    shader.setInput(9,texture,0)
                    texture.moveToGoodPosition()
            
                elif "specular" in name or "spec" in name:
                
                    shader.setInput(10,texture,0)
                    texture.moveToGoodPosition()
                    
                elif "emis" in name:
                
                    shader.setInput(27,texture,0)
                    texture.moveToGoodPosition()
                    
                elif "bump" in name or "normal" in name:
                
                    texture.destroy()
                    shader.parm("baseBumpAndNormal_enable").set(True)
                    
                    if "bump" in name:
                            shader.parm("baseBumpAndNormal_type").set("Bump")
                            shader.parm("baseBump_bumpTexture").set(texture_path)
                            
                    else:
                            shader.parm("baseNormal_texture").set(texture_path)
                        
                    
                elif "height" in name or "disp" in name or "depth" in name:
                
                    texture.destroy()
                    shader.parm("dispTex_enable").set(True)
                    shader.parm("dispTex_texture").set(texture_path)
                    
                    
                else:
                
                    hou.ui.displayMessage("Couldnt connect " +files, severity=hou.severityType.Message, default_choice=0, close_choice=0, title="Texture not applied",details_expanded=False)
                    texture.moveToGoodPosition()
                
            
            shader.moveToGoodPosition()
            

#Starts the script window for the user
app = QApplication.instance()
if app is None: 
    app = QApplication(sys.argv)      
shaderUI = UI()
shaderUI.show()
