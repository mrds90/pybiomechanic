import numpy as np
from biomechanics import *
# from .position3d import JointCenter

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
        self.__localSystem={}
    def set_markers(self,*markers):
        # try method, to verify Marker Objet type, is missing
        for marker in markers:
            self.__markers.append(marker)
    def calculate_joint_center():
        pass #define for each kind of segment
    def set_joint_center(self,proximalJointCenter:JointCenter, distalJointCenter:JointCenter): #pelvis case the order is rigth and left hip
        self.__jointCenter=[proximalJointCenter,distalJointCenter]
    def set_mass(self, b0:float, b1:float, b2:float,body=None):
        if body==None:
            body=self.__body
        mass=b0+b1*body.mass+b2*body.height
        self.__mass=mass
        return mass
    def set_inertia(self, b0Long:float, b1Long:float, b2Long:float,b0AntPos:float, b1AntPos:float, b2AntPos:float,b0MedLat:float, b1MedLat:float, b2MedLat:float,body=None):
        if body==None:
            body=self.__body
        Ixx=(b0Long+b1Long*body.mass+b2Long*body.height)/10000 # get in [kg×m^2]
        Iyy=(b0AntPos+b1AntPos*body.mass+b2AntPos*body.height)/10000 # get in [kg×m^2]
        Izz=(b0MedLat+b1MedLat*body.mass+b2MedLat*body.height)/10000 # get in [kg×m^2]
        inertia=np.array([[Ixx,0,0],[0,Iyy,0],[0,0,Izz]])
        self.__inertia=inertia
        return inertia
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
    def localSystem(self):
        return self.__localSystem
    @localSystem.setter
    def localSystem(self,localSystem:dict):
        try:
            if type(localSystem) is dict:
                self.__localSystem=localSystem
            else:
                raise ValueError
        except ValueError:
            print('ERROR: wrong type')



class Pelvis(Segment):
    def __init__(self,body:Body,pelvisWidth:float): #pelvisWidth in meters
        mass=self.set_mass(-7.498,0.0976,0.04896,body=body)
        inertia=self.set_inertia(-775, 14.7, 1.685,-1568 ,12 ,7.741,-934,11.8,3.44,body=body)
        Segment.__init__(self,'Pelvis',mass,inertia,{'pelvisWidth':pelvisWidth},body)
    def set_markers (self,sacrum, asisR, asisL):
        Segment.set_markers(self,sacrum, asisR, asisL)
    def set_joint_center(self):
        coefU=self.anthropometric['pelvisWidth']*0.598
        coefV=self.anthropometric['pelvisWidth']*0.344
        coefW=-self.anthropometric['pelvisWidth']*0.29
        hip_r=JointCenter('hip_r',self.markers[2],self.markers[1],self.markers[0],order=[2,3,1],coefU=coefU,coefV=-coefV,coefW=coefW,sign2=-1)
        hip_l=JointCenter('hip_l',self.markers[2],self.markers[1],self.markers[0],order=[2,3,1],coefU=coefU,coefV=coefV,coefW=coefW,sign2=-1) 
        Segment.set_joint_center(self,hip_r,hip_l)
    def calculate_local_system(self):
        k=Vector.unitary_vector(Vector.get_vector_from_two_points(self.markers[2].position,self.markers[1].position))
        i=Vector.unitary_vector(Vector.get_vector_from_three_points(self.markers[1].position,self.markers[2].position,self.markers[0].position))
        j=Vector.perpendicular_vector(k,i)
        self.localSystem={'i':i,'j':j,'k':k}
        self.jointCenter[0].set_coordinate_system(k,1)
        self.jointCenter[1].set_coordinate_system(k,1)

class Thigh(Segment):
    def __init__(self,body:Body,side='rigth'):
        self.__side=side
        if side=='rigth':
            self.__sideSign=1
        elif side=='left':
            self.__sideSign=-1
        Segment.__init__(self,'Thigh',Segment.set_mass(self,-2.649,0.1463,0.0137,body=body),Segment.set_inertia(self,-13.5,11.3 ,-2.28,-3557, 31.7 ,18.61,-3690,32.02,19.24 ,body=body),{},body)
    def set_markers (self,femoralWand):
        Segment.set_markers(self,femoralWand)
    def set_joint_center(self,hipJointCenter:JointCenter,kneeJointCenter:JointCenter):
        Segment.set_joint_center(self,hipJointCenter,kneeJointCenter)
    def calculate_local_system(self):
        i=Vector.unitary_vector(Vector.get_vector_from_two_points(self.jointCenter[0].position,self.jointCenter[1].position))
        if self.__sideSign==1:
            j=Vector.unitary_vector(Vector.get_vector_from_three_points(self.markers[0].position,self.jointCenter[1].position,self.jointCenter[0].position))
        elif self.__sideSign==-1:
            j=Vector.unitary_vector(Vector.get_vector_from_three_points(self.jointCenter[1].position,self.markers[0].position,self.jointCenter[0].position))
        k=Vector.perpendicular_vector(i,j)
        self.localSystem={'i':i,'j':j,'k':k}
        self.jointCenter[0].set_coordinate_system(i,3)
        self.jointCenter[1].set_coordinate_system(k,1)

