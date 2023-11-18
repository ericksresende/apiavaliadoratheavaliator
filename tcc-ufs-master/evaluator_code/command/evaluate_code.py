import json
import os
import subprocess
import sys
sys.path.append("../")

from evaluator_code.service.cyclomatic_complexity import CyclomaticComplexity
from evaluator_code.service.raw_metrics import RawMetrics
from evaluator_code.model.source_code import SourceCode
from evaluator_code.service.compare_submissions import CompareSubmissions
from evaluator_code.service.file_builder import FileBuilder

ON = "on"


def main_flow():
    configs = load_configurations()

    path = configs['root_path']

    source_codes = create_source_codes_from_path(path, configs['initial_score'])

    # ------------ CYCLOMATIC COMPLEXITY -------------
    if configs['calculate_cyclomatic_complexity'] == ON:
        calculate_cyclomatic_complexity(path, source_codes)

    # ---------------- RAW METRICS ---------------------
    if configs['calculate_raw_metrics'] == ON:
        calculate_raw_metrics(path, source_codes)

    # ------------- COMPARE SUBMISSIONS -------------
    problems = compare_submissions(source_codes, configs)

    # -------------- FILE BUILDER ------------------
    FileBuilder(problems, source_codes, configs).build()

    # ---------------- PRINT RESULTS -------------------
    # for code in source_codes:
    #     code.print_attr()
    #     print('------------------------------------------\n')


def compare_submissions(source_codes, configs):
    source_codes_for_problem = extract_source_codes_for_problem(source_codes)
    for key in source_codes_for_problem.keys():
        source_codes = source_codes_for_problem[key]
        base_code = None

        for i in range(len(source_codes)):
            if source_codes[i].is_base_source_code():
                base_code = source_codes.pop(i)
                break

        comparator = CompareSubmissions(base_code, source_codes, configs)
        comparator.compare_cyclomatic_complexity()
        comparator.compare_raw_metrics()
        comparator.compare_submissions_which_need_attention()
    return source_codes_for_problem.keys()


def extract_source_codes_for_problem(source_codes):
    source_codes_for_problem = {}
    for code in source_codes:
        if code.extract_problem_name() not in source_codes_for_problem.keys():
            source_codes_for_problem[code.extract_problem_name()] = []
        source_codes_for_problem[code.extract_problem_name()].append(code)
    return source_codes_for_problem


def calculate_raw_metrics(path, source_codes):
    rm = RawMetrics(path, source_codes)
    rm.calculate_raw_metrics()


def calculate_cyclomatic_complexity(path, source_codes):
    # cc = CyclomaticComplexity(path, source_codes)
    # cc.calculate_complexity()
    modularize_and_calculate_cyclomatic_complexity_for_all_codes(source_codes)
    # calculates_the_cyclomatic_complexity_if_the_code_is_not_modularized(source_codes)


def modularize_and_calculate_cyclomatic_complexity_for_all_codes(source_codes):
    for code in source_codes:
        file_path = code.path.replace('.py', '__CC.py')

        new_file = open(file_path, 'w')
        def_found = False  # True when found a def statement in file
        hand_created_def = False  # True when a def is created automatically false in another case
        count_hand_created_def = 0  # Count how many times a def is created automatically
        for line in code.extract_content():
            if 'def' in line[0:3]:  # If the line starts with key word 'def'
                def_found = True
                hand_created_def = False
                new_file.write(line)  # Record line in new file
                continue

            if not def_found:  # If def statement is not found
                if line == '\n' or line[0] == '#':  # If the line it's just a \n or a comment line
                    continue

                if not hand_created_def:  # If not yet created an automatically def
                    count_hand_created_def += 1
                    new_file.write('def created_by_auto_code_' + str(count_hand_created_def) + '():\n')
                    hand_created_def = True
                    def_found = False
                new_file.write('\t' + line)
            else:
                if line == '\n' or line[0] == '#':  # If the line it's just a \n or a comment line
                    continue

                if ' ' not in line[0:3]:  # If a single space of indentation not in starts of the line
                    def_found = False

                    if not hand_created_def:  # If not yet created an automatically def
                        count_hand_created_def += 1
                        new_file.write('def created_by_auto_code_' + str(count_hand_created_def) + '():\n')
                        hand_created_def = True
                        def_found = False
                    new_file.write('\t' + line)
                    continue
                new_file.write(line)

        new_file.close()
        subprocess.getoutput('python3 -m black ' + file_path)

        sc = SourceCode(file_path)
        CyclomaticComplexity(file_path, [sc]).calculate_complexity()
        code.cyclomatic_complexity = sc.cyclomatic_complexity

        os.remove(file_path)


# Unused function
def calculates_the_cyclomatic_complexity_if_the_code_is_not_modularized(source_codes):
    for code in source_codes:
        if len(code.cyclomatic_complexity) == 0:
            file_path = code.path.replace('.py', '__CC.py')

            new_file = open(file_path, 'w')
            new_file.write('def main():\n')

            for line in code.extract_content():
                new_file.write('\t' + line)

            new_file.close()

            sc = SourceCode(file_path)

            # format the file
            subprocess.getoutput('python3 -m black ' + sc.path)

            ccc = CyclomaticComplexity(file_path, [sc])
            ccc.calculate_complexity()
            code.cyclomatic_complexity = sc.cyclomatic_complexity

            os.remove(file_path)


def create_source_codes_from_path(path, score):
    source_codes = []

    for directory, subdirectories, files in os.walk(path):
        for file in files:
            if ('/alunos' in directory or '/professor' in directory) and ('.py' in file):
                source_code = SourceCode(os.path.join(directory, file))
                source_code.score = score
                source_codes.append(source_code)

    return source_codes


def load_configurations():
    return json.load(open('configuration/configs.json', 'r'))
