from django import forms
from .models import ArIterations
from manage_product.models import AR_product,AR_team
from manage_backlogs.models import AR_BACKLOG
from django.db.models import Subquery
import string
import random




class IterationForm(forms.ModelForm):
    IterationName = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': "Iteration Name", }))
    owner = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': "Owner", }))
    Description = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control login-frm-input", "style": "height: 100px!important;","placeholder": "Description", }))
    IterationScore = forms.CharField(widget=forms.NumberInput(attrs={"class": "form-control", 'name': 'Iteration Score', "value": "0", "readonly": "readonly"}))
    IterationSize = forms.CharField(widget=forms.NumberInput(attrs={"class": "form-control", 'name': 'Iteration Size', "value": "0", "readonly": "readonly"}))

    class Meta:
        model = ArIterations
        fields = ['IterationName', 'owner','Description', 'Product','Backlog','UserStory','Team','IterationScore','IterationSize']

    def __init__(self, org_info, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Product'] = forms.ModelChoiceField(required=False,empty_label="Please select product",queryset=AR_product.objects.filter(ORG_ID__in=Subquery(org_info.values("id"))),widget=forms.Select(attrs={"class": "form-control"}))
        self.fields['Backlog'] = forms.ModelChoiceField(required=False,empty_label="Please select backlog",queryset=AR_BACKLOG.objects.none(),widget=forms.Select(attrs={"class": "form-control"}))

        if 'Product' in self.data:
            try:
                Product_id = int(self.data.get('Product'))
                # self.fields['Backlog'].queryset = AR_BACKLOG.objects.filter(required=False,product_parent_id=Product_id)
                self.fields['Backlog'] = forms.ModelChoiceField(required=False, empty_label="Please select backlog",
                                                                queryset=AR_BACKLOG.objects.filter(
                                                                    product_parent=Product_id),
                                                                widget=forms.Select(attrs={"class": "form-control"}))
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            # self.fields['Backlog'].queryset = AR_BACKLOG.objects.filter(required=False,product_parent=self.instance.Product)

            self.fields['Backlog'] = forms.ModelChoiceField(required=False, empty_label="Please select backlog",
                                                                queryset=AR_BACKLOG.objects.filter(
                                                                    product_parent=self.instance.Product),
                                                                widget=forms.Select(attrs={"class": "form-control"}))
        self.fields['Team'] = forms.ModelChoiceField(required=False, empty_label="Please select team",
                                                                queryset=AR_team.objects.filter(
                                                                    ORG_id__in=Subquery(org_info.values("id"))),
                                                                widget=forms.Select(attrs={"class": "form-control"}))


        # self.fields['Team'] = forms.ModelChoiceField(required=False,empty_label="Please select team",queryset=AR_team.objects.filter(ORG_id__in=Subquery(org_info.values("id"))),widget=forms.Select(attrs={"class": "form-control"}))



