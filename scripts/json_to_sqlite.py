import sqlite3
import json
from datetime import datetime

def main():
    con = sqlite3.connect('data/data.db')
    cur = con.cursor()
    create_db(cur)

    all_data = None
    with open('data/alltime_data.json', 'r', encoding='utf-8') as f:
        all_data = json.load(f)
    if all_data and hasattr(all_data, '__iter__'):
        for day in all_data:
            date = datetime.strptime(day['data'], '%d/%m/%Y').strftime('%Y-%m-%d')
            test_day = cur.execute("SELECT id FROM cardapio WHERE data = ?", (date,)).fetchone()
            if test_day:
                print('Day already exists')
                continue

            keys = list(day.keys())
            proteina_animal_key = keys[4]
            proteina_vegetal_key = keys[5]
            acompanhamento_key = keys[6]
            
            proteina_animal = insert_prato(cur, day[proteina_animal_key], day['data'], proteina_animal_key)
            proteina_vegetal = insert_prato(cur, day[proteina_vegetal_key], day['data'], proteina_vegetal_key)
            acompanhamento = insert_prato(cur, day[acompanhamento_key], day['data'], acompanhamento_key)

            arroz_branco = insert_prato(cur, day['ARROZ BRANCO'], day['data'], 'ARROZ BRANCO')
            arroz_integral = insert_prato(cur, day['ARROZ INTEGRAL'], day['data'], 'ARROZ INTEGRAL')
            feijao = insert_prato(cur, day['FEIJÃO PRETO'], day['data'], 'FEIJAO PRETO')
            salada_crua = insert_prato(cur, day['SALADA CRUA'], day['data'], 'SALADA CRUA')
            salada_cozida = insert_prato(cur, day['SALADA COZIDA'], day['data'], 'SALADA COZIDA')
            salada_folhosa = insert_prato(cur, day['SALADA FOLHOSA'], day['data'], 'SALADA FOLHOSA')
            fruta = insert_prato(cur, day['FRUTA'], day['data'], 'FRUTA')
            cur.execute("INSERT INTO cardapio (data, arroz_branco, arroz_integral, feijao, proteina_animal, proteina_vegetal, acompanhamento, salada_crua, salada_cozida, salada_folhosa, fruta) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (day['data'], arroz_branco, arroz_integral, feijao, proteina_animal, proteina_vegetal, acompanhamento, salada_crua, salada_cozida, salada_folhosa, fruta))
    con.commit()
    cur.close()


def insert_prato(cur, prato, date, name):
    cur.execute("SELECT * FROM prato WHERE nome = ?", (name,))
    row = cur.fetchone()
    if row:
        #row = (0:id,1:nome,2:composicao,3:calorias,4:porcao)
        if prato['composicao'] != row[2]:
            cur.execute("INSERT INTO alteracao (cardapio_id, prato_id, tipo, from_value, to_value) VALUES (?, ?, ?, ?, ?)", (date, row[0], 'composicao', row[2], prato['composicao']))
            cur.execute("UPDATE prato SET composicao = ? WHERE id = ?", (prato['composicao'], row[0]))
        if int(prato['calorias']) != row[3]:
            cur.execute("INSERT INTO alteracao (cardapio_id, prato_id, tipo, from_value, to_value) VALUES (?, ?, ?, ?, ?)", (date, row[0], 'calorias', row[3], int(prato['calorias'])))
            cur.execute("UPDATE prato SET calorias = ? WHERE id = ?", (prato['calorias'], row[0]))
        if prato['porcao'] != row[4]:
            cur.execute("INSERT INTO alteracao (cardapio_id, prato_id, tipo, from_value, to_value) VALUES (?, ?, ?, ?, ?)", (date, row[0], 'porcao', row[4], prato['porcao']))
            cur.execute("UPDATE prato SET porcao = ? WHERE id = ?", (prato['porcao'], row[0]))
        return row[0]
    cur.execute("INSERT INTO prato (nome, composicao, calorias, porcao) VALUES (?, ?, ?, ?)", (name, prato['composicao'], int(prato['calorias']), prato['porcao']))
    return cur.lastrowid


def create_db(cur):
    cur.execute("""CREATE TABLE IF NOT EXISTS cardapio (
        id INTEGER PRIMARY KEY, 
        data DATE,
        arroz_branco INTEGER,
        arroz_integral INTEGER,
        feijao INTEGER,
        proteina_animal INTEGER,
        proteina_vegetal INTEGER,
        acompanhamento INTEGER,
        salada_crua INTEGER,
        salada_cozida INTEGER,
        salada_folhosa INTEGER,
        fruta INTEGER,
        FOREIGN KEY (arroz_branco) REFERENCES prato(id),
        FOREIGN KEY (arroz_integral) REFERENCES prato(id),
        FOREIGN KEY (feijao) REFERENCES prato(id),
        FOREIGN KEY (proteina_animal) REFERENCES prato(id),
        FOREIGN KEY (proteina_vegetal) REFERENCES prato(id),
        FOREIGN KEY (acompanhamento) REFERENCES prato(id),
        FOREIGN KEY (salada_crua) REFERENCES prato(id),
        FOREIGN KEY (salada_cozida) REFERENCES prato(id),
        FOREIGN KEY (salada_folhosa) REFERENCES prato(id),
        FOREIGN KEY (fruta) REFERENCES prato(id)
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS prato (
        id INTEGER PRIMARY KEY, 
        nome TEXT,
        composicao TEXT,
        calorias INTEGER,
        porcao TEXT
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS alteracao (
        id INTEGER PRIMARY KEY,
        date DATE,
        prato_id INTEGER,
        tipo TEXT,
        from_value TEXT,
        to_value TEXT,
        FOREIGN KEY (prato_id) REFERENCES prato(id)
    )""")

if __name__ == '__main__':
    main()