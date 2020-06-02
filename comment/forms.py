from django import forms

class CommentForm(forms.Form):
    object_blog=forms.CharField(widget=forms.HiddenInput)
    object_id=forms.IntegerField(widget=forms.HiddenInput)
    text=forms.CharField(label='欢迎评论',widget=forms.Textarea(attrs={'class':"form-control",'placeholder':'请在此处评论','rows':5}))
    
    reply_comment_id=forms.IntegerField(widget=forms.HiddenInput(attrs={'id':'reply_comment_id'}))