import csv
import json


def csv_to_json(csv_file_path, json_file_path):
    # Abrir o arquivo CSV para leitura
    with open(csv_file_path, 'r') as csv_file:
        # Ler o conteúdo do CSV
        csv_data = csv.DictReader(csv_file)

        # Converter os dados do CSV para uma lista de dicionários
        data_list = []
        for row in csv_data:
            data_list.append(row)

    # Escrever os dados como JSON no arquivo de saída
    with open(json_file_path, 'w') as json_file:
        json.dump(data_list, json_file)


# Exemplo de uso:
csv_file_path = 'caminho/para/o/arquivo.csv'
json_file_path = 'caminho/para/o/arquivo.json'
csv_to_json(csv_file_path, json_file_path)
