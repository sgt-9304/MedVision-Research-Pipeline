from app.settings import settings
from app.security import safe_data_path
from app.dicom_io import load_series,scan_privacy
from app.preprocess import normalise
from app.inference import infer
from app.measurements import measure
from app.visualise import save_views
from app.store import save_result,audit
def analyse(directory,threshold):
 path=safe_data_path(directory);s=settings();volume,spacing,files=load_series(path,s.max_slices,s.max_file_mb);privacy=scan_privacy(files);norm=normalise(volume);mask,confidence,meta=infer(norm,threshold)
 data={"study":{"series_count":1,"slice_count":len(files),"shape":list(volume.shape),"spacing_mm":list(spacing),"privacy_findings":privacy},"inference":meta,"candidate_region":measure(mask,confidence,spacing)}
 rid,root=save_result(data);save_views(norm,mask,root/"overlay.png");audit("analysis.completed",{"result_id":rid,"privacy_findings":len(privacy)});return data|{"result_id":rid,"clinical_status":"not_reviewed","warning":"Model-generated research output. Not a diagnosis or treatment recommendation."}
