


from group.models import Organization
from django import forms

class MediaForm(forms.ModelForm):
    class Meta:
        model= Organization
        fields= ["org_name", "org_desc", "media"]