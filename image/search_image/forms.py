from django import forms
from . models import UpForm, Famous, Video

famous = Famous.objects.all().values_list('name','name')
famous_list = []
for item in famous:
    famous_list.append(item)

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UpForm
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={
        'class': 'form-control',
        'type':'file',
        # 'accept': 'images/*',
        # 'value':'Upload photo',
        # 'name': 'inpFile',
        # 'id': 'inpFile',
        
        })
        }


      
class UploadVideoForm(forms.ModelForm):
    class Meta:
        # famous = Famous.objects.all().values_list('name','name')
        model = Video
        fields = ['title','video','description','represent']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'video': forms.FileInput(attrs={
            'class': 'form-control',
            'type':'file',
            'accept': 'video/*',
            
            }),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'represent': forms.FileInput(attrs={
            'class': 'form-control',
            'type':'file',
            'accept': 'image/*',
            }),
        }


class FamousForm(forms.ModelForm):
    class Meta:
        model = Famous
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'famous'}),
        }

class EditFamousForm(forms.ModelForm):
    class Meta:
        model = Famous
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'famous'}),
        }
