from pathlib import Path
import pydicom,numpy as np
from pydicom.uid import generate_uid
PHI_TAGS=["PatientName","PatientID","PatientBirthDate","PatientAddress","InstitutionName","ReferringPhysicianName","AccessionNumber"]
def scan_privacy(files):
 findings=[]
 for p in files[:5]:
  ds=pydicom.dcmread(str(p),stop_before_pixels=True,force=True)
  for name in PHI_TAGS:
   value=getattr(ds,name,None)
   if value and str(value).strip() not in {"ANONYMOUS","SYNTHETIC","REMOVED"}:findings.append({"file":p.name,"attribute":name})
 return findings
def load_series(directory:Path,max_slices=1000,max_file_mb=50):
 files=sorted([p for p in directory.rglob("*") if p.is_file() and p.suffix.lower() in {".dcm",""}])
 if not files:raise ValueError("No DICOM files found")
 if len(files)>max_slices:raise ValueError("Slice limit exceeded")
 datasets=[]
 for p in files:
  if p.stat().st_size>max_file_mb*1024*1024:raise ValueError(f"File too large: {p.name}")
  ds=pydicom.dcmread(str(p),force=True)
  if not hasattr(ds,"PixelData"):continue
  datasets.append((p,ds))
 if not datasets:raise ValueError("No DICOM pixel data found")
 datasets.sort(key=lambda x:float(getattr(x[1],"ImagePositionPatient",[0,0,getattr(x[1],"InstanceNumber",0)])[2]))
 arrays=[]
 for _,ds in datasets:
  a=ds.pixel_array.astype(np.float32);slope=float(getattr(ds,"RescaleSlope",1));inter=float(getattr(ds,"RescaleIntercept",0));arrays.append(a*slope+inter)
 volume=np.stack(arrays)
 first=datasets[0][1];spacing=getattr(first,"PixelSpacing",[1.0,1.0]);thickness=float(getattr(first,"SpacingBetweenSlices",getattr(first,"SliceThickness",1.0)))
 return volume,(thickness,float(spacing[0]),float(spacing[1])),[p for p,_ in datasets]
def deidentify_copy(source:Path,target:Path):
 target.mkdir(parents=True,exist_ok=True)
 for p in source.rglob("*"):
  if not p.is_file():continue
  ds=pydicom.dcmread(str(p),force=True)
  for name in PHI_TAGS:
   if hasattr(ds,name):setattr(ds,name,"ANONYMOUS")
  ds.PatientIdentityRemoved="YES";ds.SOPInstanceUID=generate_uid();ds.SeriesInstanceUID=generate_uid();ds.StudyInstanceUID=generate_uid();ds.save_as(str(target/(p.name or "image.dcm")))
