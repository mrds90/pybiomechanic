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
        self.__jointCenter:pos3d.JointCenter
        self.__centerOfMass:pos3d.CenterOfMass
        self.__body=body
    def set_joint_center(self,proximalJointCenter:pos3d.JointCenter, distalJointCenter:pos3d.JointCenter):
        self.__jointCenter=[proximalJointCenter,distalJointCenter]
    def set_mass(self, b0:float, b1:float, b2:float):
        self.__mass=b0+b1*self.__body.mass+b2*self.__body.height
    def set_inertia(self, b0Long:float, b1Long:float, b2Long:float,b0AntPos:float, b1AntPos:float, b2AntPos:float,b0MedLat:float, b1MedLat:float, b2MedLat:float):
        Ixx=(b0Long+b1Long*self.__body.mass+b2Long*self.__body.height)/10000 # get in [kg×m^2]
        Iyy=(b0AntPos+b1AntPos*self.__body.mass+b2AntPos*self.__body.height)/10000 # get in [kg×m^2]
        Izz=(b0MedLat+b1MedLat*self.__body.mass+b2MedLat*self.__body.height)/10000 # get in [kg×m^2]
        self.__inertia=[[Ixx,0,0][0,Iyy,0][0,0,Izz]]




