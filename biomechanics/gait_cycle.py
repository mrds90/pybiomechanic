import numpy as np

class Gait ():
    def __init__(self,heelSrike1,heelSrike2,toeOff,fs,type='time'):
        if type=='time':
            self.__heelStrike=np.array([heelSrike1,heelSrike2])*fs
            self.__heelStrike=self.__heelStrike.astype(int)
            self.__toeOff=np.array([toeOff])*fs
            self.__toeOff=self.__toeOff.astype(int)
        elif type=='frame':
            self.__heelStrike=np.array([heelSrike1],[heelSrike2])
            self.__heelStrike=np.array([toeOff])
    def normalize (self,vector:np.array(object)):
        length=self.__heelStrike[1]-self.__heelStrike[0]
        x=range(100)
        xp=np.arange(0,100,100/length)
        print(len(xp))
        print(vector[self.__heelStrike[0]:self.__heelStrike[1]].shape[0])
        return np.interp(x,xp,vector[self.__heelStrike[0]:self.__heelStrike[1]])
    
    @property
    def hs1(self):
        return self.__heelStrike[0]
    @property
    def hs2(self):
        return self.__heelStrike[1]
    @property
    def toe(self):
        return self.__toeOff[0]

        