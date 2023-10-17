import json
import os

from services.polda_dimens import DimensPolda
from services.polres_dimens import DimensPolres
from services.satwil_dimens import DimensSatwil


def main():
    path_folder = "lib/polres/"
    for name_file in os.listdir(path_folder):
        with open(f"{path_folder}{name_file}", 'r') as file_json:
            datas = json.load(file_json)
            print(datas['polda'])
            polda = DimensPolda(data=datas['polda'])
            polda.insert_polda()

            polres = DimensPolres(datas=datas['polres'], polda_id=polda.get_id_polda())
            polres.insert_polres()

            satwil = DimensSatwil(polres_ids=polres.get_ids_polres(), polda_id=polda.get_id_polda())
            satwil.insert_satwil()


if __name__ == "__main__":
    main()
