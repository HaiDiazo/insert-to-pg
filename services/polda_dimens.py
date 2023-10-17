from config.pg_config import client as conn
from loguru import logger
from services import location
from helpers import convert


class DimensPolda:
    def __init__(self, data: dict):
        self.polda_id = data['id']
        self.data = data
        self.tuple_data = None

    def get_id_polda(self):
        return self.polda_id

    def _generate_tuple(self):
        self.tuple_data = (
            self.data.get('id'),
            self.data.get('code_satpas'),
            self.data.get('name_polda'),
            self.data.get('address'),
            self.data.get('logo_polda'),
            self.data.get('phone_polda'),
            self.data.get('hotline'),
            self.data.get('website'),
            self.data.get('latitude'),
            self.data.get('longitude'),
            location.province(convert.file_shp_to_province(self.data.get('file_shp'))),
            self.data.get('facebook'),
            self.data.get('instagram'),
            self.data.get('twitter'),
            self.data.get('youtube')
        )

    def insert_polda(self):
        connect = conn.connect()
        cursor = connect.cursor()
        self._generate_tuple()

        args_val = cursor.mogrify("""(
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )""", self.tuple_data).decode('utf-8')

        query = """
            INSERT INTO polda_data_v2
            (
                polda_id, 
                code_satpas, 
                polda_name, 
                address, 
                polda_image, 
                phone_polda, 
                hotline, 
                website,
                latitude,
                longitude,
                province_id,
                facebook,
                instagram,
                twitter,
                youtube
            ) VALUES """ + args_val
        cursor.execute(query)
        connect.commit()

        count = cursor.rowcount
        logger.info("Already insert polda_data : {}", count)

        cursor.close()
        connect.close()
