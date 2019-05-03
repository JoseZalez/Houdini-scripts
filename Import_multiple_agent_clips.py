#Imports multiple clips selected from a list to a Houdini agent clip node
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
        self.setWindowTitle("Import animation clips")
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
        
        #Create a check for convert to In-Place
        inplace_layout = QHBoxLayout()
        self.inplace = QCheckBox("", self)
        inplace_layout.addWidget(QLabel("Convert to In-Place:"))
        inplace_layout.addWidget(self.inplace)
        inplace_layout.setSpacing(10)

        #Set a button to start
        self.button = QPushButton('Import')

        #Set a button to add
        self.buttonAdd = QPushButton('Add')
 
        #Add all the layout together
        main_layout.addLayout(filepath_layout, stretch=1)
        main_layout.addLayout(inplace_layout, stretch=1)
        main_layout.addWidget(self.button)        
        main_layout.addWidget(self.buttonAdd)
        self.setLayout(main_layout)
        
        #Start the main code
        self.button.clicked.connect(self.main)
        self.buttonAdd.clicked.connect(self.mainAdd)

    def main(self): #Check if the user selected a node and check if its a agent clip node
        

        nodes = hou.selectedNodes()
        
        if not nodes or 'agentclip' not in nodes[0].type().name() :

            hou.ui.displayMessage("Please select a Agent Clip node to import the clips into", buttons=('OK',), severity=hou.severityType.Message, default_choice=0, close_choice=0, title="Select a node",details_expanded=False)
                
        else:
        
            self.importclips()
            
    def mainAdd(self): #Check if the user selected a node and check if its a agent clip node
    
        nodes = hou.selectedNodes()
        
        if not nodes or 'agentclip' not in nodes[0].type().name() :

            hou.ui.displayMessage("Please select a Agent Clip node to add the clips into", buttons=('OK',), severity=hou.severityType.Message, default_choice=0, close_choice=0, title="Select a node",details_expanded=False)
                
        else:
        
            self.add()
        
    def path(self): #Returns the fixed path

        path = self.filepath.text()

        if not path.endswith("\\"):
            path=path + "\\"

        return path

    def getlist_paths(self):
        
        empty=0
        
        path=self.path()
        file_list = os.listdir(path)
        list_paths=[]

        #Gets all the clip paths in the input path
        for clip in file_list:
                    
            clip_path = path+clip
                                
                                
            if(clip.endswith("fbx")):
                    
                list_paths.append(clip_path)

        #Returns a list of all the files with a short name
        name_list_all=self.getlist_names(list_paths)
        
        #Creates a list with the index of the clips selected by the user
        index_list=hou.ui.selectFromList(name_list_all, exclusive=False, title='Select clips', column_header="Clips", num_visible_rows=10, clear_on_cancel=False)
        
        if not index_list:
            empty=1
        
        chosen_clips=[]
        name_list=[]
        
        #Creates a new name list with just the clips selected from the user 
        for j in index_list:
        
            name_list.append(name_list_all[j])

        #Creates a new list with just the clips selected from the user 
        for x in index_list:
        
            chosen_clips.append(list_paths[x])

        return chosen_clips,name_list,empty;

    def getlist_names(self,list_paths): #Get a short name for each clip
    
        name_list_all=[]
        
        for i in list_paths:
            i=i[i.rfind('\\')+1:]
            i=i[:-4]
            name_list_all.append(i)  
            
        return name_list_all
        
        
    def importclips(self): #Imports the clips into the agent clip node
    
        n=0
        j=0
        i=0
        nodes = hou.selectedNodes()
		load_clip=nodes[0]
        
        tuple_list=self.getlist_paths()
        
        chosen_clips=tuple_list[0]
        name_list = tuple_list[1]
        empty = tuple_list[2]
        
        if empty != 1: 

            clipsparm = load_clip.parm("clips")
            clipsparm.set(len(chosen_clips))
            parms = load_clip.parms()
            
            #Gives to each clip parm a name and the file path, sets it to fbx and convert to in-place if selected in the UI
            for x in parms:
                
                if x.name().startswith("name"):
                    x.set(name_list[n])
                    n+=1
                elif x.name().startswith("file"):
                    x.set(chosen_clips[j])
                    j+=1
                elif x.name().startswith("source"):
                    x.set(1)
                elif x.name().startswith("converttoinplace") and self.inplace.isChecked():
                    x.set(1)

    def add(self): #Same as importclips but without deleting previous clips
    
        n=0
        j=0

        nodes = hou.selectedNodes()

        load_clip=nodes[0]
        clipsparm = load_clip.parm("clips")
        i=clipsparm.eval()

        tuple_list=self.getlist_paths()
        chosen_clips=tuple_list[0]
        name_list = tuple_list[1]
        empty = tuple_list[2]
        
        if empty != 1:
        
            clipsparm = load_clip.parm("clips")
            clipsparm.set(len(chosen_clips)+i)
            parms = load_clip.parms()
            
            for x in parms:
                if x.name().startswith("name"):
                    if not x.eval():
                            x.set(name_list[n])
                            n+=1
                elif x.name().startswith("file"):
                    if not x.eval():
                            x.set(chosen_clips[j])
                            j+=1
                elif x.name().startswith("source"):
                    x.set(1)
                elif x.name().startswith("converttoinplace") and self.inplace.isChecked():
                    x.set(1)

#Starts the script window for the user
app = QApplication.instance()
if app is None: 
    app = QApplication(sys.argv)      
clipsUI = UI()
clipsUI.show()