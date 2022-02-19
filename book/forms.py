from django import forms


class SearchBookForm(forms.Form):
    search_value = forms.CharField(max_length=255,label='',widget=forms.TextInput(attrs={'class':'form-control me-2'}))