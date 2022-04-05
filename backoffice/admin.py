from django.contrib import admin

# Register your models here.
from backoffice.models import *

admin.site.register(Product)
admin.site.register(OrderProductList)
admin.site.register(Order)
admin.site.register(Client)
admin.site.register(Address)
admin.site.register(Sale)
admin.site.register(Purchase)
admin.site.register(PurchaseProductList)
admin.site.register(Spending)
