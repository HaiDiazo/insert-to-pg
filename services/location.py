from config.pg_config import client as conn
from elasticsearch import Elasticsearch
from shapely.geometry import mapping, shape
from config.base import settings
from loguru import logger


def convert_shapely(geometry: dict) -> str:
    return f"{shape(geometry)}"


def query_province(province_name: str):
    return {
        'query': {
            "bool": {
                "should": [
                    {
                        "match_phrase": {
                            "other_name.keyword": province_name
                        }
                    },
                    {
                        "match_phrase": {
                            "province_name.keyword": province_name
                        }
                    }
                ]
            }
        }
    }


def province(province_name: str):
    if province_name is not None:
        with Elasticsearch(
                hosts=settings.ES_GIS_HOST
        ) as es:
            resp = es.search(body=query_province(province_name), index=settings.ES_GIS_INDEX_PROVINCE, size=1)
            for hit in resp['hits']['hits']:
                source = hit['_source']
                raw_geometry = source['geometry']
                clean_geometry = convert_shapely(raw_geometry)

                connection = conn.connect()
                cursor = connection.cursor()

                args_val = cursor.mogrify("(%s,%s,%s,%s,%s,%s,%s,%s,ST_SetSRID(ST_GeomFromText(%s), 4326))", (
                    hit['_id'],
                    source.get('province_code'),
                    source.get('domestic_code'),
                    source.get('province_name'),
                    source.get('domestic_name'),
                    source.get('adm_level'),
                    source.get('adm_type'),
                    source.get('bps_name'),
                    clean_geometry
                )).decode('utf-8')

                cursor.execute("""
                        INSERT INTO catalog_province
                        (province_id, 
                        province_code, 
                        domestic_code, 
                        province_name, 
                        domestic_name, 
                        adm_level, 
                        adm_type,
                        bps_name,
                        geometry)
                        VALUES""" + args_val)

                connection.commit()
                count = cursor.rowcount
                logger.info("Already insert province : {}", count)

                cursor.close()
                connection.close()
                return hit['_id']
    return None
