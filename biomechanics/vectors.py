import numpy as np
import position3d as pos3d

class Vector:
    def __init__(self,x=0,y=0,z=0):
        self.__orientatation=np.array([[x],[y],[z]])
        self.__orientatation.transpose()
    @classmethod
    def get_vector_from_two_points(cls,head:pos3d.Point3D,tail:pos3d.Point3D):
        try:
            if (head.position.shape[0]==3 and tail.position.shape[0]==3) or (head.position.shape[1]==3 and tail.position.shape[1]==3):
                vector=head.position-tail.position
                if vector.shape[0]==3:
                    return Vector(vector[1,:],vector[2,:],vector[3,:])
                elif vector.shape[1]==3:
                    return Vector(vector[:,1],vector[:,2],vector[:,3])
            else:
                raise ValueError
        except ValueError:
            print('ERROR: wrong type or shape')