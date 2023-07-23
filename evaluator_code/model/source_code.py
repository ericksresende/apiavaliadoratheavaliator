class SourceCode:
    def __init__(self, path):
        self.path = path
        self.content = []
        self.cyclomatic_complexity = []
        self.raw_metrics = []
        self.cyclomatic_complexity_result_txt = ''
        self.raw_metrics_result_txt = ''
        self.cyclomatic_complexity_result_csv = ''
        self.raw_metrics_result_csv = ''
        self.score = 0
        self.need_attention = False
        self.need_attention_type = ''

    def print_content(self):
        print(self.content)

    def extract_content(self):
        with open(self.path, 'r') as file:
            self.content = [line for line in file]
        return self.content

    def count_code_lines(self):
        return len(self.content)

    def print_attr(self):
        print(self.path)
        print(self.cyclomatic_complexity)
        print(self.raw_metrics)

    def extract_file_name(self):
        return self.path.split('\\')[-1].replace('.py', '')

    def extract_problem_name(self):
        return self.path.split('\\')[-3]

    def is_base_source_code(self):
        return self.path.split('\\')[-2] == 'professor'
