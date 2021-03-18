import numpy as np
import position3d as pos3d

class body:
    def __init__(self,mass:float,height):
        self.__mass=mass #must be in kilograms
        self.__height=height #must be in centimeters
    @property
    def mass(self):
        return self.__mass
    @property
    def height(self):
        return self.__height

class Segment:
    def __init__(self,label:str,mass:float,inertia:np.array,anthropometric:dict,body:body):
        self.__label=label
        self.__mass=mass
        self.__inertia=inertia
        self.__anthropometric=anthropometric
        self.__jointCenter=[]
        self.__centerOfMass:pos3d.CenterOfMass
        self.__body=body
        self.__markers=[]
    def set_markers(*markers):
        # try method to verify Marker Objet type is missing
        for marker in markers:
            self.__markers.append(marker)
    def calculate_joint_center():
        pass #define for each kind of segment
    def set_joint_center(self,proximalJointCenter:pos3d.JointCenter, distalJointCenter:pos3d.JointCenter):
        self.__jointCenter=[proximalJointCenter,distalJointCenter]
    def set_mass(self, b0:float, b1:float, b2:float,body=self.__body):
        self.__mass=b0+b1*body.mass+b2*body.height
    def set_inertia(self, b0Long:float, b1Long:float, b2Long:float,b0AntPos:float, b1AntPos:float, b2AntPos:float,b0MedLat:float, b1MedLat:float, b2MedLat:float,body=self.__body):
        Ixx=(b0Long+b1Long*body.mass+b2Long*body.height)/10000 # get in [kg×m^2]
        Iyy=(b0AntPos+b1AntPos*body.mass+b2AntPos*body.height)/10000 # get in [kg×m^2]
        Izz=(b0MedLat+b1MedLat*body.mass+b2MedLat*body.height)/10000 # get in [kg×m^2]
        self.__inertia=np.array([[Ixx,0,0][0,Iyy,0][0,0,Izz]])
    def set_center_of_mass(self,proportionalProximalDistance:float):
        try:
            if len(self.__jointCenter==2 and type(proportionalProximalDistance) is float):
                self.__centerOfMass=pos3d.CenterOfMass(self.__jointCenter[0].position,self.__jointCenter[1].position,proportionalProximalDistance,self.__label,self.__jointCenter[0].fs)
            else:
                raise ValueError
        except ValueError:
            print('ERROR: joint centers not defined')
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
    def mass(self):
        return self.__mass
    @mass.setter
    def label(self,mass:float):  
        self.__mass=mass
    @property
    def inertia(self):
        return self.__inertia
    @inertia.setter
    def inertia(self,inertia:np.ndarray):  
        try:
            if type(inertia) is np.ndarray and inertia.shape==(3,3):
                self.__inertia=inertia
            else:
                raise ValueError
        except ValueError:
            print ('ERROR: wrong type or shape')
    @property
    def body(self):
        return self.__body
    @property
    def markers(self):
        return self.__markers

class Pelvis(Segment):
    def __init__(self,body:body,pelvisWidth:float): #pelvisWidth in meters
        Segment.__init__('Pelvis',Segment.set_mass(-7.498,0.0976,0.04896,body=body),Segment.set_inertia(-775, 14.7, 1.685,-1568 ,12 ,7.741,-934,11.8,3.44,body=body),{'pelvisWidth':pelvisWidth},body)
    def set_markers (sacrum, asisR, asisL):
        Segment.set_markers(sacrum, asisR, asisL)
    def calculate_joint_center(self):
        pass  


    def calculate_local_system():
        pass
    




