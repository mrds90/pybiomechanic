import numpy as np
# from .position3d import Point3D

class Vector:
    def __init__(self,x=0,y=0,z=0):
        self.__orientatation=np.array([x,y,z])
        self.__orientatation=self.__orientatation.transpose()
        self.__module=Vector.module(self)
    @property
    def orientatation(self):
        return self.__orientatation
    @property
    def module(self):
        return self.__module
    @classmethod
    def new_vector_from_np_array(cls,vector:np.array):
        try:
            if vector.shape[0]==3:
                return cls(vector[0,:],vector[1,:],vector[2,:])
            elif vector.shape[1]==3:
                return cls(vector[:,0],vector[:,1],vector[:,2])
            else:
                raise ValueError

        except ValueError:
            print ('ERROR: wrong type or shape')
            
    @classmethod
    def get_vector_from_two_points(cls,head,tail):
        try:
            if (head.shape[0]==3 and tail.shape[0]==3) or (head.shape[1]==3 and tail.shape[1]==3):
                vector=head-tail
                return Vector.new_vector_from_np_array(vector)
            else:
                raise ValueError
        except ValueError:
            print('ERROR: wrong type or shape')
    @classmethod
    def get_vector_from_three_points(cls,head1,head2,tail):
        try:
            if ((head1.shape[0]==3 and head2.shape[0]==3 and tail.shape[0]==3) or (head1.shape[1]==3 and head2.shape[1]==3 and tail.shape[1]==3)) and head1.shape==head2.shape==tail.shape :
                vector=cross(head1-tail,head2-tail)
                return Vector.new_vector_from_np_array(vector)
            else:
                raise ValueError
        except ValueError:
            print('ERROR: wrong type or shape')
    @classmethod
    def module(cls,vector):
        if vector.orientatation.shape[0]==3:
            return np.sqrt((vector.orientatation*vector.orientatation).sum(axis=0))
        elif vector.orientatation.shape[1]==3:
            return np.sqrt((vector.orientatation*vector.orientatation).sum(axis=1))
    @classmethod
    def unitary_vector(cls,vector):
        module=cls.module(vector) #get module of the vector
        # print('modulo' , module)
        # print('vector', vector.orientatation)
        versorOrientation=np.divide(vector.orientatation,np.transpose([module,module,module])) # wise element division with moudule
        return Vector.new_vector_from_np_array(versorOrientation)
    @classmethod
    def perpendicular_vector(cls,vector1,vector2,sign=1):
        vector=None
        if vector1.orientatation.shape[0]==3 and vector2.orientatation.shape[0]==3:
            vector=np.cross(vector1.orientatation,vector2.orientatation,axis=0)
        elif vector1.orientatation.shape[1]==3 and vector2.orientatation.shape[1]==3:
            vector=np.cross(vector1.orientatation,vector2.orientatation,axis=1)
        if type(vector)==type(np.array([1,2])):
            return Vector.new_vector_from_np_array(vector)
       