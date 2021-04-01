from biomechanics import *
import pyc3dserver as c3d
import numpy as np
from matplotlib import pyplot

itf = c3d.c3dserver(False)
ret = c3d.open_c3d(itf, "0037_Davis_MarchaDavis_Walking02C2020Cu2.c3d")
dict_markers = c3d.get_dict_markers(itf)
dict_groups = c3d.get_dict_groups(itf)
ret = c3d.close_c3d(itf)
body=Body(float(dict_groups['Antropometria']['PESO'])  ,float(dict_groups['Antropometria']['ALTURA']))




#Pelvis
pelvis=Pelvis(body,0.01*float(dict_groups['Antropometria']['LONGITUD_ASIS']))
sacrum=Marker(dict_markers['DATA']['POS']['sacrum'],'sacrum',340)
sacrum.filter()
rAsis=Marker(dict_markers['DATA']['POS']['r asis'],'r asis',340)
rAsis.filter()
lAsis=Marker(dict_markers['DATA']['POS']['l asis'],'l asis',340)
lAsis.filter()
pelvis.set_markers(sacrum,rAsis,lAsis)
pelvis.set_joint_center()
pelvis.calculate_local_system()

# pyplot.plot(range(pelvis.jointCenter[0].position.shape[0]),pelvis.jointCenter[1].position) 
# pyplot.plot(range(pelvis.localSystem['i'].orientation.shape[0]),pelvis.localSystem['i'].orientation) 

# pyplot.show()

#Foot
    #rigth
footR=Foot(body,0.01*dict_groups['Antropometria']['LONGITUD_PIE_DERECHO'],0.01*dict_groups['Antropometria']['ANCHO_PIE_DERECHO'],0.01*dict_groups['Antropometria']['ALTURA_MALEOLOS_DERECHO'],0.01*dict_groups['Antropometria']['ANCHO_MALEOLOS_DERECHO'],side='rigth')
rMet=Marker(dict_markers['DATA']['POS']['r met'],'r metatarsal',340)
rMet.filter()
rHeel=Marker(dict_markers['DATA']['POS']['r heel'],'r heel',340)
rHeel.filter()
rMal=Marker(dict_markers['DATA']['POS']['r mall'],'r lateralMalleolus',340)
rMal.filter()
footR.set_markers(rMet,rHeel,rMal)
footR.set_joint_center()
footR.calculate_local_system()


# pyplot.plot(range(footR.jointCenter[0].position.shape[0]),footR.jointCenter[1].position) 
# pyplot.plot(range(footR.localSystem['i'].orientation.shape[0]),footR.localSystem['i'].orientation) 
# pyplot.plot(range(footR.jointCenter[0].coordinateSystem['e2'].orientation.shape[0]),footR.jointCenter[0].coordinateSystem['e2'].orientation) 
# pyplot.show()

    #left
footL=Foot(body,0.01*dict_groups['Antropometria']['LONGITUD_PIE_IZQUIERDO'],0.01*dict_groups['Antropometria']['ANCHO_PIE_IZQUIERDO'],0.01*dict_groups['Antropometria']['ALTURA_MALEOLOS_IZQUIERDO'],0.01*dict_groups['Antropometria']['ANCHO_MALEOLOS_IZQUIERDO'],side='left')
lMet=Marker(dict_markers['DATA']['POS']['l met'],'l metatarsal',340)
lMet.filter()
lHeel=Marker(dict_markers['DATA']['POS']['l heel'],'l heel',340)
lHeel.filter()
lMal=Marker(dict_markers['DATA']['POS']['l mall'],'l lateralMalleolus',340)
lMal.filter()
footL.set_markers(lMet,lHeel,lMal)
footL.set_joint_center()
footL.calculate_local_system()


# pyplot.plot(range(footL.jointCenter[0].position.shape[0]),footL.jointCenter[1].position) 
# pyplot.plot(range(footL.localSystem['i'].orientation.shape[0]),footL.localSystem['i'].orientation) 
# pyplot.show()

#Calf
    #rigth
