from pydantic import BaseModel
from typing import List, Optional


class ToolSpec(BaseModel):
    name: str
    description: str
    entrypoint: str  # module:function
    input_schema: Optional[dict] = None


class PluginManifest(BaseModel):
    name: str
    version: str
    tools: List[ToolSpec]