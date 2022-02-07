from django import forms
from django.contrib.auth.models import User
from apps.userauth.models import UserProfile

class UserForm(forms.ModelForm):
	email = forms.EmailField(required=True)
	password = forms.CharField(widget=forms.PasswordInput())
	confirm_password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password')

	# Make sure passwords match:
	def clean(self):
		cleaned_data = super(UserForm, self).clean()
		password = cleaned_data.get("password")
		confirm_password = cleaned_data.get("confirm_password")

		if password != confirm_password:
			raise forms.ValidationError("Password do not match")

# Form for all users to create a profile
class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		exclude = ['']