from django.forms import ModelForm
from backoffice.models import *

from django.forms import DateInput


class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = '__all__'

class ClientAddressForm(ModelForm):
    class Meta:
        model = Address
        fields = '__all__'

class ClientDetailForm(ModelForm):
    class Meta:
        model = Client
        fields = '__all__'


# ------------------------------------------------------------------- #
# ------------------------------------------------------------------- #
# ---------------------------- PRODUCTS ----------------------------- #
# ------------------------------------------------------------------- #
# ------------------------------------------------------------------- #

class NewProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class ProductDetailForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

# ------------------------------------------------------------------- #
# ------------------------------------------------------------------- #
# ----------------------------- ORDERS ------------------------------ #
# ------------------------------------------------------------------- #
# ------------------------------------------------------------------- #

class NewOrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        
        labels = {
            'client': 'Selecione o Cliente',
            'date': 'Data do Pedido',
            'status': 'Status do Pedido',
        }
        
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }

class OrderDetailForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'


# ------------------------------------------------------------------- #
# ------------------------------------------------------------------- #
# ---------------------------- SPENDING ----------------------------- #
# ------------------------------------------------------------------- #
# ------------------------------------------------------------------- #

class NewSpendingForm(ModelForm):
    class Meta:
        model = Spending
        fields = '__all__'

        labels = {
            'tipo': 'Selecione o tipo de gasto',
            'date': 'Data',
        }
        
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }

class NewPurchaseForm(ModelForm):
    class Meta:
        model = Purchase
        fields = '__all__'
        
        labels = {
            'date': 'Data da Compra',
        }
        
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }