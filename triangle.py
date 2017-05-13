import numpy as np
import matplotlib.pyplot as plt
import copy
import math
import json


#models triangle, point and subtriangle inside
class triangle:
    def __init__(self):
        self.x =[]#x coordinates of self
        self.y =[]#y coordinates of self
    def setCoordinate(self,x,y):
        self.x = x
        self.y = y
    #randomly generate it self(a triangle)
    def randGenTrg(self):
        for i in range(0,3):
            temp=np.random.rand(1)
            self.x.append(temp[0])
            temp=np.random.rand(1)
            self.y.append(temp[0])   
    def plotSelf(self):
        x=copy.copy(self.x)
        x.append(self.x[0])
        y=copy.copy(self.y)
        y.append(self.y[0]) 
        plt.plot(x,y,color='k')
    #randomly generate the point inside
    def randGenPt(self,ptList):
        self.pt=point(self)#point inside
        r1=np.random.random()
        r2=np.random.random()
        self.pt.setValue(self.x[0]*(1-math.sqrt(r1))+self.x[1]*(math.sqrt(r1)*(1-r2))+self.x[2]*r2*math.sqrt(r1),self.y[0]*(1-math.sqrt(r1))+self.y[1]*(math.sqrt(r1)*(1-r2))+self.y[2]*r2*math.sqrt(r1))
        ptList.append(self.pt.x)
        ptList.append(self.pt.y)
        self.pt.formAllTrg()
    #generate point inside from list read from file
    def listGenPt(self,ptList):
        self.pt=point(self)
        self.pt.x=ptList.pop(0)
        self.pt.y=ptList.pop(0)
        self.pt.formAllTrg()    
    def plotPt(self):
        plt.plot(self.pt.x,self.pt.y, marker='o', markersize=3, color='r')
    def printSelf(self):
        print "triangle:"
        print self.x
        print self.y
    #recursively draw random subtriangles
    def randDrawSubTrg(self,i,I,ptList):
        self.randGenPt(ptList)
        if i<I:
            self.pt.trg0.randDrawSubTrg(i+1,I,ptList)
            self.pt.trg1.randDrawSubTrg(i+1,I,ptList)
            self.pt.trg2.randDrawSubTrg(i+1,I,ptList)
        else:
            self.pt.plotTrg() 
    #function tiggers the random subtriangle generation process
    #after generating, the points are saved in a list, modeled as a complete trinomial tree(node=1 point inside)
    def randDrawAllSubTrg(self,I):
        plt.close()
        self.ptList=[]
        temp=copy.copy(self.x)
        for i in range(0,3):
            self.ptList.append(temp.pop(0))
        temp=copy.copy(self.y)
        for i in range(0,3):
            self.ptList.append(temp.pop(0)) 
        self.randDrawSubTrg(1,I,self.ptList)
        plt.savefig("%ilayerOriginal" %(I)) 
        f=open("%ilayerData"  %(I),'w')
        json.dump(self.ptList,f)
    #read data from file 
    def readData(self,name):
        f=open(name,'r')
        self.ptList=json.load(f)
        for i in range(0,3):
                self.x.append(self.ptList.pop(0))
        for i in range(0,3):
            self.y.append(self.ptList.pop(0))
        self.nLayer=int(round(math.log(len(self.ptList)+1,3)))
    #recover trinomial tree and thus the triangles from data read 
    def listDrawSubTrg(self,i,I,ptList):
        self.listGenPt(ptList)
        if i<I:
            self.pt.trg0.listDrawSubTrg(i+1,I,ptList)
            self.pt.trg1.listDrawSubTrg(i+1,I,ptList)
            self.pt.trg2.listDrawSubTrg(i+1,I,ptList)
        else:
            self.pt.plotTrg() 
    #triggers the triangles recovery process
    def listDrawAllSubTrg(self,name):
        self.readData(name)
        if self.ptList!=[]:
            plt.close()
            self.listDrawSubTrg(1,self.nLayer,self.ptList)
            plt.savefig("%ilayerRecoveredAll" %(self.nLayer))
    def cosVec(self,x1,x2,y1,y2):
        return (x1*y1+x2*y2)/(math.sqrt(math.pow(x1,2)+math.pow(x2,2))*math.sqrt(math.pow(y1,2)+math.pow(y2,2)))
    #find edge corresponds to the triangle in a direction
    def findEdge(self,north,west):
        x=copy.copy(self.x)
        y=copy.copy(self.y)
        if west==False:
            for i in range(1,3):
                x[i]=x[i]*(-1)
        if north==False:
            for i in range(1,3):
                y[i]=y[i]*(-1)   
        z=[]
        for i in range(0,3):
            z.append(y[i]-x[i])
        j=z.index(max(z))
        cos=[2,2,2]
        for i in range(0,3):
            if i!=j:
                cos[i]=abs(self.cosVec(1.0,1.0,x[i]-x[j],y[i]-y[j]))
        return cos.index(min(cos)) 
    #leverage the tree structure to quickly generate the subtriangles of interest(e.g. in northwest)
    def listDrawBorderSubTrg(self,name,north,west):
        self.readData(name)
        if self.ptList!=[]:
            plt.close()
            self.plotSelf()
            t=triangle()
            if self.nLayer==1:
                t.pt=point(self)
                t.pt.setValue(self.ptList[0],self.ptList[1])
            else:
                edge=self.findEdge(north,west)
                if edge==0:#left leaf
                    a=self.nLayer-1
                    b=self.nLayer
                elif edge==1:#middle leaf
                    b=int((pow(3,self.nLayer)+2*self.nLayer-1)/4)
                    a=b-2
                else:#right leaf
                    b=int((pow(3,self.nLayer)-1)/2)
                    a=b-3
                for i in range(0,3):
                    if i!=edge:
                        t.x.append(self.x[i])
                        t.y.append(self.y[i])
                t.x.append(self.ptList[2*a-2])
                t.y.append(self.ptList[2*a-1])
                t.pt=point(t)
                t.pt.setValue(self.ptList[2*b-2],self.ptList[2*b-1])
            t.pt.formAllTrg()
            t.pt.plotTrg()
            plt.savefig("%ilayerRecoveredBorder" %(self.nLayer))
            
        
        
            
#models the point inside a triangle  (parent)      
class point:
    def __init__(self,parent):
        self.parent=copy.deepcopy(parent)
    def setValue(self,x,y):
        self.x=x
        self.y=y
    def form1Trg(self,i):
        trg=copy.deepcopy(self.parent)
        trg.x[i]=self.x
        trg.y[i]=self.y
        return trg
    def formAllTrg(self):
        self.trg0=self.form1Trg(0)
        self.trg1=self.form1Trg(1)
        self.trg2=self.form1Trg(2)
    def plotTrg(self):
        self.trg0.plotSelf()
        self.trg1.plotSelf()
        self.trg2.plotSelf()
    def printTrg(self):
        self.trg0.printSelf()
        self.trg1.printSelf()
        self.trg2.printSelf()



















