rLFE=Marker(dict_markers['DATA']['POS']['r knee 1'],'r lateral femoral epicondyle',340)
rLFE.filter()
rLM=Marker(dict_markers['DATA']['POS']['r mall'],'r lateralMalleolus',340)
rLM.filter()
rTW=Marker(dict_markers['DATA']['POS']['r bar 2'],'r tibial wand',340)
rTW.filter()
calfR=Calf(body,float(0.01*dict_groups['Antropometria']['DIAMETRO_RODILLA_DERECHA']),side='rigth')
calfR.set_markers(rLFE,rLM,rTW)
calfR.set_joint_center(footR.jointCenter[0])
calfR.calculate_local_system()


# pyplot.plot(range(calfR.jointCenter[0].position.shape[0]),calfR.jointCenter[0].position) 
# pyplot.plot(range(calfR.localSystem['i'].orientation.shape[0]),calfR.localSystem['i'].orientation) 
# pyplot.show()


    #left
lLFE=Marker(dict_markers['DATA']['POS']['l knee 1'],'l lateral femoral epicondyle',340)
lLFE.filter()
lLM=Marker(dict_markers['DATA']['POS']['l mall'],'l lateralMalleolus',340)
lLM.filter()
lTW=Marker(dict_markers['DATA']['POS']['l bar 2'],'l tibial wand',340)
lTW.filter()
calfL=Calf(body,float(0.01*dict_groups['Antropometria']['DIAMETRO_RODILLA_IZQUIERDA']),side='left')
calfL.set_markers(lLFE,lLM,lTW)
calfL.set_joint_center(footL.jointCenter[0])
calfL.calculate_local_system()

# pyplot.plot(range(calfL.jointCenter[0].position.shape[0]),calfL.jointCenter[0].position) 
# pyplot.plot(range(calfL.localSystem['i'].orientation.shape[0]),calfL.localSystem['i'].orientation) 
# pyplot.show()

#Thigh
    #rigth
rFW=Marker(dict_markers['DATA']['POS']['r bar 1'],'r femoral wand',340)
rFW.filter()
thighR=Thigh(body,side='rigth')
thighR.set_markers(rFW)
thighR.set_joint_center(pelvis.jointCenter[0],calfR.jointCenter[0])
thighR.calculate_local_system()

# pyplot.plot(range(thighR.localSystem['i'].orientation.shape[0]),thighR.localSystem['i'].orientation) 
# pyplot.show()

    #left
lFW=Marker(dict_markers['DATA']['POS']['l bar 1'],'l femoral wand',340)
lFW.filter()
thighL=Thigh(body,side='left')
thighL.set_markers(lFW)
thighL.set_joint_center(pelvis.jointCenter[1],calfL.jointCenter[0])
thighL.calculate_local_system()

# pyplot.plot(range(thighL.localSystem['i'].orientation.shape[0]),thighL.localSystem['i'].orientation) 
# pyplot.show()

# pyplot.plot(range(thighL.jointCenter[1].coordinateSystem['e2'].orientation.shape[0]),thighL.jointCenter[1].coordinateSystem['e2'].orientation)

thighR.jointCenter[0].angles=Angle(pelvis,thighR,thighR.jointCenter[0])
thighR.jointCenter[0].angles.alpha=thighR.jointCenter[0].angles.get_alpha()

thighL.jointCenter[0].angles=Angle(pelvis,thighL,thighL.jointCenter[0])
thighL.jointCenter[0].angles.alpha=thighL.jointCenter[0].angles.get_alpha()

calfR.jointCenter[0].angles=Angle(thighR,calfR,calfR.jointCenter[0])
calfR.jointCenter[0].angles.alpha=calfR.jointCenter[0].angles.get_alpha()

calfL.jointCenter[0].angles=Angle(thighL,calfL,calfL.jointCenter[0])
calfL.jointCenter[0].angles.alpha=calfL.jointCenter[0].angles.get_alpha()

footR.jointCenter[0].angles=Angle(calfR,footR,footR.jointCenter[0])
footR.jointCenter[0].angles.alpha=footR.jointCenter[0].angles.get_alpha()

footL.jointCenter[0].angles=Angle(calfL,footL,footL.jointCenter[0])
footL.jointCenter[0].angles.alpha=footL.jointCenter[0].angles.get_alpha()

# pyplot.plot(range(thighR.jointCenter[0].angles.alpha.shape[0]),thighR.jointCenter[0].angles.alpha) 
# pyplot.show()
