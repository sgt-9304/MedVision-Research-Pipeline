import argparse
from pathlib import Path
import numpy as np,pydicom
from pydicom.dataset import Dataset,FileDataset
from pydicom.uid import ExplicitVRLittleEndian,CTImageStorage,generate_uid
def generate(output,slices=32,size=128):
 out=Path(output);out.mkdir(parents=True,exist_ok=True);study=generate_uid();series=generate_uid();yy,xx=np.mgrid[:size,:size]
 for i in range(slices):
  meta=Dataset();meta.MediaStorageSOPClassUID=CTImageStorage;meta.MediaStorageSOPInstanceUID=generate_uid();meta.TransferSyntaxUID=ExplicitVRLittleEndian
  ds=FileDataset(str(out/f"slice_{i:03}.dcm"),{},file_meta=meta,preamble=b"\0"*128);ds.SOPClassUID=CTImageStorage;ds.SOPInstanceUID=meta.MediaStorageSOPInstanceUID;ds.StudyInstanceUID=study;ds.SeriesInstanceUID=series;ds.PatientName="SYNTHETIC";ds.PatientID="SYNTHETIC";ds.PatientIdentityRemoved="YES";ds.Modality="CT";ds.Rows=size;ds.Columns=size;ds.InstanceNumber=i+1;ds.ImagePositionPatient=[0,0,i*2.5];ds.PixelSpacing=[1.0,1.0];ds.SliceThickness=2.5;ds.SamplesPerPixel=1;ds.PhotometricInterpretation="MONOCHROME2";ds.BitsAllocated=16;ds.BitsStored=16;ds.HighBit=15;ds.PixelRepresentation=1;ds.RescaleSlope=1;ds.RescaleIntercept=-1024
  base=np.full((size,size),500,dtype=np.int16);radius=9+int(3*np.sin(i/5));region=(xx-size*.62)**2+(yy-size*.48)**2<radius**2;base[region]=1300;noise=np.random.default_rng(i).normal(0,25,(size,size)).astype(np.int16);ds.PixelData=(base+noise).tobytes();ds.save_as(ds.filename)
 print({"output":str(out),"slices":slices,"note":"Synthetic data only"})
if __name__=="__main__":p=argparse.ArgumentParser();p.add_argument("--output",default="sample_data/dicom");a=p.parse_args();generate(a.output)
