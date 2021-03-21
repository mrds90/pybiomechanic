import numpy as np
from biomechanics import *

class Body:
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
    def __init__(self,label:str,mass:float,inertia:np.array,anthropometric:dict,body:Body):
        self.__label=label
        self.__mass=mass
        self.__inertia=inertia
        self.__anthropometric=anthropometric
        self.__jointCenter:dict
        self.__centerOfMass:CenterOfMass
        self.__body=body
        self.__markers=[]
        self.__orientatation={}
    def set_markers(*markers):
        # try method to verify Marker Objet type is missing
        for marker in markers:
            self.__markers.append(marker)
    def calculate_joint_center():
        pass #define for each kind of segment
    def set_joint_center(self,proximalJointCenter:JointCenter, distalJointCenter:JointCenter): #pelvis case the order is rigth and left hip
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
                self.__centerOfMass=CenterOfMass(self.__jointCenter[0].position,self.__jointCenter[1].position,proportionalProximalDistance,self.__label,self.__jointCenter[0].fs)
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
    @property
    def anthropometric(self):
        return self.__anthropometric
    @property
    def jointCenter(self):
        return self.__jointCenter
    @property
    def orientatation(self):
        return self.__orientatation
    @inertia.setter
    def orientatation(self,orientatation:dict):
        try:
            if type(orientatation) is dict:
                self.__orientatation=orientatation
            else:
                raise ValueError
        except ValueError:
            print('ERROR: wrong type')



class Pelvis(Segment):
    def __init__(self,body:Body,pelvisWidth:float): #pelvisWidth in meters
        Segment.__init__('Pelvis',Segment.set_mass(-7.498,0.0976,0.04896,body=body),Segment.set_inertia(-775, 14.7, 1.685,-1568 ,12 ,7.741,-934,11.8,3.44,body=body),{'pelvisWidth':pelvisWidth},body)
    def set_markers (sacrum, asisR, asisL):
        Segment.set_markers(sacrum, asisR, asisL)
    def set_joint_center(self):
        coefU=self.anthropometric['pelvisWidth']*0.598
        coefV=self.anthropometric['pelvisWidth']*0.344
        coefW=-self.anthropometric['pelvisWidth']*0.29
        hip_r=JointCenter('hip_r',self.markers[1],self.markers[2],self.markers[0],order=[1,2,3],coefU=coefU,coefV=-coefV,coefW=coefW)
        hip_l=JointCenter('hip_l',self.markers[1],self.markers[2],self.markers[0],order=[1,2,3],coefU=coefU,coefV=coefV,coefW=coefW) 
        Segment.set_joint_center(hip_r,hip_l)
    def calculate_local_system(self):
        k=Vector.unitary_vector(Vector.get_vector_from_two_points(self.markers[2],self.markers[1]))
        i=Vector.unitary_vector(Vector.get_vector_from_three_points(self.markers[2],self.markers[1],self.markers[0]))
        j=Vector.perpendicular_vector(k,i)
        self.orientatation={'i':i,'j':j,'k':k}

class Calf(Segment):
    def __init__(self,body:Body,kneeDiameter:float,side='rigth'): #kneeDiameter in meters
        if side=='rigth':
            self.__side=1
        elif side=='left':
            self.__side=-1
        Segment.__init__('Calf',Segment.set_mass(-1.592,0.0362,0.0121,body=body),Segment.set_inertia(-70.5, 1.134, 0.3,-1105 ,4.59 ,6.63,-1152,4.594,6.815,body=body),{'kneeDiameter':kneeDiameter},body)
    def set_markers (lateralFemoralEpicondyle, lateralMalleolus, tibialWand):
        Segment.set_markers(lateralFemoralEpicondyle, lateralMalleolus, tibialWand)
    def set_joint_center(self,ankleJointCenter:JointCenter):
        coefU=0
        coefV=0
        coefW=self.anthropometric['kneeDiameter']*0.5
        knee=JointCenter('knee_'+self.__side[0],self.markers[0],self.markers[1],self.markers[2],order=[1,2,3],coefU=coefU,coefV=coefV,coefW=self.__side*coefW,sign2=-self.__side)
        Segment.set_joint_center(knee,ankleJointCenter)
    def calculate_local_system(self):
        i=Vector.unitary_vector(Vector.get_vector_from_two_points(self.jointCenter[0],self.jointCenter[1]))
        if self.__side==1:
            j=Vector.unitary_vector(Vector.get_vector_from_three_points(self.markers[0],self.jointCenter[0],self.jointCenter[1]))
        elif self.__side==-1:
            j=Vector.unitary_vector(Vector.get_vector_from_three_points(self.jointCenter[0],self.markers[0],self.jointCenter[1]))
        k=Vector.perpendicular_vector(i,j)
        self.orientatation={'i':i,'j':j,'k':k}
        
    




