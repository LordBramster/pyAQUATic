import yaml
import logging


# ---------------------------------------------------------------------------------------------------------------------


class validation:
    def __init__(self, requirements_file, logfile=None):
        # SETUP
        self.setup_logging(logfile)

        # PREP REQUIREMENTS
        self.requirements_yaml = open_yaml(requirements_file)
        self.required_list = self.requirements_yaml['required']
        self.optional_list = self.requirements_yaml['optional']
        self.index_name = 0
        self.index_desc = 1
        self.index_exp = 2

    def setup_logging(self, log):
        if log is None:
            logging.basicConfig(format='%(asctime)s | %(message)s',
                                datefmt='%m/%d/%Y %I:%M:%S %p',
                                level=logging.INFO)
        else:
            logging.basicConfig(filename=log,
                                format='%(asctime)s | %(message)s',
                                datefmt='%m/%d/%Y %I:%M:%S %p',
                                level=logging.INFO)

    def log(self, result, title, level=None):
        if result:
            if not level: level = 'info'
            result_str = 'PASSED'
        else:
            if not level: level = 'error'
            result_str = 'FAILED'

        message = f"{title} : {result_str}"
        if level == 'info': logging.info(message)
        if level == 'debug': logging.debug(message)
        if level == 'warn': logging.warning(message)
        if level == 'error': logging.error(message)

    def validate(self, req_name, actual):
        try:
            found_req = self.find_requirement_match(req_name, self.required_list)

            name = found_req[self.index_name]
            description = found_req[self.index_desc]
            expected = found_req[self.index_exp]

            self.do_validate(description, actual, expected)

        except Exception as e:
            print(e)

    def do_validate(self, title, actual, expected):
        try:
            assert actual == expected
            result = True
        except AssertionError as e:
            result = False

        self.log(result, title)
        return result

    def find_requirement_match(self, req_name, requirements):
        found = None
        for requirement in requirements:
            if req_name == requirement[self.index_name]:
                found = requirement
                break
        if not found:
            raise Exception('\nCould not match this actual value to an item...\n')
        else:
            return found


# ---------------------------------------------------------------------------------------------------------------------

def open_yaml(filename):
    with open(filename, 'r') as stream:
        try:
            data = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            data = None
    return data