class Calf(Segment):
    def __init__(self,body:Body,kneeDiameter:float,side='rigth'): #kneeDiameter in meters
        self.__side=side
        if side=='rigth':
            self.__sideSign=1
        elif side=='left':
            self.__sideSign=-1
        Segment.__init__(self,'Calf',Segment.set_mass(self,-1.592,0.0362,0.0121,body=body),Segment.set_inertia(self,-70.5, 1.134, 0.3,-1105 ,4.59 ,6.63,-1152,4.594,6.815,body=body),{'kneeDiameter':kneeDiameter},body)
    def set_markers (self,lateralFemoralEpicondyle, lateralMalleolus, tibialWand):
        Segment.set_markers(self,lateralFemoralEpicondyle, lateralMalleolus, tibialWand)
    def set_joint_center(self,ankleJointCenter:JointCenter):
        coefU=0
        coefV=0
        coefW=self.anthropometric['kneeDiameter']*0.5
        knee=JointCenter('knee_'+self.__side[0],self.markers[1],self.markers[0],self.markers[2],order=[2,1,3],coefU=coefU,coefV=coefV,coefW=self.__sideSign*coefW,sign2=self.__sideSign,origin=2)
        Segment.set_joint_center(self,knee,ankleJointCenter)
    def calculate_local_system(self):
        i=Vector.unitary_vector(Vector.get_vector_from_two_points(self.jointCenter[0].position,self.jointCenter[1].position))
        if self.__sideSign==1:
            j=Vector.unitary_vector(Vector.get_vector_from_three_points(self.markers[0].position,self.jointCenter[1].position,self.jointCenter[0].position))
        elif self.__sideSign==-1:
            j=Vector.unitary_vector(Vector.get_vector_from_three_points(self.jointCenter[1].position,self.markers[0].position,self.jointCenter[0].position))
        k=Vector.perpendicular_vector(i,j)
        self.localSystem={'i':i,'j':j,'k':k}
        self.jointCenter[0].set_coordinate_system(i,3)
        self.jointCenter[1].set_coordinate_system(k,1)

class Foot(Segment):
    def __init__(self,body:Body,footLength:float,footWidth:float,malleolusHigh:float,malleolusWidth:float,side='rigth'):
        self.__side=side
        if side=='rigth':
            self.__sideSign=1
        elif side=='left':
            self.__sideSign=-1
        Segment.__init__(self,'Foot',Segment.set_mass(self,-0.829,0.0077,0.0073,body=body),Segment.set_inertia(self,-15.48,0.144,0.088,-100,0.480,0.626,-97.09,0.414,0.614,body=body),{'footLength':footLength,'footWidth':footWidth,'malleolusHigh':malleolusHigh,'malleolusWidth':malleolusWidth},body)
    def set_markers (self,metatarsal,heel,lateralMalleolus):
        Segment.set_markers(self,metatarsal,heel,lateralMalleolus)
    def set_joint_center(self):
        
        coefUAnkle=self.anthropometric['footLength']*0.016
        coefVAnkle=self.anthropometric['malleolusHigh']*0.392
        coefWAnkle=self.__sideSign*self.anthropometric['malleolusWidth']*0.478

        coefUToe=self.anthropometric['footLength']*0.742
        coefVToe=self.anthropometric['malleolusHigh']*1.074
        coefWToe=-self.__sideSign*self.anthropometric['footWidth']*0.187

        ankle=JointCenter('ankle_'+self.__side[0],self.markers[0],self.markers[1],self.markers[2],order=[1,3,2],coefU=coefUAnkle,coefV=coefVAnkle,coefW=coefWAnkle)
        toe=JointCenter('toe_'+self.__side[0],self.markers[0],self.markers[1],self.markers[2],order=[1,3,2],coefU=coefUToe,coefV=coefVToe,coefW=coefWToe)
        Segment.set_joint_center(self,ankle,toe)

    def calculate_local_system(self):
        i=Vector.unitary_vector(Vector.get_vector_from_two_points(self.markers[1].position,self.jointCenter[1].position))
        k=Vector.unitary_vector(Vector.get_vector_from_three_points(self.jointCenter[0].position,self.jointCenter[1].position,self.markers[1].position))
        j=Vector.perpendicular_vector(k,i)
        self.localSystem={'i':i,'j':j,'k':k}    
        self.jointCenter[0].set_coordinate_system(i,3)
    




