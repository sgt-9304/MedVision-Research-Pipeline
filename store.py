import json
from pathlib import Path
from uuid import uuid4
from datetime import datetime,timezone
from app.settings import settings
def save_result(data):
 rid=str(uuid4());root=settings().output_root/rid;root.mkdir(parents=True,exist_ok=True);data.update({"result_id":rid,"clinical_status":"not_reviewed","created_at":datetime.now(timezone.utc).isoformat(),"warning":"Model-generated research output. Not a diagnosis or treatment recommendation."});(root/"result.json").write_text(json.dumps(data,indent=2));return rid,root
def get_result(rid):
 p=settings().output_root/rid/"result.json"
 if not p.exists():raise FileNotFoundError(rid)
 return json.loads(p.read_text())
def update_result(rid,data):
 p=settings().output_root/rid/"result.json";p.write_text(json.dumps(data,indent=2))
def audit(event,details):
 root=settings().output_root;root.mkdir(parents=True,exist_ok=True)
 with (root/"audit.jsonl").open("a") as f:f.write(json.dumps({"time":datetime.now(timezone.utc).isoformat(),"event":event,"details":details})+"\n")
