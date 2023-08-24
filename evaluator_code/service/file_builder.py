import json
import csv
import os

new_line = '\n'
tab = '\t'
two_tabs = '\t\t'
three_tabs = '\t\t\t'
four_tabs = '\t\t\t\t'


class FileBuilder:
    def __init__(self, problems, source_codes, name, path):
        self.problems = problems
        self.source_codes = source_codes
        self.name = name
        self.path = path

    def build(self):
        self.build_txt()
        self.build_csv()
        self.build_csv_with_solutions_which_need_attention()
        self.build_json()

    def build_txt(self):
        file_path = os.path.join(self.path, 'result.txt')

        with open(file_path, 'w', encoding='UTF-8') as output:
            for problem in self.problems:
                header_problem = '--------------- Resultados para o problema: `{0}`. --------------- {1}{2}'.format(problem, new_line, tab)
                body_problem = ''
                for code in self.source_codes:
                    if code.extract_problem_name() == problem:
                        if code.is_base_source_code():
                            header_problem += 'Resultado para a solução base:' + new_line + two_tabs
                            header_problem += code.cyclomatic_complexity_result_txt + new_line + two_tabs
                            header_problem += code.raw_metrics_result_txt + new_line + tab
                            header_problem += 'Resultado para as submissões dos alunos:' + new_line + two_tabs
                            continue
                        body_problem += 'Submissão: ' + code.extract_file_name() + new_line + three_tabs
                        body_problem += 'Complexidade ciclomática: ' + code.cyclomatic_complexity_result_txt + new_line + three_tabs
                        body_problem += code.raw_metrics_result_txt + new_line + two_tabs
                output.write(header_problem)
                output.write(body_problem)
                output.write(new_line)

    def build_csv(self):
        header = 'PROBLEM;SOLUTION;IS_TEACHER;CYCLOMATIC_COMPLEXITY;EXCEEDED LIMIT CC;LINES OF CODE;'\
                 'EXCEEDED LIMIT LOC;LOGICAL LINES OF CODE;EXCEEDED LIMIT LLOC;SOURCE LINES OF CODE;LIMIT SLOC;'\
                 'FINAL SCORE;\n'
        file_path = os.path.join(self.path, 'result.csv')

        with open(file_path, 'w', encoding='UTF-8') as output:
            output.write(header)
            for problem in self.problems:
                for code in self.source_codes:
                    if code.extract_problem_name() == problem:
                        if code.cyclomatic_complexity_result_csv != '':
                            output.write(code.cyclomatic_complexity_result_csv + code.raw_metrics_result_csv + '\n')

    def build_csv_with_solutions_which_need_attention(self):
        header = 'PROBLEM;SOLUTION;ATTENTION_TYPE;SCORE;\n'
        file_path = os.path.join(self.path, 'result_alert.csv')

        with open(file_path, 'w', encoding='UTF-8') as output:
            output.write(header)
            for problem in self.problems:
                for code in self.source_codes:
                    if code.extract_problem_name() == problem:
                        if code.need_attention:
                            line = problem + ';' + code.extract_file_name() + ';' + code.need_attention_type + ';' + str(code.score) + ';\n'
                            output.write(line)

    def build_json(self):
        data = []
        file_path_csv = os.path.join(self.path, 'result.csv')

        with open(file_path_csv, 'r') as csvfile:
            csvreader = csv.DictReader(csvfile, delimiter=';')  # Use o ponto-e-vírgula como delimitador
            for row in csvreader:
                # Montar o dicionário para o JSON
                json_entry = {
                    "PROBLEM": row["PROBLEM"],
                    "SOLUTION": row["SOLUTION"],
                    "IS_TEACHER": row["IS_TEACHER"],
                    "CYCLOMATIC_COMPLEXITY": row["CYCLOMATIC_COMPLEXITY"],
                    "EXCEEDED_LIMIT_CC": row["EXCEEDED LIMIT CC"],
                    "LINES OF CODE": row["LINES OF CODE"],
                    "EXCEEDED LIMIT LOC": row["EXCEEDED LIMIT LOC"],
                    "LOGICAL LINES OF CODE": row["LOGICAL LINES OF CODE"],
                    "EXCEEDED LIMIT LLOC": row["EXCEEDED LIMIT LLOC"],
                    "SOURCE LINES OF CODE": row["SOURCE LINES OF CODE"],
                    "LIMIT SLOC": row["LIMIT SLOC"],
                    "FINAL SCORE": row["FINAL SCORE"]
                }
                data.append(json_entry)

        file_path = os.path.join(self.path, self.name)

        with open(file_path, 'w', encoding='UTF-8') as jsonfile:
            json.dump(data, jsonfile, indent=4)

        print(f"CSV file converted to JSON file successfully.")
