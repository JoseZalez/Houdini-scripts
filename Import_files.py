#Get a path and a file type and import all the objects matching in the folder + subdirectories
#https://www.linkedin.com/in/jose-gonzalezvfx/

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
        
        #Create a word filter
        filter_layout = QHBoxLayout()
        lbl = QLabel("Word filter:")
        self.filter = QLineEdit("")
        filter_layout.addWidget(lbl)
        filter_layout.addWidget(self.filter)
        filter_layout.setSpacing(10)
 
        #Create a check for looking for files in the subdirectories
        subdir_layout = QHBoxLayout()
        self.subdir = QCheckBox("", self)
        subdir_layout.addWidget(QLabel("Check in subdirectories:"))
        subdir_layout.addWidget(self.subdir)
        subdir_layout.setSpacing(10)
 
         #Create a check for fbx import
        fbx_layout = QHBoxLayout()
        self.fbx = QCheckBox("", self)
        fbx_layout.addWidget(QLabel("Import as FBX:"))
        fbx_layout.addWidget(self.fbx)
        fbx_layout.setSpacing(1)
       
        #Create a check for abc import
        abc_layout = QHBoxLayout()
        self.abc = QCheckBox("", self)
        abc_layout.addWidget(QLabel("Import as Alembic:"))
        abc_layout.addWidget(self.abc)
        abc_layout.setSpacing(1)

        #Set a button to start
        self.button = QPushButton('Create')
 
        #Add all the layout together
        main_layout.addLayout(filepath_layout, stretch=1)
        main_layout.addLayout(extension_layout, stretch=1)
        main_layout.addLayout(filter_layout, stretch=1)
        main_layout.addLayout(subdir_layout, stretch=1)
        main_layout.addLayout(fbx_layout, stretch=1)
        main_layout.addLayout(abc_layout, stretch=1)
        main_layout.addWidget(self.button)
        self.setLayout(main_layout)
        
        #Start the main code
        self.button.clicked.connect(self.main)

    def main(self):
        
        #Get a list of the nodes selected, we will be using just the first one
        geo_node=hou.selectedNodes()               

        #Check if the user selected a Node, if not returns a message
        if not geo_node:
            hou.ui.displayMessage("Please select a node to import the files into", buttons=('OK',), severity=hou.severityType.Message, default_choice=0, close_choice=0, title="Select a node",details_expanded=False)
            
        else:
            self.importfiles()
                    
    def getlist_names(self,list_paths): #Get a short name for each file
    
        name_list_all=[]
        
        for i in list_paths:
            i=i[i.rfind('\\')+1:]
            i=i[:-4]
            name_list_all.append(i)  
            
        return name_list_all
        
    def getlist_paths(self):
        
        empty=0
        
        path=self.filepath.text()
        extension = self.extension.text()
        filter = self.filter.text()
        list_paths=[]
        file_list =[]
        
        if not path.endswith("\\"):
            path=path + "\\"
            
        if self.subdir.isChecked():
            
                        
            #Gets all the subdirectories files and creates a path for each
            for r, d, f in os.walk(path):
                
                for file in f:

                    #Append files
                    file_list.append(os.path.join(r, file))
        
        else:

            for file in os.listdir(path):
                #Gets all the file paths in the input path    
                file_list.append(path+file)
                
        
        for file in file_list:
                    
            file_path = file
                                
                                
            if(file.endswith(extension) and file.find(filter)!=-1):
                    
                list_paths.append(file_path)

        #Returns a list of all the files with a short name
        name_list_all=self.getlist_names(list_paths)
        
        #Creates a list with the index of the files selected by the user
        index_list=hou.ui.selectFromList(name_list_all, exclusive=False, title='Select files', column_header="Files", num_visible_rows=10, clear_on_cancel=False)
        
        if not index_list:
            empty=1
        
        chosen_files=[]
        name_list=[]
        
        #Creates a new name list with just the files selected from the user 
        for j in index_list:
        
            name_list.append(name_list_all[j])

        #Creates a new list with just the files selected from the user 
        for x in index_list:
        
            chosen_files.append(list_paths[x])

        return chosen_files,name_list,empty;

        
        
    def importfiles(self):
    
        #Get a list of the nodes selected, we will be using just the first one
        geo_node=hou.selectedNodes()               

        tuple_list=self.getlist_paths()
        chosen_files=tuple_list[0]
        name_list = tuple_list[1]
        empty = tuple_list[2]

        #Iterate for every file path and creates a file node with the path loaded
        for file_path in chosen_files:
            if self.fbx.isChecked():
                    
                fbx_file = hou.hipFile.importFBX(file_path)
                #fbx_file.moveToGoodPosition()
                      
            elif self.abc.isChecked():
                        
                file_node= geo_node[0].createNode("alembic")
                file_node.parm("fileName").set(file_path)
                file_node.moveToGoodPosition()                        
                    
            else:
                
                file_node= geo_node[0].createNode("file")
                file_node.parm("file").set(file_path)
                file_node.moveToGoodPosition()               
        
           
#Starts the script window for the user
app = QApplication.instance()
if app is None: 
    app = QApplication(sys.argv)      
geoUI = UI()
geoUI.show()
