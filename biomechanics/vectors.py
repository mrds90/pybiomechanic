import numpy as np
import position3d as pos3d

class Vector:
    def __init__(self,x=0,y=0,z=0):
        self.__orientatation=np.array([[x],[y],[z]])
        self.__orientatation.transpose()
        self.__module=Vector.module(self)
    @property
    def orientatation(self):
        return self.__orientatation
    @property
    def module(self):
        return self.__module
    @classmethod
    def new_vector_from_np_array(cls,matrix:np.array):
        try:
            if vector.shape[0]==3:
                return cls(vector[1,:],vector[2,:],vector[3,:])
            elif vector.shape[1]==3:
                return cls(vector[:,1],vector[:,2],vector[:,3])
            else:
                raise ValueError

        except ValueError:
            print ('ERROR: wrong type or shape')
            
    @classmethod
    def get_vector_from_two_points(cls,head:pos3d.Point3D,tail:pos3d.Point3D):
        try:
            if (head.position.shape[0]==3 and tail.position.shape[0]==3) or (head.position.shape[1]==3 and tail.position.shape[1]==3):
                vector=head.position-tail.position
                return Vector.new_vector_from_np_array(vector)
            else:
                raise ValueError
        except ValueError:
            print('ERROR: wrong type or shape')
    @classmethod
    def get_vector_from_three_points(cls,head1:pos3d.Point3D,head2:pos3d.Point3D,tail:pos3d.Point3D):
        try:
            if ((head1.position.shape[0]==3 and head2.position.shape[0]==3 and tail.position.shape[0]==3) or (head1.position.shape[1]==3 and head2.position.shape[1]==3 and tail.position.shape[1]==3)) and head1.position.shape==head2.position.shape==tail.position.shape :
                vector=cross(head1.position-tail.position,head2.position-tail.position)
                return Vector.new_vector_from_np_array(vector)
            else:
                raise ValueError
        except ValueError:
            print('ERROR: wrong type or shape')
    @classmethod
    def module(cls,vector:Vector):
        if vector.orientatation.shape[0]==3:
            return np.sqrt((vector.orientatation*vector.orientatation).sum(axis=1))
        elif vector.orientatation.shape[1]==3:
            return np.sqrt((vector.orientatation*vector.orientatation).sum(axis=0))
    @classmethod
    def unitary_vector(cls,vector:Vector):
        module=module(vector) #get module of the vector
        versorOrientation=np.divide(vector.orientatation,np.transpose([module,module,module])) # wise element division with moudule
        return Vector.new_vector_from_np_array(versorOrientation)
    @classmethod
    def perpendicular_vector(cls,vector1:Vector,vector2:Vector,sign=1):
        vector=None
        if vector1.orientatation.shape[0]==3 and vector2.orientatation.shape[0]==3:
            vector=np.cross(vector1.orientatation,vector2.orientatation,axis=1)
        elif vector1.shape[1]==3 and vector2.shape[1]==3:
            vector=np.cross(vector1.orientatation,vector2.orientatation,axis=0)
        if vector !=None:
            return Vector.new_vector_from_np_array(vector)
       