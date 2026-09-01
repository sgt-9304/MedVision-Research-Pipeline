from pathlib import Path
from app.settings import settings
def safe_data_path(value:str)->Path:
 root=settings().data_root.resolve();candidate=Path(value).resolve()
 if root not in candidate.parents and candidate!=root:raise ValueError("Path must remain inside DATA_ROOT")
 return candidate
