import numpy as np
from scipy import signal
from .vectors import Vector


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
            self.__position[np.argwhere(~np.isnan(self.__position[0,:]))]=signal.filtfilt(b, a, self.__position[np.argwhere(~np.isnan(self.__position[0,:]))],axis=1)
        elif self.__position.shape[1]==3:
            self.__position[np.argwhere(~np.isnan(self.__position[:,0]))]=signal.filtfilt(b, a, self.__position[np.argwhere(~np.isnan(self.__position[:,0]))],axis=0)
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
    def __init__(self,position:np.array,label:str,samplingFrecuency:int):
        Point3D.__init__(self,position,label,samplingFrecuency)

class CenterOfMass(Point3D):
    def __init__(self,proximal:np.array,distal:np.array,proportionalProximalDistance:float,label:str,samplingFrecuency:int):
        self.__position=proximal+(distal-proximal)*proportionalProximalDistance
        Point3D.__init__(self,self.__position,label,samplingFrecuency)

class JointCenter(Point3D): 
    def __init__(self,label:str,marker1:Marker,marker2:Marker,marker3:Marker,coefU:float,coefV:float,coefW:float,order=[1,2,3],sign2=1,sign3=1,origin=3): #order is 1=u,# 2=v #and 3=w
        if origin==1:
            origin=marker1
        elif origin==2:
            origin=marker2
        elif origin==3:
            origin=marker3
        self.__vectors=[None, None, None]
        self.__vectors[order[0]-1]=self.first_vector(marker1,marker2)
        self.__vectors[order[1]-1]=self.second_vector(marker1,marker2,marker3,sign2)
        self.__vectors[order[2]-1]=self.third_vector(sign3)
        position=self.__set_position(self.__vectors[0],self.__vectors[1],self.__vectors[2],origin,coefU,coefV,coefW)
        Point3D.__init__(self,position,label,marker1.fs)
    def first_vector(self,marker1,marker2): #first to estimate, dosent mean that is u
        vector=marker2.position-marker1.position
        return Vector.unitary_vector(Vector.new_vector_from_np_array(vector))
    def second_vector(self,marker1,marker2,marker3,sign=1): #second to estimate, dosent mean that is v,
        vector1=marker1.position-marker3.position
        vector1=Vector.new_vector_from_np_array(vector1)
        vector2=marker2.position-marker3.position
        vector2=Vector.new_vector_from_np_array(vector2)
        # print ('vector1',vector1.orientatation.shape)
        # print ('vector2',vector2.orientatation.shape)
        vector=None
        return Vector.new_vector_from_np_array(sign*Vector.unitary_vector(Vector.perpendicular_vector(vector1,vector2,sign)).orientatation)
    def third_vector(self,sign=1): #third to estimate, dosent mean that is w
        if self.__vectors[0]==None:
            return Vector.perpendicular_vector(self.__vectors[1],self.__vectors[2],sign)
        if self.__vectors[1]==None:
            return Vector.perpendicular_vector(self.__vectors[2],self.__vectors[0],sign)
        if self.__vectors[2]==None:
            return Vector.perpendicular_vector(self.__vectors[0],self.__vectors[1],sign)

    def __set_position(self,u:Vector,v:Vector,w:Vector,origin,coefU:float,coefV:float,coefW:float):
        return origin.position+coefU*u.orientatation+coefV*v.orientatation+coefW*w.orientatation


