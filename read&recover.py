#1. read data from file 
#2. recover all subtriangles(see ?layerRecoveredAll.png, ?stands for number of subtriangle layers)
#3. recover only the northwest subtriangle and its neighbours(see ?layerRecoveredBorder.png, ?stands for number of subtriangle layers)
from triangle import * 

north=True
west=True

for nLayer in range(1,6):#layer of subtriangles
    print "nLayer=",nLayer
    name="%ilayerData" %nLayer
    #recover all triangles from file    
    t2=triangle()
    t2.listDrawAllSubTrg(name)
    #recover the "northwest" triangle and its neighbours from file
    t2=triangle()
    t2.listDrawBorderSubTrg(name,north,west)
    
    
    