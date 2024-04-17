from django import forms
from .models import Sale
from users.models import CustomUser


class SaleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer'].queryset = CustomUser.objects.filter(groups__name='customer')

    class Meta:
        model = Sale
        fields = ('customer',)


class SalesReportForm(forms.Form):
    start_date = forms.DateField(label='Fecha de inicio',
                                 widget=forms.DateInput(
                                     attrs={'type': 'date'}
                                 ))
    end_date = forms.DateField(label='Fecha de fin',
                               widget=forms.DateInput(
                                   attrs={'type': 'date'}
                               ))