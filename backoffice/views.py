from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Sum
from django.db.models.functions import TruncMonth, ExtractMonth

from backoffice.models import *
from backoffice.forms import *

from datetime import datetime

# Create your views here.

@login_required(login_url="login")
def indexView(request):
    # ACTUAL MONTH AND YEAR
    currentMonth = datetime.now().month
    currentYear = datetime.now().year
    # GET MONTHLY SALES
    sales = Sale.objects.filter(
            date__year__gte=currentYear,
            date__month__gte=currentMonth,
        ).aggregate(earning = Sum('total_value'))['earning']
    if (sales):
        earning = '{:,.2f}'.format(sales)
    else:
        earning = 'Nenhum'
    
    # Cálculo do Lucro mensal
    liquid_sales = Sale.objects.filter(
            date__year__gte=currentYear,
            date__month__gte=currentMonth,
        ).aggregate(earning = Sum('liquid_value'))['earning']
    if (liquid_sales):
        lucro = '{:,.2f}'.format(liquid_sales)
    else:
        lucro = 'Nenhum'
    # GET MONTHLY SPENDINGS
    spending = Spending.objects.filter(
            date__year__gte=currentYear,
            date__month__gte=currentMonth,
        ).aggregate(earning = Sum('value'))['earning']
    if (spending):
        spending = '{:,.2f}'.format(spending)
    else:
        spending = 'Nenhum'
    
    # Gráfico
    #meses = 
    #metrics = {
    #    'sales_sum': Sum('total_value'),
    #}
    #dados = Sale.objects.annotate(valor = Sum('total_value'), month=ExtractMonth('date')).values('month')
    #print(dados)
    context = {
        'vazio': 'vazio',
        'earning': earning,
        'spending': spending,
        'lucro': lucro,
    #    'dados': dados,
    }
    return render(request, "backoffice/dashboard.html", context)

def loginView(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Bem-vindo!")
            return redirect('/')
        else:
            messages.error(request, "Usuário e/ou Senha incorreto(s)")
            return redirect('/')
    else:
        return render(request, "backoffice/login.html")


# ------------------------------------------------------------------- #
# ------------------------------------------------------------------- #
# ---------------------------- CLIENTS ------------------------------ #
# ------------------------------------------------------------------- #
# ------------------------------------------------------------------- #


@login_required(login_url="login")
def newClientView(request):
    if request.method == 'POST':
        client_form = []
        phone_form = []
        address_form = []
        # GET CLIENT DATA FROM FORM
        client_form = {
            'name':request.POST['name'],
            'cpf':request.POST['cpf']
        }
        # GET PHONE DATA FROM FORM
        phone_form = {
            'number':request.POST['phone'],
            'description':request.POST['phone_description']
        }
        # GET ADDRESS DATA FROM FORM
        address_form = {
            'number':request.POST['number'],
            'street': request.POST['street'],
            'district': request.POST['district'],
            'city': request.POST['city'],
            'state': request.POST['state'],
            'postal_code': request.POST['postal_code'],
            'description': request.POST['address_description'],
            'latitude': request.POST['latitude'],
            'longitude': request.POST['longitude']
        }

        # CREATE CLIENT
        client = Client.objects.create(
            name = client_form['name'],
            cpf = client_form['cpf'], 
            )
        client.save()
        # CREATE PHONE
        phone = Phone.objects.create(
            client = client,
            number = phone_form['number'], 
            description = phone_form['description'], 
            )
        phone.save()
        # CREATE ADDRESS
        address = Address.objects.create(
            client = client,
            number = address_form['number'], 
            street = address_form['street'], 
            district = address_form['district'],
            state = address_form['state'], 
            postal_code = address_form['postal_code'], 
            description = address_form['description'],
            latitude = address_form['latitude'], 
            longitude = address_form['longitude'],
            )
        address.save()
        messages.success(request, "Cliente cadastrado!")
        return redirect('/')
        '''else:
            messages.error(request, 'Algum dado inválido!')
            return redirect('/new-client')
            '''
    
    return render(request, "backoffice/new-client.html")



@login_required(login_url="login")
def allClientsView(request):
    clients = Client.objects.all()
    context = {
        'clients':clients,
    }
    return render(request, "backoffice/all-clients.html", context)


@login_required(login_url="login")
def clientDetailView(request, pk):
    # LOAD DATA FROM ESPECIFIC CLIENT
    client = Client.objects.get(id = pk)
    address = Address.objects.get(client = client.id)
    # FORMS
    client_form = ClientDetailForm(instance=client)
    address_form = ClientAddressForm(instance=address)
    if request.method == 'POST':
        form = ClientDetailForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, "Client's info updated!")
            return redirect('/client-details/' + pk)
    context = {
        'client_form':client_form,
        'address_form':address_form,
        'client':client,
        }
    return render(request, "backoffice/client-details.html", context)


