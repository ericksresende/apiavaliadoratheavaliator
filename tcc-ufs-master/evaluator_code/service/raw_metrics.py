import json
import subprocess as sp


class RawMetrics:
    def __init__(self, path, sources_code):
        self.path = path
        self.sources_code = sources_code

    def calculate_raw_metrics(self):
        """
        Calculate raw metrics:
        loc = Total lines of code
        lloc = Number of logical lines of code
        sloc = Number of source lines of code
        comments = Number of python comment lines
        single_comments = Number of lines which are just comments with no code
        multi = Number of line which represent multi-line string
        blank = Number of blank lines or whitespace only

        equation: loc = sloc + blanks + multi + single_comments
        :return:
        """
        process_data_string = sp.getoutput('python3 -m radon raw ' + self.path + ' -j')

        self.__extract_data(process_data_string)

        return self.sources_code

    def __extract_data(self, data):
        """
        :param data: string containing data for process
        :return: list of SourceCode class
        """
        data = json.loads(data[0:-4])

        # for key in json data
        for key in data.keys():
            # for source code in sources_code list
            for source_code in self.sources_code:
                if key == source_code.path:
                    source_code.raw_metrics = data[key]

        return self.sources_code

