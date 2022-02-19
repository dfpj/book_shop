from django import forms



class CommentForm(forms.Form):
    text = forms.CharField(label='Password', widget=forms.Textarea(attrs={'row':3,'class':'form-control','placeholder':"Write Your comment"}))
