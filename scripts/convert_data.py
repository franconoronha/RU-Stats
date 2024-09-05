# Converter dados do formato antigo
# para o formato novo

# Formato antigo:
# [
#     {
#         "data": "01/01/2021",
#         "NOME": {
#             "composicao": "composicao",
#             "calorias": "calorias",
#             "porcao": "porcao"
#         },
#         ...
#     },
#     ...
# ]


# Formato novo
# data.json
# [
#     {
#         "data": "01/01/2021",
#         "items": [ id1, id2, id3 ]
#     },
#     ...   
# ]

# pratos_conhecidos.json

import json
import os
from datetime import datetime

INPUT_FILE = 'data/alltime_data.json'
OUTPUT_FILE = 'data/alltime_data_converted.json'
PRATOS_CONHECIDOS_FILE = 'data/pratos_conhecidos.json'

def main():
    data = []
    pratos_conhecidos = {}

    if os.path.exists(PRATOS_CONHECIDOS_FILE):
        with open(PRATOS_CONHECIDOS_FILE, 'r', encoding='utf-8') as f:
            pratos_conhecidos = json.load(f)

    last_id = max(pratos_conhecidos.keys()) if pratos_conhecidos else 0

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    new_data = []

    for d in data:
        new_d = {
            "data": d['data'],
            "items": []
        }
 
        for key in d:
            if key == 'data':
                continue


        new_data.append(new_d)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(new_data, f)

    with open(PRATOS_CONHECIDOS_FILE, 'w', encoding='utf-8') as f:
        json.dump(pratos_conhecidos, f, indent=4)


if __name__ == '__main__':
    main()