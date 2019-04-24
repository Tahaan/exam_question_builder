import json

from flask import render_template

from questionaire.subjects.utils import subject_name

TYPE_LIST = [
    ('entry', 'Simple Input'),
    ('int', 'Integer Number'),
    ('multi', 'Multiple Choice'),
    ('box', 'Picture Box')]


def type_description(typeid):
    for x, name in TYPE_LIST:
        if x == typeid:
            return name
    return "TYPE NAME NOT FOUND: %s" % typeid


def parse_question_options(optionlist_data, boxw, boxh):
    return json.dumps({
        'mcoptions': [str(i) for i in optionlist_data],
        'mc_debug_type': str(type(optionlist_data)),
        'mc_debug_raw': str(optionlist_data),
        'boxw': str(boxw),
        'boxh': str(boxh)
    })


def show_questionlist(question_page, pg, subj=None):
    question_list = [{'q': i.q,
                      'points': i.points,
                      'answer': i.answer,
                      'type': type_description(i.type),
                      'memo': i.memo,
                      'id': i.id,
                      'subject': subject_name(i.subject),
                      'subj_id': i.subject,
                      'nr': n + 1 + (pg - 1) * question_page.per_page} for n, i in enumerate(question_page.items)]

    return render_template('questions.html',
                           questions=question_list,
                           pages=question_page.iter_pages(left_edge=1,
                                                          right_edge=1,
                                                          left_current=2,
                                                          right_current=3),
                           current_pagenr=pg,
                           subj=subj
                           )
