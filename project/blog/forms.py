from django import forms

class NameForm(forms.Form):
    name = forms.CharField(label='What is your name?')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        fields = '__all__'
        