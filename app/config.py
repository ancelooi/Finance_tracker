from pydantic_settings import BaseSettings 

class Settings(BaseSettings):
    mongo_uri: str 

    class Config: 
        env_file = ".env" #Tells pydantic to load variables from .env

settings = Settings()
