# Converter dados do formato antigo
# para o formato novo

import json
import os
from datetime import datetime

INPUT_FILE = 'data/alltime_data.json'
OUTPUT_FILE = 'data/alltime_data_converted.json'

def main():
    data = []

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    new_data = []
    columns = ["arroz_branco", "arroz_integral", "feijao", "proteina_animal", "acompanhamento", "proteina_vegetal", "salada_folhosa", "salada_crua", "salada_cozida", "fruta"]

    for d in data:
        day_data = {
            'data': d['data']
        }
        for i, key in enumerate(d.keys()):
            if key == 'data':
                continue

            day_data[columns[i - 1]] = {
                'nome': key,
                'composicao': d[key]['composicao'],
                'calorias': d[key]['calorias'],
                'porcao': d[key]['porcao']
            }

        new_data.append(day_data)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    main()