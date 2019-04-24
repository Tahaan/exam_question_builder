# Use this module to read the Excel file or database.

# The main function will select questions from the file and return them.

# As an example we just have 3 hard-coded questions for now.
import csv
import json
import os
from random import randint


DEFAULT_CONFIG_FILE = 'webservice.conf'


# Singleton Class holding application config
class ConfigManager:
    SECRET_KEY = 'd31b4f37bf2b1a8be9f93107c1d27ad083e92b4ed6416866b5487be73765a2b5'

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = '587'
    MAIL_USE_TLS = 'True'

    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')

    _conf = {}

    def __init__(self, filename=None):
        if not ConfigManager._conf:
            if filename is None:
                filename - DEFAULT_CONFIG_FILE
            ConfigManager._conf = self.read_config(filename)
            for k, v in ConfigManager._conf.items():
                self.set_property(k, v)
                print('Config Update: %s = %s' % (k, v))

    @classmethod
    def set_property(cls, propertyname, value):
        cls.propertyname = value

    @classmethod
    def read_config(cls, filename):
        try:
            with open(filename, 'rt') as configfile:
                return json.loads(configfile.read())
        except Exception as e:
            print('WARNING: Failed to load config file "%s".\nError: %s' % (filename, str(e)))
            return {}

    @classmethod
    def get(cls, key, default=None):
        return cls._conf.get(key, default)

    def __getitem__(self, item):
        return ConfigManager.get(item)


def parse_question_fields(question_row) -> dict:
    q_type = question_row[0]
    q_text = question_row[1]
    ans = question_row[2]
    points = question_row[3]
    if q_type == 'entry':
        q = {'q': q_text,
             'type': q_type,
             'points': points}
    elif q_type == 'multi':
        q = {'q': q_text,
             'type': q_type,
             'points': points,
             'answer_list': question_row[4:]
             }
    elif q_type == 'box':
        q = {'q': q_text,
             'type': q_type,
             'points': points,
             'w': question_row[4],
             'h': question_row[5]
             }
    elif q_type == 'calc':

        # Parse the row and substitute variables here

        q = {'q': q_text,
             'type': q_type,
             'points': points,
             'formula': question_row[1],
             'q_var': question_row[4],
             }
    else:
        raise ValueError('Unknown question type %s' % q_type)
    return q


def read_from_csv(filename):
    questions = []
    with open(filename, 'rt') as csvfile:
        question_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for question_row in question_reader:
            questions.append(question_row)
    return questions


def fixed_questions():
    raise NotImplemented('Oops, This is no longer working')
    # i1 = {'q': 'What is the Formula for calculating X',
    #       'type': 'multi',
    #       'answer_list': ['x = a + b',
    #                       'X = 3a + 9',
    #                       'X = z / 0']}
    # i2 = {'q': 'In what year was the computer discovered',
    #       'type': 'multi',
    #       'answer_list': ['1990', '2005', '1805', 'All of the above']}
    # i3 = {'q': 'What is the foo of the fib',
    #       'type': 'entry',
    #       'a': 'Enter Foo'}
    # questions = [i1, i2, i3]
    # return questions


def pick_n_from_list(n, list_len, sorted=False) -> list:
    if n > list_len:
        raise ValueError("Impossible to select %d items from a list of %d questions" % (n, list_len))
    picked = []
    while len(picked) < n:
        p = randint(0, list_len-1)
        if p not in picked:
            picked.append(p)
    if sorted:
        picked.sort()
    return picked


def get_items(n=0) -> list:
    # Return a list of dict.  Select items randomly from a database, text file ot spreadsheet
    # Every item must have a type (type) and a question (q).  Other fields depends on what the
    # template needs.
    #
    # For now we have "multi" and "entry" but you can have many types.  Each type needs to have a
    # template if it needs different formatting.

    questions = read_from_csv('questions.csv')
    selected_question_nrs = pick_n_from_list(n, len(questions), sorted=True)
    print(selected_question_nrs)
    return [parse_question_fields(questions[i]) for i in selected_question_nrs]


def prompt_questionaire_data() -> dict:
    nr_of_questions = int(input('How many questions: '))
    title = input('Enter Exam Title: ')
    time = input('Time Allowed: ')

    print('Type Instructions.  End with a single fullstop on the last line')
    instr_list = []
    while True:
        instr_line = input()
        instr_line = instr_line.strip()
        if instr_line == '.':
            break
        instr_list.append(instr_line)
    instr = '<br>\n'.join(instr_list)

    return {"time": time,
            "instr": instr,
            "total_points": 0,
            "question_list": [],
            "title": title,
            "nr_of_questions": nr_of_questions
            }
