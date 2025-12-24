import os
from crowdin_api import CrowdinClient

crowdin_client = CrowdinClient(
    token= os.environ.get("CROWDIN_TOKEN")
)
