#Create a Controller to set a percentage in a copy to points for each geometry
#https://www.linkedin.com/in/jose-gonzalezvfx/

def createexpression(controller):
    
    list=[]
    for parm in controller.parms():
    
        if parm.name().startswith("percen"):
            path=parm.path()
            val="ch('{}')".format(path)
            list.append(val)
        
    #Create the string for the expression with a initial data
    
    expression="{\n"+ "float v=0;\n"
    n=1


    list_set=[]

    setval=""


    for path in list:
    
        expression= expression +"float set"+str(n)+ " = " + path + ";\n"
        setval=setval+"set"+str(n)+"+"
        list_set.append(setval)
        n+=1
    
    expression= expression + "if(pulse(int(point(-1,0,'range',0)),0,set1)) {v=0;} \n"  

    #Add the conditionals for the percentages

    for j in range(len(list_set)-1):
        
        expression= expression + "if(pulse(int(point(-1,0,'range',0)),{},{}))".format(list_set[j][:-1],list_set[j+1][:-1])
        expression=expression+ " {"+"v={};".format(j+1)+"}\n"

    
    #Close the expression
    expression = expression + "return v;\n}"
    
    return expression

#Main

#Get a list of the selected node

nodes = hou.selectedNodes()

if not nodes:

    hou.ui.displayMessage("Please select the geometry nodes to scatter", buttons=('OK',), severity=hou.severityType.Message, default_choice=0, close_choice=0, title="Select a node",details_expanded=False)

geo=nodes[0].parent()

wrangle=geo.createNode("attribwrangle","Input_points")
controller=geo.createNode("null","Controller")
switch=geo.createNode("switch")
copytopts=geo.createNode("copytopoints")
block_begin_input=geo.createNode("block_begin")
compile_end=geo.createNode("compile_end")
block_end=geo.createNode("block_end")


#Set the block_end parms

block_begin_input.parm("method").set(1)
block_begin_input.parm("blockpath").set("../"+block_end.name())

block_end.parm("itermethod").set(1)
block_end.parm("method").set(1)
block_end.parm("useattrib").set(0)
block_end.parm("blockpath").set("../"+block_begin_input.name())
block_end.parm("templatepath").set("../"+block_begin_input.name())
block_end.parm("multithread").set(1)


#Add the rand attribute to the wrangle

wrangle.parm("snippet").set("f@range=rand(@ptnum)*100;")

#Add the percentages controls to the null node

ptg = controller.parmTemplateGroup()
parm_folder = hou.FolderParmTemplate('folder', 'Controls')

i=1

default=100/len(nodes)

for node in nodes:

    parmtemplate=hou.IntParmTemplate('percentage_'+str(i), 'Geo '+str(i)+' %', 1,default_value=(default,0),min =0,max=100)
    parm_folder.addParmTemplate(parmtemplate)
    i+=1
    
ptg.append(parm_folder)
controller.setParmTemplateGroup(ptg)

#Create the compile and block begins and connect them to the switch

compile_begin_first=geo.createNode("compile_begin")
compile_begin_first.parm("blockpath").set("../"+compile_end.name())

for node in nodes:
    compile_begin=geo.createNode("compile_begin")
    compile_begin.parm("blockpath").set("../"+compile_end.name())
    compile_begin.setInput(0,node)
    block_begin_loop=geo.createNode("block_begin")
    block_begin_loop.parm("method").set(3)
    block_begin_loop.parm("blockpath").set("../"+block_end.name())
    block_begin_loop.setInput(0,compile_begin)
    
    switch.setNextInput(block_begin_loop)
    

#Connect the inputs from the nodes to create the network

compile_begin_first.setInput(0,wrangle)
block_begin_input.setInput(0,compile_begin_first)

copytopts.setInput(0,switch)
copytopts.setInput(1,block_begin_input)

block_end.setInput(0,copytopts)
compile_end.setInput(0,block_end)

switch.moveToGoodPosition()
copytopts.moveToGoodPosition()

pos=switch.position()

v1=hou.Vector2((2.0,0.0))
v2=hou.Vector2((4.0,0.0))

pos1=pos.__add__(v1)
pos2=pos.__add__(v2)

controller.setPosition(pos1)
wrangle.setPosition(pos2)

    
#Set the expression on the switch parm    
    
switch.parm("input").setExpression(createexpression(controller))

ptg = switch.parmTemplateGroup()
parm_folder = hou.FolderParmTemplate('folder', 'Spare Input')
parmtemplate=hou.StringParmTemplate ('spare_input0','Spare Input 0', 1 ,naming_scheme=hou.parmNamingScheme.Base1, string_type=hou.stringParmType.FileReference, tags={ "opfilter" : "!!SOP!!",  "oprelative" : ".", })
parm_folder.addParmTemplate(parmtemplate)
ptg.append(parm_folder)
switch.setParmTemplateGroup(ptg)

switch.parm("spare_input0").set("../"+block_begin_input.name())

