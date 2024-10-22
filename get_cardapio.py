import time
import os
import argparse
import platform
import json
import logging
from datetime import datetime

from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

CLEAR_COMMAND = "clear"
if platform.system() == "Windows":
    CLEAR_COMMAND = "cls"

parser = argparse.ArgumentParser(prog="RUStats", description="Web scraping de cardápios da UFPel")
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())

parser.add_argument("--verbose", "-v", type=bool, default=False, help="Ativa o modo verbose")
parser.add_argument("--loading-time", "-l", type=int, default=5, help="Tempo de espera para carregar a página")

args = parser.parse_args()

URL = "https://cobalto.ufpel.edu.br/portal/cardapios/cardapioPublico"
TABELA_ID = "gridListaCardapios"
SELECTOR_ROWS = f"#{TABELA_ID} > tbody > tr:not(.jqgfirstrow)"
SELECTOR_CELLS = "td[role='gridcell']"

ALLTIME_OUTPUT_FILE_NAME = "data/alltime_data.json"
LAST_OUTPUT_FILE_NAME = "data/last_data.json"

def main():
    loading_time = args.loading_time
    log_level = logging.INFO if args.verbose else logging.ERROR
    logging.basicConfig(filename='rustats.log', level=log_level, encoding='utf-8')

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.page_load_strategy = 'none'

    driver = Chrome(options=options)
    driver.implicitly_wait(loading_time)

    driver.get(URL)
    print("Esperando 5 segundos para carregar a página...")

    time.sleep(loading_time)
    os.system(CLEAR_COMMAND)

    # TODO: CONSIDERAR element = wait.until(EC.presence_of_element_located((By.ID, "myElement")))
    # TODO: TRY/EXCEPT PARA TRATAR ERROS
    # TODO: CONSIDERAR FORMATO DOS DADOS
    rows = driver.find_elements(By.CSS_SELECTOR, SELECTOR_ROWS)

    if len(rows) == 0 or not rows:
        logger.error("Nenhuma linha encontrada")
        return
    
    logger.info(f"Encontradas {len(rows)} linhas")

    todays_date = datetime.now().strftime('%d/%m/%Y')

    alltime_data = []
    if os.path.exists(ALLTIME_OUTPUT_FILE_NAME):
        alltime_data_file = open(ALLTIME_OUTPUT_FILE_NAME, "r", encoding='utf-8')
        alltime_data = json.load(alltime_data_file)

    for data in alltime_data:
        if data["data"] == todays_date:
            logger.error("Já existe um registro para o dia de hoje")
            return 

    columns = ["arroz_branco", "arroz_integral", "feijao", "proteina_animal", "acompanhamento", "proteina_vegetal", "salada_folhosa", "salada_crua", "salada_cozida", "fruta"]
    day_data = {
        "data": todays_date,
    }

    cur = 0
    for i, row in enumerate(rows):
        cells = row.find_elements(By.CSS_SELECTOR, SELECTOR_CELLS)
        cells = [cell for cell in cells if cell.text]
        logger.info(f"Encontradas {len(cells)} células")
        if len(cells) != 4:
            logger.warning("Número de células diferente de 4")
            continue
        else:
            if cur >= len(columns):
                logger.warning("cur maior que len(columns)")
                break
            if columns[cur] in day_data:
                continue
            day_data[columns[cur]] = {
                "nome": cells[0].text,
                "composicao": cells[1].text,
                "calorias": cells[2].text,
                "porcao": cells[3].text
            }
            cur += 1

    alltime_data.append(day_data)

    print("Salvando dados...")
    with open(ALLTIME_OUTPUT_FILE_NAME, "w", encoding='utf-8') as f:
        json.dump(alltime_data, f, indent=4, ensure_ascii=False)
    
    with open(LAST_OUTPUT_FILE_NAME, "w", encoding='utf-8') as f:
        json.dump(day_data, f, indent=4, ensure_ascii=False)

def cell_content_validation(cell):
    if not cell.text:
        return False
    elif cell.text == "&nbsp;":
        return False
    
    return True

if __name__ == '__main__':
    main()