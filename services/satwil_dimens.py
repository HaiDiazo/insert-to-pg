from config.pg_config import client as conn
from utils import generate
from loguru import logger


class DimensSatwil:
    def __init__(self, polres_ids: list, polda_id: str):
        self.polda_id = polda_id
        self.polres_ids = polres_ids
        self.tuple_datas = []

    def _generate_tuple(self):
        for data in self.polres_ids:
            tuple_data = (
                generate.hash_key(f"{data}-{self.polda_id}"),
                self.polda_id,
                data
            )
            self.tuple_datas.append(tuple_data)

    def insert_satwil(self):
        connect = conn.connect()
        cursor = connect.cursor()
        self._generate_tuple()

        args_val = ",".join(cursor.mogrify("""(
                %s,
                %s,
                %s
            )""", data).decode('utf-8') for data in self.tuple_datas)
        query = """
            INSERT INTO satwil_data_v2
            (
                satwil_id, 
                polda_id, 
                polres_id 
            ) VALUES """ + args_val
        cursor.execute(query)
        connect.commit()

        count = cursor.rowcount
        logger.info("Already insert satwil_data : {}", count)

        cursor.close()
        connect.close()
