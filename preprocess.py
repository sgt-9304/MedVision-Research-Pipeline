import numpy as np
def normalise(volume):
 lo,hi=np.percentile(volume,[1,99]);scaled=np.clip((volume-lo)/(max(hi-lo,1e-6)),0,1);return scaled.astype(np.float32)
