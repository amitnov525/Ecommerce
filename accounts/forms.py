from dataclasses import fields
from xml.dom import ValidationErr
from django import forms 
from accounts.models import MyUser

class RegistrationForm(forms.ModelForm):
    password=forms.CharField(max_length=250,required=True,widget=forms.PasswordInput(attrs={'placeholder':'Enter Password'}))
    confirm_password=forms.CharField(max_length=250, required=True,widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password'}))
    class Meta:
        model=MyUser
        fields=['first_name','last_name','email','phone_number','password']
    
    def __init__(self,*args,**kwargs):
        super(RegistrationForm,self).__init__(*args,**kwargs)
        self.fields['first_name'].widget.attrs['placeholder']='Enter Your First Name'
        self.fields['last_name'].widget.attrs['placeholder']='Enter Your Last Name'
        self.fields['email'].widget.attrs['placeholder']='Enter Your Email Address'
        self.fields['phone_number'].widget.attrs['placeholder']='Enter Your phone_number.'
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'
    def clean(self):
        cleaned_data=super(RegistrationForm,self).clean()
        password=cleaned_data.get('password')
        passwoed1=cleaned_data.get('confirm_password')
        if password!=passwoed1:
            raise forms.ValidationError(
                "Password Does Not Match."
            )


    