# ------------------------------------------------------------------- #
# ------------------------------------------------------------------- #
# ---------------------------- PRODUCTS ----------------------------- #
# ------------------------------------------------------------------- #
# ------------------------------------------------------------------- #

@login_required(login_url="login")
def allProductsView(request):
    products = Product.objects.all()
    total_amount = 0
    total_sell_value = 0
    total_buy_value = 0
    for product in products:
        total_amount += product.stock
        total_sell_value += product.stock * product.sell_value
        total_buy_value += product.stock * product.buy_value
    context = {
        'products':products,
        'total_amount':total_amount,
        'total_sell_value':total_sell_value,
        'total_buy_value':total_buy_value,

    }
    return render(request, "backoffice/all-products.html", context)

@login_required(login_url="login")
def productDetailView(request, pk):
    # LOAD DATA FROM ESPECIFIC PRODUCT
    product = Product.objects.get(id = pk)
    # FORMS
    product_form = ProductDetailForm(instance=product)
    if request.method == 'POST':
        form = ProductDetailForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Produto atualizado!")
            return redirect('/product-details/' + pk)
    context = {
        'product_form':product_form,
    }
    return render(request, "backoffice/product-details.html", context)

@login_required(login_url="login")
def newProductView(request):
    if request.method == 'POST':
        form = NewProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Produto Cadastrado!")
            return redirect('/')
    else:
        return render(request, "backoffice/new-product.html")

# ------------------------------------------------------------------- #
# ------------------------------------------------------------------- #
# ----------------------------- ORDERS ------------------------------ #
# ------------------------------------------------------------------- #
# ------------------------------------------------------------------- #

@login_required(login_url="login")
def allOrdersView(request):
    orders = Order.objects.all().order_by('-id')
    context = {
        'orders':orders,
    }
    return render(request, "backoffice/all-orders.html", context)

@login_required(login_url="login")
def orderDetailView(request, pk):
    # LOAD DATA FROM ESPECIFIC ORDER
    order = Order.objects.get(id = pk)
    client = Client.objects.get(id = order.client.id)
    address = Address.objects.get(client = client)
    products = OrderProductList.objects.filter(order = order)
    # FORMS
    order_form = OrderDetailForm(instance=order)
    if request.method == 'POST':
        form = OrderDetailForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, "Pedido atualizado!")
            return redirect('/order-details/' + pk)
    context = {
        'order_form':order_form,
        'address':address,
        'client':client,
        'order':order,
        'products':products,
    }
    return render(request, "backoffice/order-details.html", context)

@login_required(login_url="login")
def newOrderView(request):
    if request.method == 'POST':
        form = NewOrderForm(request.POST)
        if form.is_valid():
            new_order = form.save()
            products = request.POST.getlist('product')
            products_amount = request.POST.getlist('product_amount')
            # Cadastrar os produtos no product-list
            for i in range(len(products)):
                product = Product.objects.get(id = products[i])
                orderlist = OrderProductList.objects.create(
                    product = product,
                    order = new_order,
                    amount = int(products_amount[i]),
                    value = int(products_amount[i]) * product.sell_value,
                )
                orderlist.save()
                # Reduzir o produto do estoque
                product.stock -= int(products_amount[i])
                product.save()
                
            messages.success(request, "Pedido Cadastrado!")
            return redirect('/')
    else:
        # LOAD FORMS
        new_order_form = NewOrderForm()
        products = Product.objects.all()
        context = {
            'new_order_form':new_order_form,
            'products':products,
        }
        return render(request, "backoffice/new-order.html", context)



@login_required(login_url="login")
def generateOrderDelivery(request):
    # __lt = Lower than...
    orders = Order.objects.filter(status__lt = 2)
    produtos = OrderProductList.objects.filter(order__status__lt = 2).values('product__title').annotate(Sum('amount'))
    delivery = []
    for order in orders:
        # Product list
        plist = OrderProductList.objects.filter(order=order)
        total = 0.0
        for i in plist:
            total += i.value
        delivery.append([order, plist, total])
    context = {
        'delivery':delivery,
    }
    return render(request, "backoffice/generate-order-delivery.html", context)

#FUNCAO PARA MUDAR O STATUS DOS PEDIDOS
@login_required(login_url="login")
def changeOrderStatus(request):
    # Pegar os ids das vendas e apenas alterar o status
    for i in request.POST.getlist('orders'):
        order = Order.objects.get(id = i)
        order.status = 2
        order.save()
    return redirect("order-delivery")

