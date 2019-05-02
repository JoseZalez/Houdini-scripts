#Add parameters to the camera 
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
        self.setWindowTitle("Add parameters to camera")

        #Keep the window on top always
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        
        #Get Houdini window style and apply to interface
        self.setStyleSheet(hou.qt.styleSheet())
        self.setProperty("houdiniStyle", True)
        
        #Create a path input
        camera_layout = QHBoxLayout()
        lbl = QLabel("Camera node:")
        self.camera = QLineEdit("")
        camera_layout.addWidget(lbl)
        camera_layout.addWidget(self.camera)
        camera_layout.setSpacing(10)
 
        #Create an extension input
        solver_layout = QHBoxLayout()
        lbl = QLabel("Node:")
        self.solver = QLineEdit("")
        solver_layout.addWidget(lbl)
        solver_layout.addWidget(self.solver)
        solver_layout.setSpacing(10)
 
        #Set a button to start
        self.buttonCreate = QPushButton('Create')
 
        #Set a button to delete old parms
        self.buttonAdd = QPushButton('Add') 

        #Set a button to delete old parms
        self.buttonReset = QPushButton('Reset')
 
        #Add all the layout together
        main_layout.addLayout(camera_layout, stretch=1)
        main_layout.addLayout(solver_layout, stretch=1)
        main_layout.addWidget(self.buttonCreate)
        main_layout.addWidget(self.buttonAdd)
        main_layout.addWidget(self.buttonReset)
        self.setLayout(main_layout)
        
        #Start the main code
        self.buttonCreate.clicked.connect(self.createcomment)
        self.buttonAdd.clicked.connect(self.add)
        self.buttonReset.clicked.connect(self.reset)
        
    def getCameraNode(self):

        camera_path = self.camera.text()
        return hou.node(camera_path)


    def gettext(self):
        
        #Gets the camera and solver node
        solver_path = self.solver.text()
        solver = hou.node(solver_path)

        camera = self.getCameraNode()


        #Creates a list of parms from the selected node
        all_parms = solver.parms()

        #Initialize a dictionary and a list for the parms
        thisdict ={}
        parmlist=[]

        i=0

        #Iterates for each paramater, adds the name with the value in the dictionary, also adds the name to the list
        filter_word=["Interpolation","Position","Value","Visualization","Control"]

        previousname=""

        for parm in all_parms:
            name=parm.name()
            long_name=parm.description()
            
            if not any(x in long_name for x in filter_word):
                if "enable" not in name:

                    if long_name == previousname:
                    
                        vectorname=name[:-1]
                        del parmlist[-1]
                        i-=1
                        thisdict[str(i)] =  "data+=" + "'"+ long_name +": "+"'"+" + "+ 'str(solver.parmTuple({}).eval())'.format("'"+vectorname+"'") + "+" + "'\\n'"
                        previousname=long_name
                        long_name+=" (vector) "
                    else:
                        thisdict[str(i)] =  "data+=" + "'"+ long_name +": "+"'"+" + "+ 'str(solver.parm({}).eval())'.format("'"+name+"'") + "+" + "'\\n'"
                        previousname=long_name
                        

                    parmlist.append(long_name)
                    i+=1

        text = 'data=""' + "\n"+'solver = hou.node({})'.format("'"+self.solver.text()+"'") +"\n"

        #Shows a list of all the parameters for the user to select which he wants
        selected = hou.ui.selectFromList(parmlist, exclusive=False, title='Import parameters', column_header="Parameters", num_visible_rows=10, clear_on_cancel=False)

        #Iterates for all the parms with the values from the ditionary and appends it to a string with a line jump
        for x in range(len(selected)): 
            index = str(selected[x])
            text += thisdict[index] + '\n'

        return text


    def createcomment(self):

        text_out=self.gettext()
            
        camera = self.getCameraNode()

        text_out+="return data"

        if not camera.parm("vcomment"):
                #Add a string parameter to the camera input
                ptg = camera.parmTemplateGroup()
                parm_folder = hou.FolderParmTemplate('folder', 'Notes')
                parmtemplate=hou.StringParmTemplate('vcomment', 'Text', 1)
                parmtemplate.setTags({"editor": "1","editorlang": "python"})
                parm_folder.addParmTemplate(parmtemplate)
                ptg.append(parm_folder)
                camera.setParmTemplateGroup(ptg)

                #Set the paramaters with the values in the string parameter as a expression
                camera.parm("vcomment").setExpression(text_out, hou.exprLanguage.Python)
        else:
            hou.ui.displayMessage("Please click 'Reset' to create new parameters or 'Add' to add new parameters", buttons=('OK',), severity=hou.severityType.Message, default_choice=0, close_choice=0, title="Select a node",details_expanded=False)


    def add(self):
        text_out=self.gettext()
        camera = self.getCameraNode()
        

        #Set the paramaters with the values in the string parameter
        current_text=camera.parm("vcomment").expression()
        old_out=current_text.split("\n", 1)[1]
        new_text=text_out+old_out
        
        camera.parm("vcomment").setExpression(new_text, hou.exprLanguage.Python)

        
    def reset(self):
    
        #Deletes the folder and the comment stored in the camera node
        camera = self.getCameraNode()
                
        ptg = camera.parmTemplateGroup()
        folder_to_delete = ptg.findFolder('Notes')
        ptg.remove(folder_to_delete)
        camera.setParmTemplateGroup(ptg)
        
#Starts the script window for the user
app = QApplication.instance()
if app is None: 
    app = QApplication(sys.argv)      
CommentUI = UI()
CommentUI.show()