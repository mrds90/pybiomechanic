import numpy as np
import pyc3dserver as c3d

itf = c3d.c3dserver(False)
ret = c3d.open_c3d(itf, "0037_Davis_MarchaDavis_Walking02C2020Cu2.c3d")
# For the information of header
dict_header = c3d.get_dict_header(itf)
# For the information of all groups
dict_groups = c3d.get_dict_groups(itf)
# For the information of all markers(points)
dict_markers = c3d.get_dict_markers(itf)
# For the information of all forces/moments
dict_forces = c3d.get_dict_forces(itf)
# For the information of all analogs(excluding or including forces/moments)
dict_analogs = c3d.get_dict_analogs(itf)

# c3d.get_video_times(itf)

# Close the C3D file from C3Dserver
ret = c3d.close_c3d(itf)

dict_markers['DATA']['POS']['sacrum']

dict_groups['EVENT']['TIMES']