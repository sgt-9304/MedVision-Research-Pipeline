import json
from fastapi import FastAPI,HTTPException
from fastapi.responses import FileResponse
from app.schemas import DirectoryRequest,AnalyseRequest,ReviewRequest
from app.security import safe_data_path
from app.dicom_io import load_series,scan_privacy
from app.pipeline import analyse
from app.store import get_result,update_result,audit
from app.settings import settings
app=FastAPI(title="MedVision Research Pipeline",version="0.1.0",description="Research-only DICOM processing, segmentation, visualisation and human review. Not for diagnosis or treatment.")
@app.get("/health")
def health():return {"status":"ok","intended_use":"research_only"}
@app.post("/v1/dicom/validate")
def validate(req:DirectoryRequest):
 try:path=safe_data_path(req.dicom_directory);volume,spacing,files=load_series(path,settings().max_slices,settings().max_file_mb);return {"valid":True,"slice_count":len(files),"shape":list(volume.shape),"spacing_mm":spacing,"privacy_findings":scan_privacy(files),"warning":"Metadata scanning does not guarantee complete de-identification."}
 except Exception as e:raise HTTPException(400,str(e))
@app.post("/v1/studies/analyse")
def run(req:AnalyseRequest):
 try:return analyse(req.dicom_directory,req.threshold)
 except Exception as e:raise HTTPException(400,str(e))
@app.get("/v1/results/{rid}")
def result(rid:str):
 try:return get_result(rid)
 except FileNotFoundError:raise HTTPException(404,"Result not found")
@app.get("/v1/results/{rid}/visualisation")
def image(rid:str):
 p=settings().output_root/rid/"overlay.png"
 if not p.exists():raise HTTPException(404,"Visualisation not found")
 return FileResponse(p,media_type="image/png")
@app.post("/v1/reviews/{rid}")
def review(rid:str,req:ReviewRequest):
 try:data=get_result(rid)
 except FileNotFoundError:raise HTTPException(404,"Result not found")
 data["clinical_status"]=req.decision;data["review"]={"reviewer":req.reviewer,"comment":req.comment};update_result(rid,data);audit("review.recorded",{"result_id":rid,"decision":req.decision,"reviewer":req.reviewer});return {"result_id":rid,"status":req.decision}
@app.get("/v1/audit")
def audits():
 p=settings().output_root/"audit.jsonl"
 return [] if not p.exists() else [json.loads(x) for x in p.read_text().splitlines()[-100:]]
