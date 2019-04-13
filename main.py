from formatting import Formatter, MultiChoiceItemFormatter, TextItemFormatter, BoxFormatter, CalcFormatter
from tools import get_items, prompt_questionaire_data

formatted_item_list = []
output_file = 'questionare.html'
total_points = 0


# Step 1: Get user inputs
qdata = prompt_questionaire_data()
nr_of_questions = qdata.pop('nr_of_questions')


# Step 2: Get a random list of questions.
items = get_items(nr_of_questions)


# Step 3: Turn each question into a properly formatted HTML snippet
for n, i in enumerate(items):
    total_points += int(i.get('points'))
    # print(n, str(i))
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


# Step 4: Combine all of the snippets into a single HTML questionaire.
qdata.update({"question_list": formatted_item_list,
              "total_points": total_points})
with open(output_file, 'wt') as f:
    f.write(str(Formatter(**qdata)))

print('Saved %d questions in file: %s' % (nr_of_questions, output_file))
