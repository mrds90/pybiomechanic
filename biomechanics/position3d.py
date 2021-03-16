import numpy as np
from scipy import signal
from biomechanics import Segment


class Point3D:
    def __init__(self,position:np.array,label:str,samplingFrecuency:int):
        try:
            if (position.shape[0] ==3 or position.shape[1] ==3) and type(label) is str:
                self.__position=position
                self.__label=label
                self.__fs=samplingFrecuency #sampligFrecuency
                self.__speed=self.__get_derivative(self.__position)
                self.__aceleration=self.__get_derivative(self.__speed)
            else:
                raise ValueError
        except ValueError:
            if not(type(label) is str):
                print ('ERROR: label must be string type')    
            else:
                print ('the dimensions are wrong, it must be at least one dimension of size 3')
    #method
    def filter (self):
        fc = 8  # Cut-off frequency of the filter
        w = fc / (self.__fs / 2) # Normalize the frequency
        b, a = signal.butter(2, w, 'low')
        if self.__position.shape[0]==3:
            self.__position=signal.filtfilt(b, a, self.__position,axis=1)
        elif self.__position.shape[1]==3:
            self.__position=signal.filtfilt(b, a, self.__position,axis=0)
        self.__speed=self.__get_derivative(self.__position)
        self.__aceleration=self.__get_derivative(self.__speed)
    def __get_derivative(self,variable):
        if variable.shape[0]==3:
            return np.gradient(variable,1/self.__fs,axis=1)  # dvariable/dTime (time in colums)
        elif variable.shape[1]==3:
            return np.gradient(variable,1/self.__fs,axis=0)  # dvariable/dTime (time in rows)
            
    #properties 
    @property
    def label(self):
        return self.__label
    @label.setter
    def label(self,newLabel:str):
        try:
            if type(newLabel) is str:
                self.__label=newLabel
            else:
                raise ValueError
        except ValueError:
            print ('ERROR: label must be a string')
    @property
    def position(self):
        return self.__position
    @position.setter
    def position(self,newPosition:np.array):
        self.__position=newPosition
    @property
    def speed(self):
        return self.__speed
    @property
    def aceleration(self):
        return self.__aceleration
    @property
    def fs(self):
        return self.__fs
class Marker (Point3D):
    def __init__(self,position:np.array,label:str,samplingFrecuency:int,segment:Segment):
        Point3D.__init__(self,position,label,samplingFrecuency)
        self.__segment=segment

class CenterOfMass(Point3D):
    def __init__(self,proximal:np.array,distal:np.array,proportionalProximalDistance:float,label:str,samplingFrecuency:int):
        self.__position=proximal+(distal-proximal)*proportionalProximalDistance
        Point3D.__init__(self,self.__position,label,samplingFrecuency)

class JointCenter(Point3D):
    def __init__(self,label:str,marker1:Marker,marker2:Marker,marker3:Marker,order=[1,2,3],coefU:float,coefV:float,coefW:float): #order is 1=u, 2=v and 3=w
        self.__vectors=[None, None, None]
        self.__vectors[order[0]-1]=self.first_vector(marker1,marker2)
        self.__vectors[order[1]-1]=self.second_vector(marker1,marker2,marker3)
        self.__vectors[order[2]-1]=self.third_vector()
        self.__set_position(self,self.__vectors[0],self.__vectors[1],self.__vectors[2],marker3,coefU,coefV,coefW)
        Point3D.__init__(self.__position,label,marker1.fs)

    def first_vector(self,marker1,marker2): #first to estimate, dosent mean that is u
        return unitary_vector(marker2.position-marker1.position)
    def second_vector(self,marker1,marker2,marker3,sign=1): #second to estimate, dosent mean that is v
        auxiliar1=marker1.position-marker3.position
        auxiliar2=marker2.position-marker3.__position
        vector=None
        if auxiliar1.shape[0]==3 and auxiliar2.shape[0]==3:
            vector=np.cross(auxiliar1,auxiliar2,axis=1)
        elif auxiliar1.shape[1]==3 and auxiliar2.shape[1]==3:
            vector=np.cross(auxiliar1,auxiliar2,axis=0)
        if vector !=None:
            return sign*unitary_vector(vector)
    def third_vector(self): #third to estimate, dosent mean that is w
        if self.__vectors[0]==None:
            if self.__vectors[1].shape[0]==3 and self.__vectors[2].shape[0]==3:
                return np.cross(self.__vectors[1],self.__vectors[2],axis=1)
            if self.__vectors[1].shape[1]==3 and self.__vectors[2].shape[1]==3:
                return np.cross(self.__vectors[1],self.__vectors[2],axis=0)
        if self.__vectors[1]==None:
            if self.__vectors[0].shape[0]==3 and self.__vectors[2].shape[0]==3:
                return np.cross(self.__vectors[2],self.__vectors[0],axis=1)
            if self.__vectors[0].shape[1]==3 and self.__vectors[2].shape[1]==3:
                return np.cross(self.__vectors[2],self.__vectors[0],axis=0)
        if self.__vectors[2]==None:
            if self.__vectors[0].shape[0]==3 and self.__vectors[1].shape[0]==3:
                return np.cross(self.__vectors[0],self.__vectors[1],axis=1)
            if self.__vectors[0].shape[1]==3 and self.__vectors[1].shape[1]==3:
                return np.cross(self.__vectors[0],self.__vectors[1],axis=0)
    def __set_position(self,u,v,w,origin,coefU:float,coefV:float,coefW:float)
        self.__position=origin+coefU*u+coefV*v+coefW*w
def module(vector:np.array):
    if vector.shape[0]==3:
        return np.sqrt((vector*vector).sum(axis=1))
    elif vector.shape[1]==3:
        return np.sqrt((vector*vector).sum(axis=0))
def unitary_vector(vector:np.array):
    module=module(vector) #get module of the vector
    return np.divide(vector,np.transpose([module,module,module])) # wise element division with moudule


