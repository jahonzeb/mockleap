from django import forms
from apps.reading.models import ReadingTest, ReadingPassage, QuestionGroup, Question
from apps.listening.models import ListeningTest, ListeningSection, ListeningQuestion

_textarea = lambda rows: forms.Textarea(attrs={'rows': rows})
_input    = lambda placeholder='': forms.TextInput(attrs={'placeholder': placeholder})


class ReadingTestForm(forms.ModelForm):
    class Meta:
        model  = ReadingTest
        fields = ['title', 'test_type', 'duration_minutes', 'is_published']


class ReadingPassageForm(forms.ModelForm):
    class Meta:
        model   = ReadingPassage
        fields  = ['order', 'title', 'content', 'source']
        widgets = {'content': _textarea(18), 'title': _input('Passage title')}


class QuestionGroupForm(forms.ModelForm):
    class Meta:
        model   = QuestionGroup
        fields  = ['order', 'question_type', 'instructions']
        widgets = {'instructions': _textarea(3)}


class ReadingQuestionForm(forms.ModelForm):
    class Meta:
        model   = Question
        fields  = ['number', 'text', 'option_a', 'option_b', 'option_c', 'option_d',
                   'correct_answer', 'explanation']
        widgets = {
            'text':        _textarea(2),
            'explanation': _textarea(2),
        }


class ListeningTestForm(forms.ModelForm):
    class Meta:
        model  = ListeningTest
        fields = ['title', 'duration_minutes', 'audio_file', 'is_published']


class ListeningSectionForm(forms.ModelForm):
    class Meta:
        model   = ListeningSection
        fields  = ['order', 'title', 'description']
        widgets = {
            'title':       _input('Section title'),
            'description': _textarea(3),
        }


class ListeningQuestionForm(forms.ModelForm):
    class Meta:
        model   = ListeningQuestion
        fields  = ['number', 'question_type', 'text',
                   'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer']
        widgets = {'text': _textarea(2)}
