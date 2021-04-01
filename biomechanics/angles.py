import numpy as np
from biomechanics import *

class Angle():
    def __init__(self,proximalSegment:Segment,distalSegment:Segment,jointCenter:JointCenter):
        self.__proximalSegment=proximalSegment
        self.__distalSegment=distalSegment
        self.__jointCenter=jointCenter
    def get_alpha(self):
        if self.__jointCenter.label[0:len(self.__jointCenter.label)-2] == 'ankle':
            alpha = np.rad2deg(-np.arcsin((np.multiply(self.__jointCenter.coordinateSystem['e2'].orientation,self.__proximalSegment.localSystem['j'].orientation)).sum(axis=1))) #alpha in deg
        elif self.__jointCenter.label[0:len(self.__jointCenter.label)-2] == 'knee':
            alpha = np.rad2deg(-np.arcsin((np.multiply(self.__jointCenter.coordinateSystem['e2'].orientation,self.__proximalSegment.localSystem['i'].orientation)).sum(axis=1))) #alpha in deg
        elif self.__jointCenter.label[0:len(self.__jointCenter.label)-2] == 'hip':
            alpha = np.rad2deg(np.arcsin((np.multiply(self.__jointCenter.coordinateSystem['e2'].orientation,self.__proximalSegment.localSystem['i'].orientation)).sum(axis=1))) #alpha in deg
        return alpha

        