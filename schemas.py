from typing import Literal
from pydantic import BaseModel,Field
class DirectoryRequest(BaseModel):dicom_directory:str=Field(min_length=1,max_length=500)
class AnalyseRequest(DirectoryRequest):threshold:float=Field(default=0.65,ge=0.05,le=0.99)
class ReviewRequest(BaseModel):decision:Literal["accept_for_research","reject","needs_correction"];reviewer:str=Field(min_length=2,max_length=120);comment:str=Field(default="",max_length=1000)
