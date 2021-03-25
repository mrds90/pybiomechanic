import numpy as np
# from .position3d import Point3D

class Vector:
    def __init__(self,x=0,y=0,z=0):
        self.__orientation=np.array([x,y,z])
        self.__orientation=self.__orientation.transpose()
        self.__module=Vector.get_module(self)
    @property
    def orientation(self):
        return self.__orientation
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
    def get_module(cls,vector):
        if vector.orientation.shape[0]==3:
            return np.sqrt((vector.orientation*vector.orientation).sum(axis=0))
        elif vector.orientation.shape[1]==3:
            return np.sqrt((vector.orientation*vector.orientation).sum(axis=1))
    @classmethod
    def unitary_vector(cls,vector:np.array):
        module=cls.get_module(vector) #get module of the vector
        moduleMatrix=np.transpose([module,module,module])
        versorOrientation=np.divide(vector.orientation,moduleMatrix) # wise element division with moudule
        return Vector.new_vector_from_np_array(versorOrientation)
    @classmethod
    def perpendicular_vector(cls,vector1,vector2,sign=1):
        vector=None
        if vector1.orientation.shape[0]==3 and vector2.orientation.shape[0]==3:
            vector=sign*np.cross(vector1.orientation,vector2.orientation,axis=0)
        elif vector1.orientation.shape[1]==3 and vector2.orientation.shape[1]==3:
            vector=sign*np.cross(vector1.orientation,vector2.orientation,axis=1)
        if type(vector)==type(np.array([1,2])):
            return Vector.new_vector_from_np_array(vector)
       