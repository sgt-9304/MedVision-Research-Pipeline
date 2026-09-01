from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
def save_views(volume,mask,path:Path):
 path.parent.mkdir(parents=True,exist_ok=True);z,y,x=[s//2 for s in volume.shape]
 fig,axes=plt.subplots(1,3,figsize=(12,4));views=[(volume[z],mask[z],"Axial"),(volume[:,y,:],mask[:,y,:],"Coronal"),(volume[:,:,x],mask[:,:,x],"Sagittal")]
 for ax,(im,ms,title) in zip(axes,views):ax.imshow(im,cmap="gray");ax.imshow(np.ma.masked_where(ms==0,ms),cmap="autumn",alpha=.45);ax.set_title(title);ax.axis("off")
 fig.suptitle("Research segmentation overlay - not for diagnosis");fig.tight_layout();fig.savefig(path,dpi=150);plt.close(fig)
