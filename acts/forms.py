from django.forms import ModelForm
from django import forms
from .models import Act

class ActForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'special'})
        self.fields['adress'].widget.attrs.update({'class': 'special'})
        self.fields['act_type'].widget.attrs.update({'class': 'special'})
        self.fields['text'].widget.attrs.update({'class': 'special'})
        self.fields['image'].widget.attrs.update({'class': 'special'})

    image = forms.ImageField(required = False)
    file = forms.FileField(required = False)

    class Meta:
        model = Act
        fields = '__all__'
        exclude = ('act_processing', 'do_until', 'user', 'executer')


class ActSetDateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['do_until'].widget.attrs.update({'class': 'special'})

    class Meta:
        model = Act
        fields = ('do_until',)
        widgets = {
            'do_until': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }