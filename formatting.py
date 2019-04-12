import preppy


# Master formatter class.  Passes all the initialisation arguments to the parser.
class Formatter:
    templatefile = 'questionaire.prep'

    def __init__(self, **kwargs):
        self.formatter = preppy.getModule(self.templatefile)
        self.props = kwargs

    def __str__(self):
        return self.formatter.get(**self.props)


# A sub-class for questions.  We strip out the 'type' field since this isn't used in any question template.
class QuestionFormatter(Formatter):
    def __init__(self, **kwargs):
        kwargs.pop('type', None)
        # After removing the type field, just works like the main formatter class
        super().__init__(**kwargs)


# A formatter that will set a different template file for a multi-choice question.
class MultiChoiceItemFormatter(QuestionFormatter):
    templatefile = 'question_template_multichoice.prep'


# A formatter that will set a different template file for a test-input-choice question.  It also passes along only the question
class TextItemFormatter(QuestionFormatter):
    templatefile = 'question_template_text.prep'

    def __init__(self, **kwargs):
        super().__init__(q=kwargs.get('q'))


# A formatter that will draw a box
class BoxFormatter(QuestionFormatter):
    templatefile = 'question_template_box.prep'

    def __init__(self, **kwargs):
        super().__init__(q=kwargs.get('q'), w=kwargs.get('w'), h=kwargs.get('h'))


# An INCOMPLETE formatter that will make up a calculation question....
class CalcFormatter(QuestionFormatter):
    templatefile = 'question_template_calc.prep'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
