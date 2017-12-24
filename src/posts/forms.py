from django import forms
from .models import post

class PostForm(forms.ModelForm):
	class Meta:
		model=post
		fields=[
		"title",
		"content",
		"image",
		"draft",
		"publish",
		]




# forms.class MODELNAMEForm(forms.ModelForm):
#     class Meta:
#         model = MODELNAME
#         fields = ('',)
    