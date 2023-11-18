import subprocess as sp
import json


class CyclomaticComplexity:
    """
        Main responsibility is to calculate cyclomatic complexity using
        **radon** library.
    """

    def __init__(self, path, sources_code):
        """
        :param path: base path to files
        :param sources_code: list of SourceCode class
        """
        self.path = path
        self.sources_code = sources_code

    def calculate_complexity(self):
        """
        Calculates the cyclomatic complexity of the source codes of a given directory
        :return: List of the SourceCode class filling the cyclomatic complexity field
        """
        # Process all codes from directory and return json string with result
        process_data_string = sp.check_output('python -m radon cc ' + self.path + ' -j',shell=True)
        self.__extract_data(process_data_string)

        self.__clean_data()

        return self.sources_code

    def __extract_data(self, data):
        """
        :param data: string containing result process of sources code
        :return: list of SourceCode class
        """

        try:
            # Parse the JSON data
            parsed_data = json.loads(data)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON data: {e}")

        # Loop through the parsed data
        for key, value in parsed_data.items():
            # Find the corresponding SourceCode object
            matching_source_code = next((source_code for source_code in self.sources_code if source_code.path == key), None)
            if matching_source_code:
                matching_source_code.cyclomatic_complexity = value

        return self.sources_code


    def __clean_data(self):
        for source_code in self.sources_code:
            for component in source_code.cyclomatic_complexity:
                del component['endline']
                del component['lineno']
                del component['col_offset']
                del component['closures']

        return self.sources_code