@login_required(login_url="login")
def orderDelivery(request):
    # Seleciona os pedidos separados para entrega
    orders = Order.objects.filter(status = 2)
    # Seleciono os produtos que irao para o carro
    produtos = OrderProductList.objects.filter(order__status = 2).values('product__title').annotate(Sum('amount'))
    delivery = []
    for order in orders:
        # Product list
        plist = OrderProductList.objects.filter(order=order)
        total = 0.0
        for i in plist:
            total += i.value
        delivery.append([order, plist, total])
    context = {
        'delivery':delivery,
        'produtos':produtos,
    }
    return render(request, "backoffice/order-delivery.html", context)


# Finaliza um pedido
@login_required(login_url="login")
def orderDone(request):
    # Seleciona o pedido entregue
    order = Order.objects.get(id = request.POST['order'])
    # Altera o status do pedido
    order.status = 3
    # Acesso a lista de produtos para obter o valor bruto e o valor liquido
    plist = OrderProductList.objects.filter(order=order)
    buy_total = 0.0
    sell_total = 0.0
    for i in plist:
        product = Product.objects.get(id = i.product.id)
        sell_total += product.sell_value * i.amount
        buy_total += product.buy_value * i.amount
    # Registro a venda
    sale = Sale.objects.create(
        client = order.client,
        total_value = sell_total, 
        liquid_value = sell_total - buy_total,
        )
    # Salva as alteracoes
    order.save()
    sale.save()
    # Manda uma mensagem e volta a pagina
    messages.success(request, "Entrega Realizada")
    return redirect("order-delivery")

# Deleta um pedido
@login_required(login_url="login")
def orderDelete(request):
    # Seleciona o pedido
    order = Order.objects.get(id = request.POST['order'])
    # Acesso a lista de produtos para obter o valor bruto e o valor liquido
    plist = OrderProductList.objects.filter(order=order)
    for i in plist:
        # Pego o produto dentro da lista de produtos
        product = Product.objects.get(id = i.product.id)
        product.stock += i.amount
        product.save()
        # Deleto o objeto da lista de produtos
    # Deleto o pedido
    order.delete()
    # Manda uma mensagem e volta a pagina
    messages.success(request, "Pedido Deletado")
    return redirect("all-orders")

# ------------------------------------------------------------------- #
# ------------------------------------------------------------------- #
# ----------------------------- SALES ------------------------------- #
# ------------------------------------------------------------------- #
# ------------------------------------------------------------------- #
@login_required(login_url="login")
def allSalesView(request):
    sales = Sale.objects.all()
    context = {
        'sales':sales,
    }
    return render(request, "backoffice/all-sales.html", context)


# ------------------------------------------------------------------- #
# ------------------------------------------------------------------- #
# --------------------------- SPENDINGS ----------------------------- #
# ------------------------------------------------------------------- #
# ------------------------------------------------------------------- #

@login_required(login_url="login")
def allSpendingsView(request):
    spendings = Spending.objects.all().order_by('-date')
    context = {
        'spendings':spendings,
    }
    return render(request, "backoffice/all-spendings.html", context)

@login_required(login_url="login")
def newSpendingView(request):
    if request.method == 'POST':
        form = NewSpendingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Gasto Cadastrado!")
            return redirect('/')
    else:
        context = {
            'form':NewSpendingForm(),
        }
        return render(request, "backoffice/new-spending.html", context)


@login_required(login_url="login")
def newPurchaseView(request):
    if request.method == 'POST':
        form = NewPurchaseForm(request.POST)
        if form.is_valid():
            VALOR = 0
            new_purchase = form.save()
            products = request.POST.getlist('product')
            products_amount = request.POST.getlist('product_amount')
            products_value = request.POST.getlist('product_value')

            
            # Cadastrar os produtos no product-list
            for i in range(len(products)):
                product = Product.objects.get(id = products[i])

                valor_total = int(products_amount[i]) * float(products_value[i])
                VALOR += valor_total

                orderlist = PurchaseProductList.objects.create(
                    product = product,
                    purchase = new_purchase,
                    amount = int(products_amount[i]),
                    value = valor_total,
                )
                orderlist.save()
                # Aumentar o produto no estoque
                product.stock += int(products_amount[i])
                product.save()
            # salvar o valor da compra
            new_purchase.value = VALOR
            new_purchase.save()
                
            messages.success(request, "Compra Cadastrada!")
            return redirect('/')
    else:
        # LOAD FORMS
        new_purchase_form = NewPurchaseForm()
        products = Product.objects.all()
        context = {
            'new_purchase_form':new_purchase_form,
            'products':products,
        }
        return render(request, "backoffice/new-purchase.html", context)