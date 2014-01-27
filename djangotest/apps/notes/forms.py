from django import forms
#from django.forms.util import ErrorList
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import Group, Permission
# from django.contrib.contenttypes.models import ContentType

class UpperCaseField(forms.CharField):
    
    """
    Create custom form field that extends CharField and changes all characters 
    is the field to uppercase
    """
    
    def clean(self, value):
        try:
            return value.upper()
        except:
            raise forms.ValidationError

class AddNoteForm(forms.Form):

    """    
    Create form that allows to add new text note with at least 10 symbols"         
    """

    note = UpperCaseField(
        widget=forms.Textarea(attrs={
                'placeholder':'# newnote', 
                'class':'form-control',
                'rows':5}),
        required=False)

    def clean_note(self):
        """ Raise ValidationError when the note contains less than 10 symbols"""
        message = self.cleaned_data['note']
        num_symbs = len(message)
        if num_symbs < 10:
            raise forms.ValidationError("Your note should contain at least 10 symbols!")
        return message
