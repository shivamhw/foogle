from pydantic import BaseModel
from typing import Any, List, Optional

class Config(BaseModel):
    cred_path: str
    token_path: str
    mongo_uri: str
    tele_bot: str
    tele_group: str
    cf_worker_site: str

class AppConfig(BaseModel):
    group: Any
    bot: Any
    app: Any
    gd: Any
    search_handler: Any
    config: Any

class GdSearchResponse(BaseModel):
    parents: List
    size: str
    id: str
    name: str
    modifiedTime: str
    cf_download_link: Optional[str]
    gdrive_link: Optional[str]

class SeriesSearchRequest(BaseModel):
    series_name: str
    season_nm: int
    episode_nm: int