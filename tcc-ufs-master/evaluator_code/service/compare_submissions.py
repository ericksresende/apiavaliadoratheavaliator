class CompareSubmissions:
    def __init__(self, base, submissions, configs):
        self.base = base
        self.submissions = submissions
        self.configs = configs

    def compare_cyclomatic_complexity(self):
        base_complexity = self.__compute_total_points_of_cyclomatic_complexity(self.base.cyclomatic_complexity)
        self.base.cyclomatic_complexity_result_txt = 'Complexidade ciclomática: {0} pontos.'.format(base_complexity)
        self.base.cyclomatic_complexity_result_csv = self.base.extract_problem_name() + ';' + self.base.extract_file_name() + ';YES;' + str(base_complexity) + ';-;'

        for submission in self.submissions:
            submission_total_complexity = self.__compute_total_points_of_cyclomatic_complexity(submission.cyclomatic_complexity)

            diff = submission_total_complexity - base_complexity
            alert = self.configs['diff_cyclomatic_complexity']
            submission.cyclomatic_complexity_result_csv = submission.extract_problem_name() + ';' + submission.extract_file_name() + ';NO;' + str(submission_total_complexity) + ';'

            if 0 < diff > alert:
                # Aqui a submissao do aluno teve complexidade maior que a do professor baseado na configuração de alerta
                submission.cyclomatic_complexity_result_txt = '{0} pontos com diferença de {1} pontos com a solução base ultrapassando o limite de alerta de {2} pontos'.format(submission_total_complexity, diff, alert)
                submission.cyclomatic_complexity_result_csv += 'YES;'
                self.__calculate_score(submission, diff)
                continue
            if 0 > diff < -alert:
                print(submission.path)
                # Aqui a submissao do professor teve uma complexidade ciclomatica geral maior do que a do aluno passando do nivel de alerta
                submission.cyclomatic_complexity_result_txt = '{0} pontos com diferença de {1} pontos com a solução base ultrapassando o limite de alerta de  -{2} pontos.'.format(submission_total_complexity, diff, alert)
                submission.cyclomatic_complexity_result_csv += 'YES;'
                self.__calculate_score(submission, diff)
                continue
            if 0 < diff < alert:
                # Aqui a submissao do aluno teve maior complexidade que a do professor, porém não passou do nivel de alerta
                submission.cyclomatic_complexity_result_txt = '{0} pontos contra {1} da solução base.'.format(submission_total_complexity, base_complexity)
                submission.cyclomatic_complexity_result_csv += 'NO;'
                self.__calculate_score(submission, diff)
                continue
            if 0 > diff > -alert:
                # Aqui a submissao do aluno teve menor complexidade que a do professor, porém não passou do nivel de alerta
                submission.cyclomatic_complexity_result_txt = '{0} pontos contra {1} da solução base'.format(submission_total_complexity, base_complexity)
                submission.cyclomatic_complexity_result_csv += 'NO;'
                self.__calculate_score(submission, diff)
                continue

            submission.cyclomatic_complexity_result_txt = '{0} pontos, igual a solução base'.format(submission_total_complexity)
            submission.cyclomatic_complexity_result_csv += 'NO;'

    def compare_raw_metrics(self):
        self.base.raw_metrics_result_txt = 'Linhas de código: {0}'.format(self.base.raw_metrics['loc'])
        self.base.raw_metrics_result_txt += '\n\t\tLinhas lógicas de código: {0}'.format(self.base.raw_metrics['lloc'])
        self.base.raw_metrics_result_txt += '\n\t\tLinhas de código fonte: {0}'.format(self.base.raw_metrics['sloc'])

        self.base.raw_metrics_result_csv += str(self.base.raw_metrics['loc']) + ';-;' + str(self.base.raw_metrics['lloc']) + ';-;' + str(self.base.raw_metrics['sloc']) + ';-;-;'
        for code in self.submissions:
            self.__lines_of_code_metric(code)
            self.__logical_lines_of_code_metric(code)
            self.__lines_of_source_code_metric(code)
            code.score = round(code.score, 2)
            code.raw_metrics_result_csv += str(code.score) + ';'

    def compare_submissions_which_need_attention(self):
        score_great = self.configs['score_to_great_solution']
        score_not_so_good = self.configs['score_to_not_so_good_solution']
        for submission in self.submissions:
            if submission.score >= score_great:
                submission.need_attention = True
                submission.need_attention_type = 'Score >= ' + str(score_great)
                continue
            if submission.score <= score_not_so_good:
                submission.need_attention = True
                submission.need_attention_type = 'Score <= ' + str(score_not_so_good)


    def __lines_of_source_code_metric(self, code):
        diff_sloc = code.raw_metrics['sloc'] - self.base.raw_metrics['sloc']
        alert_sloc = self.configs['diff_raw_metrics_sloc']
        source_lines_of_code = code.raw_metrics['lloc']
        code.raw_metrics_result_csv += str(source_lines_of_code) + ';'

        if 0 < diff_sloc > alert_sloc:
            # Solucao do aluno teve mais linhas de código que a do professor e ultrapassou o limite de alerta
            code.raw_metrics_result_txt += '\n\t\t\tLinhas de código fonte: {0}; Diferença com a submissão base: {1}; Ultrapassou o limite de alerta de {2}'.format(
                source_lines_of_code, diff_sloc, alert_sloc)
            code.raw_metrics_result_csv += 'YES;'
            self.__calculate_score(code, diff_sloc, True)
            return
        if 0 < diff_sloc < alert_sloc:
            # Solucao do aluno teve mais linhas de código que a do professor, porém não ultrapassou o limite de alerta
            code.raw_metrics_result_txt += '\n\t\t\tLinhas de código fonte: {0}; Diferença com a submissão base: {1};'.format(
                source_lines_of_code, diff_sloc)
            code.raw_metrics_result_csv += 'NO;'
            self.__calculate_score(code, diff_sloc, True)
            return
        if 0 > diff_sloc < -alert_sloc:
            # Solucao do aluno teve menos linhas de código que a do professor e ultrapassou o limite de alerta
            code.raw_metrics_result_txt += '\n\t\t\tLinhas de código fonte: {0}; Menos linhas que a submissão base, porém ultrapassou o limite de alerta de {1}'.format(
                source_lines_of_code, alert_sloc)
            code.raw_metrics_result_csv += 'YES;'
            self.__calculate_score(code, diff_sloc, True)
            return
        if 0 > diff_sloc > -alert_sloc:
            # Solucao do aluno teve menos linhas de código que a do professor e não ultrapassou o limite de alerta
            code.raw_metrics_result_txt += '\n\t\t\tLinhas de código fonte: {0}; Menos linhas que a submissão base e não ultrapassou o limite de alerta'.format(
                source_lines_of_code)
            code.raw_metrics_result_csv += 'NO;'
            self.__calculate_score(code, diff_sloc, True)
            return
        code.raw_metrics_result_txt += '\n\t\t\tLinhas de código fonte: {0}; Quantidade igual de linhas com a submissão base'.format(
            source_lines_of_code)
        code.raw_metrics_result_csv += 'NO;'

    def __logical_lines_of_code_metric(self, code):
        diff_lloc = code.raw_metrics['lloc'] - self.base.raw_metrics['lloc']
        alert_lloc = self.configs['diff_raw_metrics_lloc']
        logical_lines_of_code = code.raw_metrics['lloc']
        code.raw_metrics_result_csv += str(logical_lines_of_code) + ';'

        if 0 < diff_lloc > alert_lloc:
            # Solucao do aluno teve mais linhas de código que a do professor e ultrapassou o limite de alerta
            code.raw_metrics_result_txt += '\n\t\t\tLinhas lógicas de código: {0}; Diferença com a submissão base: {1}; Ultrapassou o limite de alerta de {2}'.format(logical_lines_of_code, diff_lloc, alert_lloc)
            code.raw_metrics_result_csv += 'YES;'
            self.__calculate_score(code, diff_lloc, True)
            return
        if 0 < diff_lloc < alert_lloc:
            # Solucao do aluno teve mais linhas de código que a do professor, porém não ultrapassou o limite de alerta
            code.raw_metrics_result_txt += '\n\t\t\tLinhas lógicas de código: {0}; Diferença com a submissão base: {1};'.format(logical_lines_of_code, diff_lloc)
            code.raw_metrics_result_csv += 'NO;'
            self.__calculate_score(code, diff_lloc, True)
            return
        if 0 > diff_lloc < -alert_lloc:
            # Solucao do aluno teve menos linhas de código que a do professor e ultrapassou o limite de alerta
            code.raw_metrics_result_txt += '\n\t\t\tLinhas lógicas de código: {0}; Menos linhas que a submissão base, porém ultrapassou o limite de alerta de {1}'.format(logical_lines_of_code, alert_lloc)
            code.raw_metrics_result_csv += 'YES;'
            self.__calculate_score(code, diff_lloc, True)
            return
        if 0 > diff_lloc > -alert_lloc:
            # Solucao do aluno teve menos linhas de código que a do professor e não ultrapassou o limite de alerta
            code.raw_metrics_result_txt += '\n\t\t\tLinhas lógicas de código: {0}; Menos linhas que a submissão base e não ultrapassou o limite de alerta'.format(logical_lines_of_code)
            code.raw_metrics_result_csv += 'NO;'
            self.__calculate_score(code, diff_lloc, True)
            return
        code.raw_metrics_result_txt += '\n\t\t\tLinhas lógicas de código: {0}; Quantidade igual de linhas com a submissão base'.format(logical_lines_of_code)
        code.raw_metrics_result_csv += 'NO;'

    def __lines_of_code_metric(self, code):
        diff_loc = code.raw_metrics['loc'] - self.base.raw_metrics['loc']
        alert_loc = self.configs['diff_raw_metrics_loc']
        lines_of_code = code.raw_metrics['loc']
        code.raw_metrics_result_csv = str(lines_of_code) + ';'

        if 0 < diff_loc > alert_loc:
            # Solucao do aluno teve mais linhas de código que a do professor e ultrapassou o limite de alerta
            code.raw_metrics_result_txt = 'Linhas de código: {0}; Diferença com a submissão base: {1}; Ultrapassou o limite de alerta de {2}'.format(lines_of_code, diff_loc, alert_loc)
            code.raw_metrics_result_csv += 'YES;'
            self.__calculate_score(code, diff_loc, True)
            return
        if 0 < diff_loc < alert_loc:
            # Solucao do aluno teve mais linhas de código que a do professor, porém não ultrapassou o limite de alerta
            code.raw_metrics_result_txt = 'Linhas de código: {0}; Diferença com a submissão base: {1};'.format(lines_of_code, diff_loc)
            code.raw_metrics_result_csv += 'NO;'
            self.__calculate_score(code, diff_loc, True)
            return
        if 0 > diff_loc < -alert_loc:
            # Solucao do aluno teve menos linhas de código que a do professor e ultrapassou o limite de alerta
            code.raw_metrics_result_txt = 'Linhas de código: {0}; Menos linhas que a submissão base, porém ultrapassou o limite de alerta de {1}'.format(lines_of_code, alert_loc)
            code.raw_metrics_result_csv += 'YES;'
            self.__calculate_score(code, diff_loc, True)
            return
        if 0 > diff_loc > -alert_loc:
            # Solucao do aluno teve menos linhas de código que a do professor e não ultrapassou o limite de alerta
            code.raw_metrics_result_txt = 'Linhas de código: {0}; Menos linhas que a submissão base e não ultrapassou o limite de alerta'.format(lines_of_code)
            code.raw_metrics_result_csv += 'NO;'
            self.__calculate_score(code, diff_loc, True)
            return
        code.raw_metrics_result_txt = 'Linhas de código: {0}; Quantidade igual de linhas com a submissão base'.format(lines_of_code)
        code.raw_metrics_result_csv += 'NO;'

    def __compute_total_points_of_cyclomatic_complexity(self, complexity):
        total_points = 0
        if len(complexity) > 1:
            for function in complexity:
                total_points += function['complexity']
            return total_points

        return complexity[0]['complexity']

    def __calculate_score(self, submission, diff_in_points, is_raw_metrics=False):
        increase_factor = self.configs['increase_factor']
        decrease_factor = self.configs['decrease_factor']

        if is_raw_metrics:
            increase_factor *= (self.configs['rate_increase_to_raw_metrics'] / 100)
            decrease_factor *= (self.configs['rate_decrease_to_raw_metrics'] / 100)

        if diff_in_points > 0:
            submission.score -= diff_in_points * decrease_factor
        else:
            submission.score += -diff_in_points * increase_factor



