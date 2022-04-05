from django.db import models

# Create your models here.
# TODO O BANCO DE DADOS VAI FICAR AQUI, foda-se

class Client(models.Model):
    def __str__(self):
        return self.name
    # SELF FIELDS
    name = models.CharField(max_length=255)
    cpf = models.CharField(max_length=31, null=True, blank=True)
    date_of_creation = models.DateField(auto_now_add=True)
    class Meta:
        ordering = ['name']

class Phone(models.Model):
    # FOREIGN KEY
    client = models.OneToOneField(Client, on_delete=models.CASCADE)
    # SELF FIELDS
    number = models.CharField(max_length=31)
    description = models.CharField(max_length=127, null=True, blank=True)

class Address(models.Model):
    # FOREIGN KEY
    client = models.OneToOneField(Client, on_delete=models.CASCADE)
    # SELF FIELDs
    description = models.CharField(max_length=127, null=True, blank=True)
    number = models.CharField(max_length=15, null=True, blank=True)
    street = models.CharField(max_length=255, null=True, blank=True)
    district = models.CharField(max_length=127, null=True, blank=True)
    state = models.CharField(max_length=63, null=True, blank=True)
    postal_code = models.CharField(max_length=31, null=True, blank=True)
    latitude = models.CharField(max_length=31, null=True, blank=True)
    longitude = models.CharField(max_length=31, null=True, blank=True)

class Product(models.Model):
    def __str__(self):
        return self.title
    # SELF FIELDS
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    buy_value = models.FloatField()
    sell_value = models.FloatField()
    stock = models.IntegerField()
    is_active = models.BooleanField(default=True)
    class Meta:
        ordering = ['title']

class Order(models.Model):
    # FOREIGN KEY
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    # CHOICES
    STATUS = (
        (0, 'Encomendado'),
        (1, 'Separado'),
        (2, 'Saiu para Entrega'),
        (3, 'Entregue'),
    )
   
    # SELF DATA
    date = models.DateField(auto_now=False, null=False)
    status = models.IntegerField(choices = STATUS)


class OrderProductList(models.Model):
    # FOREIGN KEY
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    # SELF FIELDS
    amount = models.IntegerField()
    value = models.FloatField()


class Sale(models.Model):
    # FOREIGN KEY
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    # SELF FIELDS
    date = models.DateTimeField(auto_now=True)
    total_value = models.FloatField()
    liquid_value = models.FloatField()
    def __str__(self):
        return self.client.name
    class Meta:
        ordering = ['-date']


# PURCHASES

# Compras/Gastos Variáveis
class Spending(models.Model):
    CHOICES = (
        (0, 'Combustível'),
        (1, 'Reparos'),
        (2, 'Outros'),
    )
    description = models.TextField(null=True)
    value = models.FloatField(null=False)
    date = models.DateField(auto_now=False, null=False)
    tipo = models.IntegerField(choices = CHOICES)

    
class Purchase(models.Model):
    date = models.DateTimeField(auto_now=False)
    value = models.FloatField(null=False)

class PurchaseProductList(models.Model):
    # FOREIGN KEY
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    # SELF FIELDS
    amount = models.IntegerField()
    value = models.FloatField()



