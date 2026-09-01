import numpy as np
from app.measurements import measure
def test_measurement():
 mask=np.zeros((2,2,2),dtype=np.uint8);mask[0]=1;conf=np.ones_like(mask,dtype=float)*.8;r=measure(mask,conf,(2,1,1));assert r["voxel_count"]==4;assert r["volume_mm3"]==8
