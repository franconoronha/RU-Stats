import json

INPUT_PATH = 'data/alltime_data.json'

def main():
    data = []

    with open(INPUT_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if not data:
        print('Nenhum dado encontrado')
        return
    
    # Get last date
    if len(data) > 0:
        first_date = data[0]['data']
        last_date = data[-1]['data']
        print('Primeira data:', first_date)
        print('Última data:', last_date)

    print('Quantidade de dias:', len(data))
    
if __name__ == '__main__':
    main()