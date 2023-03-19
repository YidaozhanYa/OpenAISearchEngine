from pydantic import BaseModel
import yaml


class Config(BaseModel):
    openai_api_key: str
    bing_api_key: str
    openai_language: str
    bing_language: str
    search_results_count: int
    save_chat_history: bool
    chat_history_filename: str


_config = yaml.safe_load(open("config.yml"))
config = Config(**_config)
