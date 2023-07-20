from django import forms
from django.core.validators import EMPTY_VALUES

# from https://docs.djangoproject.com/en/4.1/topics/forms/
class CreateUserForm(forms.Form):
    username = forms.CharField(label='username', max_length=50,required=False)
    name = forms.CharField(label='Name', max_length=50)
    is_student = forms.BooleanField(label='Is Student',required=False)
    rate = forms.DecimalField(label='Hourly Rate in USD (Required For Tutors)',required=False)

    start_time = forms.DateTimeField(label='Availability Start Time (In "YYYY-MM-DD H:M:S" Format, Required For Tutors)',required=False)
    end_time = forms.DateTimeField(label='Availability End Time (In "YYYY-MM-DD H:M:S" Format, Required For Tutors)',required=False)

    venmo_username = forms.CharField(label='Venmo Username (Required For Tutors)', max_length=50, required=False)

    #https://stackoverflow.com/questions/22816186/make-a-field-required-if-another-field-is-checked-in-django-form
    def clean(self):
        if not self.cleaned_data['is_student']:
            venmo_username = self.cleaned_data.get('venmo_username', None)
            if venmo_username in EMPTY_VALUES:
                self._errors['venmo_username'] = self.error_class(['Venmo username required for Tutors'])
            rate = self.cleaned_data.get('rate',None)
            if rate in EMPTY_VALUES:
                self._errors['rate'] = self.error_class(['Rate required for Tutors'])
            start_time = self.cleaned_data.get('start_time',None)
            if start_time in EMPTY_VALUES:
                self._errors['start_time'] = self.error_class(['Availability start time required for Tutors'])
            end_time = self.cleaned_data.get('end_time',None)
            if end_time in EMPTY_VALUES:
                self._errors['end_time'] = self.error_class(['Availability end time required for Tutors'])
        print(self.cleaned_data)
        print(self._errors)
        return self.cleaned_data

class AddRequestForm(forms.Form):
    #student_username = forms.CharField(label='student_username',max_length-50)
    #tutor_username = forms.CharField(label='tutor_username',max_length-50)
    time = forms.DateTimeField(label='Time (In "YYYY-MM-DD H:M:S" Format)')
