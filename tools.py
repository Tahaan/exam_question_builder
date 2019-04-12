# Use this module to read the Excel file or database.

# The main function will select questions from the file and return them.

# As an example we just have 3 hard-coded questions for now.
import csv
from random import randint


def parse_question_fields(question_row) -> dict:
    q_type = question_row[0]
    q_text = question_row[1]
    ans = question_row[2]
    if q_type == 'entry':
        q = {'q': q_text,
             'type': q_type}
    elif q_type == 'multi':
        q = {'q': q_text,
             'type': q_type,
             'answer_list': question_row[3:]
             }
    elif q_type == 'box':
        q = {'q': q_text,
             'type': q_type,
             'w': question_row[3],
             'h': question_row[4]
             }
    elif q_type == 'calc':

        # Parse the row and substitute variables here

        q = {'q': q_text,
             'type': q_type,
             'formula': question_row[1],
             'q_var': question_row[3],
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
