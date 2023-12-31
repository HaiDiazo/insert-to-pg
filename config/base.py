from pydantic import BaseSettings


class Settings(BaseSettings):
    GAIAOCEAN_STAGING_AREA_HOST: str
    GAIAOCEAN_STAGING_AREA_PORT: int
    GAIAOCEAN_STAGING_AREA_USER: str
    GAIAOCEAN_STAGING_AREA_PASS: str

    ES_GIS_HOST: str
    ES_GIS_INDEX_PROVINCE: str

    class Config:
        env_file = '.env'


settings = Settings()
