import numpy as np

class Segment:
    def __init__(self,label:str,mass:float,inertia:np.array,anthropometric:dict):
        self.__label=label
        self.__mass=mass
        self.__inertia=inertia
        self.__anthropometric=anthropometric
        self.__jointCenter:JointCenter




