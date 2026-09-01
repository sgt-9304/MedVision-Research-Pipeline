import numpy as np
def measure(mask,confidence,spacing):
 voxels=int(mask.sum());volume=float(voxels*np.prod(spacing));mean=float(confidence[mask>0].mean()) if voxels else 0.0
 return {"voxel_count":voxels,"volume_mm3":round(volume,2),"mean_confidence":round(mean,4)}
