from pydantic import BaseModel
import yaml


class Config(BaseModel):
    api_key: str
    bing_key: str


_config = yaml.safe_load(open("config.yml"))
config = Config(**_config)
