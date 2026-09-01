import numpy as np
from app.preprocess import normalise
def test_normalise_range():
 x=normalise(np.arange(100,dtype=np.float32).reshape(4,5,5));assert x.min()>=0 and x.max()<=1
