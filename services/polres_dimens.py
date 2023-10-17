from config.pg_config import client as conn
from loguru import logger


class DimensPolres:
    def __init__(self, datas: list, polda_id: str):
        self.polda_id = polda_id
        self.datas = datas
        self.tuple_datas = []
        self.polres_ids = []

    def get_ids_polres(self):
        return self.polres_ids

    def _generate_tuple(self):
        for data in self.datas:
            tuple_data = (
                data.get('id'),
                data.get('code_satpas'),
                data.get('name_polres'),
                data.get('address'),
                data.get('logo_polres'),
                data.get('phone_polres'),
                data.get('latitude'),
                data.get('longitude')
            )
            self.polres_ids.append(data.get('id'))
            self.tuple_datas.append(tuple_data)

    def insert_polres(self):
        connect = conn.connect()
        cursor = connect.cursor()
        self._generate_tuple()

        args_val = ",".join(cursor.mogrify("""(
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )""", data).decode('utf-8') for data in self.tuple_datas)
        query = """
            INSERT INTO polres_data_v2
            (
                polres_id, 
                code_satpas, 
                polres_name, 
                address, 
                polres_image, 
                polres_phone, 
                latitude,
                longitude
            ) VALUES """ + args_val
        cursor.execute(query)
        connect.commit()

        count = cursor.rowcount
        logger.info("Already insert polres_data : {}", count)

        cursor.close()
        connect.close()
