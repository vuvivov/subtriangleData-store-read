#1. randomly generate a triangle and its subtriangles
#2. save data to a file(?layerdata, ?stands for number of subtriangle layers)
#3. plot all the triangles(see ?layerOriginal.png, ?stands for number of subtriangle layers)
from triangle import * 

for nLayer in range(1,6):#layer of subtriangles
    print "nLayer=",nLayer
    #create and save triangles
    t=triangle()
    t.randGenTrg()
    t.randDrawAllSubTrg(nLayer)



















































