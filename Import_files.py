#Get a path and a file type and import all the objects matching in the folder + subdirectories
#Vimeo.com/josezalez

import os

import sys
 
from PySide2.QtWidgets import QDialog, QApplication, QLineEdit, QLabel, QPushButton, QCheckBox, QHBoxLayout, QVBoxLayout
from PySide2.QtCore import Qt

class UI(QDialog):
    """"""
 
    def __init__(self, parent=None):
        """Constructor"""
        super(UI, self).__init__(parent)
        main_layout = QVBoxLayout()
        self.setWindowTitle("Import files")
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        
        #Get Houdini window style and apply to interface
        self.setStyleSheet(hou.qt.styleSheet())
        self.setProperty("houdiniStyle", True)
        
        #Create a path input
        filepath_layout = QHBoxLayout()
        lbl = QLabel("Path:")
        self.filepath = QLineEdit("")
        filepath_layout.addWidget(lbl)
        filepath_layout.addWidget(self.filepath)
        filepath_layout.setSpacing(10)
 
        #Create an extension input
        extension_layout = QHBoxLayout()
        lbl = QLabel("File extension:")
        self.extension = QLineEdit("")
        extension_layout.addWidget(lbl)
        extension_layout.addWidget(self.extension)
        extension_layout.setSpacing(10)
 
        #Create a check for looking for files in the subdirectories
        subdir_layout = QHBoxLayout()
        self.subdir = QCheckBox("", self)
        subdir_layout.addWidget(QLabel("Check in subdirectories:"))
        subdir_layout.addWidget(self.subdir)
        subdir_layout.setSpacing(10)
 
        #Set a button to start
        self.button = QPushButton('Import')
 
        #Add all the layout together
        main_layout.addLayout(filepath_layout, stretch=1)
        main_layout.addLayout(extension_layout, stretch=1)
        main_layout.addLayout(subdir_layout, stretch=1)
        main_layout.addWidget(self.button)
        self.setLayout(main_layout)
        
        #Start the main code
        self.button.clicked.connect(self.importfiles)


    def importfiles(self):

        #Get a list of the nodes selected, we will be using just the first one
        geo_node=hou.selectedNodes()

        #Store the path and the extension strings previously input by the user
        path = self.filepath.text()
        extension = self.extension.text()

        #Checks if the user closed the path, if not it closes it
        if not path.endswith("\\"):
                path=path + "\\"

        files = []

        #Check if the user selected a Node, if not returns a message
        if not geo_node:
            hou.ui.displayMessage("Please select a node to import the files into", buttons=('OK',), severity=hou.severityType.Message, default_choice=0, close_choice=0, title="Select a node",details_expanded=False)
        else:

            if self.subdir.isChecked():
                        
                        #Gets all the subdirectories files and creates a path for each
                for r, d, f in os.walk(path):
                
                    for file in f:

                        #Checks for files with the same file type as the one the user input
                        if(file.endswith(extension)):
                            files.append(os.path.join(r, file))
                
                #Iterate for every file path and creates a file node with the path loaded
                for file_path in files:
                
                    file_node= geo_node[0].createNode("file")
                    file_node.parm("file").set(file_path)
                    file_node.moveToGoodPosition()
            else:
                
                #The same as before but without iterating inside the subdirectories
                file_list = os.listdir(path)
            
                for obj in file_list:
            
                    obj_path = path+obj
                        
                        #Checks for files with the same file type as the one the user input
                    if(obj.endswith(extension)):
            
                            file_node= geo_node[0].createNode("file")
                            file_node.parm("file").set(obj_path)
                            file_node.moveToGoodPosition()
        

#Starts the script window for the user
app = QApplication.instance()
if app is None: 
    app = QApplication(sys.argv)      
geoUI = UI()
geoUI.show()