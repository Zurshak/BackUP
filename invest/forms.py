from .models import Paper

from django.forms import ModelForm, TextInput

class PaperForm(ModelForm):
	class Meta:
		model = Paper
		fields = ["name","nn","paper_price","broker_pay","dollar_price"]
		widgets = {'name': TextInput(attrs={
			'class':'form-control',
			'name':'paper',
			'id':'paper',
			'placeholder':"Введите наименование",
		}),'nn': TextInput(attrs={
			'class':'form-control',
			'name':'paper',
			'id':'paper',
			'placeholder':"кол-во",
		}),'paper_price': TextInput(attrs={
			'class':'form-control',
			'name':'paper',
			'id':'paper',
			'placeholder':"	Цена за лот",
		}),'broker_pay': TextInput(attrs={
			'class':'form-control',
			'name':'paper',
			'id':'paper',
			'placeholder':"Комиссия",
		}),'dollar_price': TextInput(attrs={
			'class':'form-control',
			'name':'paper',
			'id':'paper',
			'placeholder':"Курс покупки",
		})}