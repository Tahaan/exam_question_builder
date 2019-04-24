from questionaire.models import Subject, Question


def subject_name(subjid):
    for s in Subject.query.filter_by(id=subjid).first():
        if s.id == subjid:
            return s.name
    return "SUBJECT NAME NOT FOUND: %s" % subjid
