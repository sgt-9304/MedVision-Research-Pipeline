from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings,SettingsConfigDict
class Settings(BaseSettings):
 data_root:Path=Path("sample_data");output_root:Path=Path("outputs");model_mode:str="demo_threshold";model_path:Path|None=None
 device:str="auto";max_slices:int=1000;max_file_mb:int=50
 model_config=SettingsConfigDict(env_file=".env",extra="ignore")
@lru_cache
def settings():return Settings()
