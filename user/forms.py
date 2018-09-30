from django import forms

from .models import User


class LoginForm(forms.Form):
  email = forms.EmailField()
  password = forms.CharField()

  def clean(self):
    email = self.cleaned_data.get("email")
    password = self.cleaned_data.get("password")

    if email and password:
      valid = False

      try:
        self.user = User.objects.get(email__iexact=email)
        valid = self.user.check_password(password)
      except User.DoesNotExist:
        pass

      if not valid:
        self.add_error("email", "Email or password is incorrect.")
        self.add_error("password", "Email or password is incorrect.")