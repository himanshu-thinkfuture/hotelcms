from django import forms
from hotel.models import Nutrient, Product, ProductNutrients
from django.forms.models import inlineformset_factory


ProductNutrientFormset = inlineformset_factory(
    Product, ProductNutrients, fields=('product', 'nutrient', 'nutrient_value',)
)

class NutrientForm(forms.ModelForm):

  class Meta:
    model = Nutrient
    fields = ['nutrient_name', 'nutrient_unit']
    labels = {
      'nutrient_name': 'Nutrient Name',
      'nutrient_unit': 'Nutrient Unit'
    }


  def __init__(self, *args, **kwargs):
    super(NutrientForm, self).__init__(*args, **kwargs)


class ProductForm(forms.Form):
  CHOICES = [('Active', 'Active'),
             ('Inactive', 'Inactive')]

  name = forms.CharField(max_length=50)
  description = forms.CharField()
  status = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(attrs={'class': 'radio_button',}))

  def clean(self):
    cleaned_data = super(ProductForm, self).clean()
    name = cleaned_data.get('name')
    description = cleaned_data.get('description')
    status = cleaned_data.get('status')
    if not name and not description and not status:
      raise forms.ValidationError('You have to write something!')

class ProductNutrientsForm(forms.Form):
  nutrient = forms.ModelChoiceField(queryset=Nutrient.objects.all(), label='Nutrient', widget=forms.Select(attrs={'display': 'block'}))
  nutrient_value = forms. DecimalField()

  def clean(self):
    cleaned_data = super(ProductForm, self).clean()
    nutrient = cleaned_data.get('nutrient')
    nutrient_value = cleaned_data.get('nutrient_value')
    if not nutrient and not nutrient_value:
      raise forms.ValidationError('You have to write something!')
