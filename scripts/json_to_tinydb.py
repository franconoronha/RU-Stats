from tinydb import TinyDB, Query
from datetime import datetime
import json

id_alteracao = 1
id_prato = 1
id_cardapio = 1

import argparse

parser = argparse.ArgumentParser(description="Convert JSON data to TinyDB")
parser.add_argument("-v", "--verbose", action="store_true", help="Log to console")
parser.add_argument("-m", "--minify", action="store_true", help="Minify JSON output")
args = parser.parse_args()

MINIFY = args.minify
VERBOSE = args.verbose

columns = ["arroz_branco", "arroz_integral", "feijao", "proteina_animal", "acompanhamento", "proteina_vegetal", "salada_folhosa", "salada_crua", "salada_cozida", "fruta"]

DATA_COLUMN = 'd' if MINIFY else 'data'
ARROZ_BRANCO_COLUMN = 'ab' if MINIFY else 'arroz_branco'
ARROZ_INTEGRAL_COLUMN = 'ai' if MINIFY else 'arroz_integral'
FEIJAO_COLUMN = 'f' if MINIFY else 'feijao'
PROTEINA_ANIMAL_COLUMN = 'pa' if MINIFY else 'proteina_animal'
PROTEINA_VEGETAL_COLUMN = 'pv' if MINIFY else 'proteina_vegetal'
ACOMPANHAMENTO_COLUMN = 'ac' if MINIFY else 'acompanhamento'
SALADA_CRUA_COLUMN = 'sc' if MINIFY else 'salada_crua'
SALADA_COZIDA_COLUMN = 'sco' if MINIFY else 'salada_cozida'
SALADA_FOLHOSA_COLUMN = 'sf' if MINIFY else 'salada_folhosa'
FRUTA_COLUMN = 'fr' if MINIFY else 'fruta'

PORCAO_COLUMN = 'p' if MINIFY else 'porcao'
COMPOSICAO_COLUMN = 'c' if MINIFY else 'composicao'
CALORIAS_COLUMN = 'cal' if MINIFY else 'calorias'

def log(*args):
    msg = ' '.join([str(arg) for arg in args])
    if VERBOSE:
        print(msg)

def main():
    db_file = 'data/db' + ('_min' if MINIFY else '') + '.json'
    db = TinyDB(db_file)
    db.drop_table('alteracao')
    db.drop_table('prato')
    db.drop_table('cardapio')

    alteracao_table = db.table('alteracao')
    prato_table = db.table('prato')
    cardapio_table = db.table('cardapio')
    PratoQ = Query()
    CardapioQ = Query()

    all_data = None
    with open('data/alltime_data.json', 'r', encoding='utf-8') as f:
        all_data = json.load(f)

    if all_data and hasattr(all_data, '__iter__'):
        for day in all_data:
            date = datetime.strptime(day['data'], '%d/%m/%Y').strftime('%Y-%m-%d')
            test_day = cardapio_table.get(CardapioQ.data == date)
            if test_day:
                print('Day already exists')
                continue
            
            proteina_animal = insert_prato(alteracao_table, prato_table, PratoQ, day, 'proteina_animal')
            proteina_vegetal = insert_prato(alteracao_table, prato_table, PratoQ, day, 'proteina_vegetal')
            acompanhamento = insert_prato(alteracao_table, prato_table, PratoQ, day, 'acompanhamento')

            arroz_branco = insert_prato(alteracao_table, prato_table, PratoQ, day, 'arroz_branco')
            arroz_integral = insert_prato(alteracao_table, prato_table, PratoQ, day, 'arroz_integral')
            feijao = insert_prato(alteracao_table, prato_table, PratoQ, day, 'feijao')
            salada_crua = insert_prato(alteracao_table, prato_table, PratoQ, day, 'salada_crua')
            salada_cozida = insert_prato(alteracao_table, prato_table, PratoQ, day, 'salada_cozida')
            salada_folhosa = insert_prato(alteracao_table, prato_table, PratoQ, day, 'salada_folhosa')
            fruta = insert_prato(alteracao_table, prato_table, PratoQ, day, 'fruta')
            cardapio_table.insert({'data': day['data'],
                            'arroz_branco': arroz_branco, 
                            'arroz_integral': arroz_integral, 
                            'feijao': feijao,
                            'proteina_animal': proteina_animal,
                            'proteina_vegetal': proteina_vegetal, 
                            'acompanhamento': acompanhamento, 
                            'salada_crua': salada_crua, 
                            'salada_cozida': salada_cozida,
                            'salada_folhosa': salada_folhosa,
                            'fruta': fruta})
            
    pratos = prato_table.all()
    print('Pratos:', len(pratos))
    cardapios = cardapio_table.all()
    print('Cardapios:', len(cardapios))
    alteracoes = alteracao_table.all()
    print('Alteracoes:', len(alteracoes))

    db.close()


def insert_prato(alteracao_table, prato_table, PratoQ, day, key):
    global id_prato
    global id_alteracao

    date = day['data']
    prato = day[key]
    prato['id'] = id_prato
    prato['calorias'] = int(prato['calorias'])

    existing_prato = prato_table.search(PratoQ.nome == prato['nome'])

    log('Prato:', existing_prato)
    if existing_prato:
        prato_id = existing_prato[0]['id']
        if prato['composicao'] != existing_prato[0]['composicao']:
            log('Composição diferente')
            alteracao_table.insert({'id': id_alteracao, 'cardapio_id': date, 'prato_id': prato_id, 'tipo': 'composicao', 'from_value': existing_prato[0]['composicao'], 'to_value': prato['composicao']})
            prato_table.update({'composicao': prato['composicao']}, PratoQ.id == prato_id)
            id_alteracao += 1
        if int(prato['calorias']) != existing_prato[0]['calorias']:
            log('Calorias diferentes')
            alteracao_table.insert({'id': id_alteracao, 'cardapio_id': date, 'prato_id': prato_id, 'tipo': 'calorias', 'from_value': existing_prato[0]['calorias'], 'to_value': int(prato['calorias'])})
            prato_table.update({'calorias': int(prato['calorias'])}, PratoQ.id == prato_id)
            id_alteracao += 1
        if prato['porcao'] != existing_prato[0]['porcao']:
            log('Porção diferente')
            alteracao_table.insert({'id': id_alteracao, 'cardapio_id': date, 'prato_id': prato_id, 'tipo': 'porcao', 'from_value': existing_prato[0]['porcao'], 'to_value': prato['porcao']})
            prato_table.update({'porcao': prato['porcao']}, PratoQ.id == prato_id)
            id_alteracao += 1
        log('Prato já existe', prato_id)
        return prato_id
    else:
        log('Prato não existe')
        id_prato += 1
        prato_table.insert(prato)
        return prato['id']
    
    
if __name__ == '__main__':
    main()