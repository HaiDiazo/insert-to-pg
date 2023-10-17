from config.base import settings
import psycopg2


class PostgreConfig:
    def connect(self):
        conn = psycopg2.connect(database="gaiaocean",
                                host=settings.GAIAOCEAN_STAGING_AREA_HOST,
                                user=settings.GAIAOCEAN_STAGING_AREA_USER,
                                password=settings.GAIAOCEAN_STAGING_AREA_PASS,
                                port=settings.GAIAOCEAN_STAGING_AREA_PORT)
        return conn


client = PostgreConfig()
