from formatting import Formatter, MultiChoiceItemFormatter, TextItemFormatter, BoxFormatter, CalcFormatter
from tools import get_items


formatted_item_list = []
output_file = 'questionare.html'


# Step 1:  Get a random list of questions.
nr_of_questions = int(input('How many questions: '))
items = get_items(nr_of_questions)


# Step 2: Turn each question into a properly formatted HTML snippet
for n, i in enumerate(items):
    print(n, str(i))
    if i['type'] == 'multi':
        formatted_item_list.append(str(MultiChoiceItemFormatter(**i)))
    elif i['type'] == 'entry':
        formatted_item_list.append(str(TextItemFormatter(**i)))
    elif i['type'] == 'box':
        formatted_item_list.append(str(BoxFormatter(**i)))
    elif i['type'] == 'calc':
        formatted_item_list.append(str(CalcFormatter(**i)))
    else:
        raise ValueError("Don't know how to format item %s (type = %s)" % (n, i['type']))


# Step 3: Combine all of the snippets into a single HTML questionaire.
with open(output_file, 'wt') as f:
    f.write(str(Formatter(title='Test: 2019-02-31',
                          question_list=formatted_item_list)))

print('Saved %d questions in file: %s' % (nr_of_questions, output_file))
