from urllib import response
from django.shortcuts import render,redirect
from django.contrib.auth import *
import os
from django.core.paginator import *
import xlwt
import datetime
from django.http import HttpResponse
from django.template.loader import *
from django.db.models import Count,Sum
from xhtml2pdf import pisa
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from unicodedata import category
from .models import *
import random
from .models import Users
from django.contrib import messages
import datetime
from django.core.paginator import *
import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
import json
from django.http import JsonResponse
import razorpay
from django.contrib import messages
from twilio.rest import Client
from django.utils import timezone
from django.views.decorators.csrf  import csrf_exempt
import string
from django.db.models import Sum


otp_number  = ''
def index(request):

    data1=add_category.objects.all()
    if request.method=='POST':
        search = request.POST['search']
        print("hdsgajfhjkshdjasdhgklrahgkhkrdhagkjraehgjkrehnjgkhekjghke",search)
        if len(search) == 0:
            data=product.objects.all() 
            return render(request, 'index.html',{'data':data})
        data=product.objects.filter(product_name__icontains=search)
        return render(request, 'index1.html',{'data':data})
    a=product.objects.all()
    for i in a:
        i.price=i.actual_price_category
        i.save()
    now=datetime.datetime.now().strftime('%Y-%m-%d')
    print(now)
    products=product.objects.all()
    for k in products:
        try:
            p_offer=Product_offer.objects.get( start_date_and_time__lte=now,end_date_and_time__gte=now,product=k.id)
            try:
                c_offer=Category_offer.objects.get( start_date_and_time__lte=now,end_date_and_time__gte=now,Category=k.cat_id)
                if int(p_offer.discount_percentage) > int(c_offer.discount_percentage):
                    print("p_offer.discount_percentage > c_offer.discount_percentage",p_offer.discount_percentage,c_offer.discount_percentage)
                    calculating_discount=int(p_offer.discount_percentage)*k.actual_price_category/100
                    k.price=k.actual_price_category-calculating_discount
                    k.save()
                elif int(p_offer.discount_percentage) < int(c_offer.discount_percentage):
                    print("p_offer.discount_percentage < c_offer.discount_percentage",p_offer.discount_percentage,c_offer.discount_percentage)
                    calculating_discount=int(c_offer.discount_percentage)*k.actual_price_category/100
                    k.price=k.actual_price_category-calculating_discount
                    k.save()
                elif int(p_offer.discount_percentage) == int(c_offer.discount_percentage):
                    print("p_offer.discount_percentage == c_offer.discount_percentage",p_offer.discount_percentage,c_offer.discount_percentage)
                    calculating_discount=int(p_offer.discount_percentage)*k.actual_price_category/100
                    k.price=k.actual_price_category-calculating_discount
                    k.save()
            except:
                p_offer=Product_offer.objects.get( start_date_and_time__lte=now,end_date_and_time__gte=now,product=k.id)
                calculating_discount=int(p_offer.discount_percentage)*k.actual_price_category/100
                k.price=k.actual_price_category-calculating_discount
                k.save()
        except:
            try:
                c_offer=Category_offer.objects.get( start_date_and_time__lte=now,end_date_and_time__gte=now,Category=k.cat_id)
                calculating_discount=int(c_offer.discount_percentage)*k.actual_price_category/100
                k.price=k.actual_price_category-calculating_discount
                k.save()
            except:
                pass

    if 'user_id' in request.session:
        data=product.objects.all()[:8]
        return render(request, 'index1.html',{'data':data})
    data=product.objects.all()[:8]



    return render(request, 'index.html',{'data':data})


def user_login(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user=Users.objects.filter(username=username,password=password)
        if user:
            status=Users.objects.get(username=username,password=password)
            print(status.username,status.status)
            if status.status == True:
                if 'guest' in request.session:
                    guest = request.session['guest']
                    print(guest)
                    print('quest')
                    
                    gcart = CartGuestUser.objects.filter(user_session=guest)
                    for i in gcart:
                        cart = Cart()
                        cart.quantity = i.qty
                        cart.product_id = i.pid
                        cart.user_id = status
                        cart.save()
                    del request.session['guest']
                    gcart.delete()

                print("hi ajo",status.id)
                request.session['user_id']=status.id
                s=request.session.get('user_id')
                return redirect(index)
            else:
                return redirect(user_login)
            
        else:
            return render(request, 'user_login.html')
    return render(request, 'user_login.html')


def insert(request):
    if request.method =='POST':
        username =request.POST['username']
        email =request.POST['email']
        phone =request.POST['phone']
        password =request.POST['password']


        if username=='' or email=='' or phone=='' or password=='':
         return render(request,"signup.html")


        profile=Users.objects.create(username=username,password=password,phone=phone,email=email)
        profile.save()
        print("profile Saved")
        return redirect(user_login)   
    return render(request,'register.html')

@never_cache
def signout(request):
    logout(request)
    return redirect(index)

def products(request):
    data1=add_category.objects.all()
    if request.method=='POST':
        search = request.POST['search']
        print("hdsgajfhjkshdjasdhgklrahgkhkrdhagkjraehgjkrehnjgkhekjghke",search)
        if len(search) == 0:
            data=product.objects.all() 
            return render(request, 'products.html',{'data':data})
        data=product.objects.filter(product_name__icontains=search)
        return render(request, 'products.html',{'data':data})
    data=product.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(data, 12)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    if request.session.get('user_id'):
        return render(request,'products1.html',{'data':users,'data1':data1})
    return render(request,'products.html',{'data':users,'data1':data1})


def admin_login(request):
    users = Users.objects.all()

    if request.method == 'POST':
        username =request.POST['username']
        password =request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None and user.is_superuser:
              login(request,user)
              request.session['username'] =username
              return render(request,'admin_dash.html')
        else:
                return redirect('/admin_login/')
    else:
        return render(request,'admin_login.html') 
@never_cache
@login_required(login_url=admin_login)
def admin_dash(request):
    # cod_count=Payment.objects.filter(payment_method='COD')
    # paypal_count=Payment.objects.filter(payment_method='Paypal')
    # razorpay_count=Payment.objects.filter(payment_method='razorpay')
    # cod_payment_method_graph_data=cod_count
    # paypal_payment_method_graph_data=paypal_count
    # razorpay_payment_method_graph_data=razorpay_count

    users_count=Users.objects.all().count()




  
    
    return render(request,'admin_dash.html',{'users_count':users_count})

@never_cache
@login_required(login_url=admin_login)
def admin_logout(request):

    logout(request)
    

    return redirect(admin_login)        


@never_cache
@login_required(login_url=admin_login)
def admin_logout(request):

    logout(request)
    

    return redirect(admin_login)    

def otp(request):
    

    if request.method=='POST':
        global phone
        phone=str(request.POST.get('phone'))
        print("post success")
        print(phone)
        print()

        if Users.objects.filter(phone=phone).exists():
             print("if success")


        
             global otp_number
             otp_number=random.randint(1000,9999)
             account_sid = 'AC26f7fc1dc014b0ba70653b1d63569536'
             auth_token = '50799347b597e9e514ceb3f62f650138'
             client = Client(account_sid, auth_token)

             client.api.account.messages.create(
                                 body=otp_number,
                                 from_='+14793982895',
                                 to='+917012247797',
                             )
             print("otp success")

                
             return render(request,'smslogin.html')
        else:
            print("invalid user")
        
            return render(request,'otp.html',{'message':"invalid phone"})
            

    else:
        print("not post")
        return render(request,'otp.html')

def smslogin(request):
    
    if request.method=='POST':
        Otp1=request.POST.get('otp')
        print(Otp1,otp_number)
        if str(Otp1) == str(otp_number):

            print('eee')
            
            return render(request,'index1.html')
        else:

            return render(request,'smslogin.html',{'message':'invalid otp'})
    else: 


     return render(request,'smslogin.html') 



@never_cache
@login_required(login_url=admin_login)
def admin_userinfo(request):

    if request.method=='POST':
        search = request.POST['search']
        if len(search) == 0:
            data=Users.objects.all().order_by('id')
            page = request.GET.get('page', 1)
            paginator = Paginator(data, 10)
            try:
                users = paginator.page(page)
            except PageNotAnInteger:
                users = paginator.page(1)
            except EmptyPage:
                users = paginator.page(paginator.num_pages)
            return render(request, 'admin_userinfo.html',{'data':users})
        data=Users.objects.filter(username__icontains=search)
        page = request.GET.get('page', 1)
        paginator = Paginator(data, 10)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        return render(request, 'admin_userinfo.html',{'data':users})
    data=Users.objects.all().order_by('id')
    page = request.GET.get('page', 1)
    paginator = Paginator(data, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, 'admin_userinfo.html',{'data':users})
    # profile=Users.objects.all()
    # return render(request,'admin_userinfo.html',{'profile':profile})  


def block(request,id):
    data=Users.objects.get(id=id)
    data.status=False
    data.save()
    return redirect(admin_userinfo)

def unblock(request,id):
    data=Users.objects.get(id=id)
    data.status=True
    data.save()
    return redirect(admin_userinfo)   


@never_cache
@login_required(login_url=admin_login)
def admin_addproduct(request):
    if request.method=='POST':
        product_id = request.POST.get('p_id')
        product_name = request.POST.get('p_name')
        p_description = request.POST.get('p_description')
        price = request.POST.get('pric')
        print("price",price)
        ram = request.POST.get('ram')
        storage = request.POST.get('storage')
        c_id=request.POST.get('c_id')
        print("stock",c_id)
        stock=request.POST.get('stock')
        cat_id = add_category.objects.get(id=c_id)
        image1 = request.FILES.get('img1')
        image2 = request.FILES.get('img2')
        image3 = request.FILES.get('img3')
        image4 = request.FILES.get('img4')
        c=product.objects.create(product_id=product_id,product_name=product_name,p_description=p_description,actual_price=price,actual_price_category=price,price=price,stock=stock,ram=ram,storage=storage,cat_id=cat_id,image1=image1,image2=image2,image3=image3,image4=image4)
        c.save()
    data=add_category.objects.all()
    return render(request, 'admin_addproduct.html',{'data':data})    


@never_cache
@login_required(login_url=admin_login)
def admin_listproduct(request):
    if request.method=='POST':
        search = request.POST['search']
        print("hdsgajfhjkshdjasdhgklrahgkhkrdhagkjraehgjkrehnjgkhekjghke",search)
        if len(search) == 0:
            data=product.objects.all() 
            page = request.GET.get('page', 1)
            paginator = Paginator(data,6)
            try:
                users = paginator.page(page)
            except PageNotAnInteger:
                users = paginator.page(1)
            except EmptyPage:
                users = paginator.page(paginator.num_pages)
            return render(request,'list_product.html',{'data':users})
        data=product.objects.filter(product_name__icontains=search)
        return render(request, 'admin_listproduct.html',{'data':data})
    data=product.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(data,5)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request,'admin_listproduct.html',{'data':users})


@never_cache
@login_required(login_url=admin_login)
def updatepro(request,id):
    data1=product.objects.get(id=id)
    if request.method == 'POST':
        data2=product.objects.get(id=id)
        pro=product(id=id)
        pro.product_id = request.POST.get('p_id')
        pro.product_name = request.POST.get('p_name')
        pro.p_description = request.POST.get('p_description')
        pro.price = request.POST.get('price')
        pro.ram = request.POST.get('ram')
        pro.storage = request.POST.get('storage')
        pro.cat_id=data2.cat_id
        if len(request.FILES) != 0:
            pro.image1 = request.FILES.get('img1')
            pro.image2 = request.FILES.get('img2')
            pro.image3 = request.FILES.get('img3')
            pro.image4 = request.FILES.get('img4')
        pro.save()
    data=add_category.objects.all()
    return render(request,'updatepro.html',{'data':data,'data1':data1})

@never_cache
@login_required(login_url=admin_login)
def deletepro(request,id):
    data=product.objects.get(id=id)
    data.delete()
    return redirect(admin_listproduct)
            
   


@never_cache
@login_required(login_url=admin_login)    
def admin_addcategory(request):
    if request.method == 'POST':
        category = request.POST['category']
        print("hello",category)
        reg=add_category.objects.create(category_name=category)
        reg.save()
        messages.info(request,'Created successfully')
    return render(request,'admin_addcategory.html')

def filter_product(request,id):
    print(id)
    data1=add_category.objects.all()
    data=product.objects.filter(cat_id=id)
    page = request.GET.get('page', 1)
    paginator = Paginator(data, 1)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    if request.session.get('user_id'):
        return render(request,'products1.html',{'data':users,'data1':data1})
    return render(request,'products.html',{'data':users,'data1':data1})


def product_details(request,id):
    if request.method == "POST":
        if request.POST.get('cart_button'):
            if 'user_id' in request.session:
                user_id=request.session.get('user_id')
                cart_for_check=Cart.objects.filter(user_id=user_id,product_id=id)
                if cart_for_check:
                    cart_last=Cart.objects.get(user_id=user_id,product_id=id)
                    cart_last.quantity=int(cart_last.quantity)+1
                    cart_last.save()
                else:
                    product_id=id
                    quantity=1
                    data1=Users.objects.get(id=user_id)
                    data2=product.objects.get(id=product_id)
                    my_cart=Cart.objects.create(user_id=data1,product_id=data2,quantity=quantity)
                    my_cart.save()
            else:
                return redirect(add_cart_guest,id)
        if request.POST.get('wishlist_button'):
            if 'user_id' in request.session:
                user_id=request.session.get('user_id')
                product_id=id
                data1=Users.objects.get(id=user_id)
                data2=product.objects.get(id=product_id)
                my_wishlist=Wishlist.objects.create(user_table=data1,product_table=data2)
                my_wishlist.save()
            else:
                return redirect(user_login)
    data=product.objects.get(id=id)
    if 'user_id' in request.session:
        return render(request,'product_details1.html',{'data':data})
    return render(request,'product_details.html',{'data':data})

def add_cart_guest(request,pid):
    if 'guest' in request.session:
        prod = product.objects.get(id=pid)
        gcart = CartGuestUser()
        gcart.user_session = request.session['guest']
        gcart.pid = prod
        gcart.qty = 1
        gcart.save()
        print("no use")
    else:
        prod = product.objects.get(id=pid)
        S=10
        ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S)) 
        guser_session = str(ran)
        request.session['guest'] = guser_session
        gcart = CartGuestUser()
        gcart.user_session = guser_session
        gcart.pid = prod
        gcart.qty = 1
        gcart.save()
    return redirect(gcart_view)

def cart_update(request):
   print('cart')
   body = json.loads(request.body)
   cart = Cart.objects.get(id=body['cart_id'])
   cart.quantity = body['product_qty']
#    cart.total_price = body['total']
   cart.save()
   print("cart_test",body)
   print("update cart")
   return redirect(view_cart)    
    
def gcart_view(request):
    guser = request.session['guest']
    cart = CartGuestUser.objects.filter(user_session=guser)
    a=0                                                          
    for i in cart:
        a = a+i.pid.price*int(i.qty)
    if request.method == "POST":
        if cart:
            return redirect(checkout)
        else:
            return redirect(gcart_view)
    return render(request,'view_cart1.html',{'cart':cart,'total':a})

def gcart_update(request):
   body = json.loads(request.body)
   cart = CartGuestUser.objects.get(id=body['cart_id'])
   cart.qty = body['product_qty']
   cart.save()
   return redirect(gcart_view)

def gcart_remove(request,id):
    gcart = CartGuestUser.objects.get(id=id)
    gcart.delete()
    return redirect(gcart_view)       

def view_cart(request):
    if 'user_id' in request.session:
        id = request.session.get('user_id')
        cart=Cart.objects.filter(user_id=id)
        a=0                                                          
        for i in cart:
            a = a+i.product_id.price*int(i.quantity)
        if request.method == "POST":
            if cart:
                return redirect(checkout)
            else:
                return redirect(view_cart)
        return render(request,'view_cart.html',{'cart':cart,'total':a})
    return redirect(user_login)

def add_quantity(request,id):
    data=Cart.objects.get(id=id)
    data.quantity=int(data.quantity)+1
    data.save()
    return redirect(view_cart)

def sub_quantity(request,id):
    data=Cart.objects.get(id=id)
    f=int(data.quantity)
    if f != 1:
        data.quantity=int(data.quantity)-1
    else:
        pass
    data.save()
    return redirect(view_cart)

    

def delete_from_cart(request,id):
    data=Cart.objects.get(id=id)
    data.delete()
    return redirect(view_cart)

def checkout(request):
    if 'user_id' in request.session:
        id = request.session.get('user_id')
        cart=Cart.objects.filter(user_id=id)
        if cart:
            id = request.session.get('user_id')
            cart=Cart.objects.filter(user_id=id)
            a=0
            for i in cart:
                a = a+i.product_id.price*int(i.quantity)
            coupan_price=0
            total1=a
            if 'coupan_session' in request.session:
                coupan_id=request.session.get('coupan_session')
                request.session['not_valid']=coupan_id
                del request.session['coupan_session']
            if 'not_valid' in request.session:
                coupan_id=request.session.get('not_valid')
                coupan_obj=Coupan.objects.get(id=coupan_id)
                coupan_price=coupan_obj.discount_amount
                a=a - int(coupan_price)
            address=Address.objects.filter(user_id=id)
            if request.method=='POST':
                payment_method=request.POST['payment_method']
                selected_address_id=request.POST.get('selected_address')
                print("selected_Address_id",selected_address_id)
                request.session['address_session']=selected_address_id
                print("selected_address_id_using_session",request.session.get('address_session'))
                if payment_method == 'paypal':
                    return redirect(payment_methods,a)
                user_id = request.session.get('user_id')
                data1=Users.objects.get(id=user_id)
                reg=Payment()
                reg.user=data1
                if payment_method == 'COD':
                    reg.payment_method=payment_method
                    reg.status='pending'
                    if 'not_valid' in request.session:
                        user=data1.id
                        if 'not_valid' in request.session:
                            b=request.session.get('not_valid')
                            print("cod_coupan_id",b)
                            cou=Coupan_applied.objects.create(coupan=b,user=user)
                            cou.save()
                            del request.session['not_valid']
                reg.save()
                data=Order()
                data.user=data1
                data.payment=reg
                selected_address_id=request.session.get('address_session')
                print("rijin raju",selected_address_id)
                data.address=Address.objects.get(id=selected_address_id)
                yr = int(datetime.date.today().strftime('%Y'))
                dt = int(datetime.date.today().strftime('%d'))
                mt = int(datetime.date.today().strftime('%m'))
                d = datetime.date(yr,mt,dt)
                current_date = d.strftime("%Y%m%d") #20210305
                data.order_number = current_date + str(reg.id)
                data.order_total=a
                data.save()
                for i in cart:
                    data2=OrderProduct()
                    data2.order=data
                    data2.payment=reg
                    data2.user=data1
                    data2.product=product.objects.get(id=i.product_id.id)
                    data2.quantity=i.quantity
                    data2.product_price=i.product_id.price
                    data2.save()
                if payment_method == 'razorpay':
                    return redirect(payment_methods_razorpay, reg.pk) 
                for item in cart:
                    product1 = product.objects.get(id=item.product_id.id)
                    product1.stock -= int(item.quantity)
                    product1.save()                    
                cart.delete()
                return render(request,'order_successfully.html')
            return render(request,'checkout.html',{'cart':cart,'total':a,'address':address,'coupan_price':coupan_price,'total1':total1})
        else:
            return redirect(view_cart)
    else:
        return redirect(user_login)

def add_address(request):
    if request.method == "POST":
        user_id = request.session.get('user_id')
        buyer_name = request.POST['b_name']
        buyer_phone = request.POST['b_phone']
        address=request.POST['b_address']
        pincode=request.POST['b_pincode']
        city=request.POST['b_city']
        state=request.POST['b_state']
        country="india"
        reg=Address.objects.create(user_id=user_id,buyer_name=buyer_name,buyer_phone=buyer_phone,address=address,pincode=pincode,city=city,state=state,country=country)
        reg.save()
        return redirect(checkout)
    return render(request,'add_address.html')   

def view_wishlist(request):
    if 'user_id' in request.session:
        id = request.session.get('user_id')
        wishlist=Wishlist.objects.filter(user_table=id)
        return render(request,'view_wishlist.html',{'wishlist': wishlist})
    return redirect(login)

def delete_from_wishlist(request,id):
    data=Wishlist.objects.get(id=id)
    data.delete()
    return redirect(view_wishlist)

def myprofile(request):
    user_id=request.session.get('user_id')
    data=Users.objects.get(id=user_id)
    return render(request,'myprofile.html',{'data':data})

def address_management(request):
    user_id=request.session.get('user_id')
    data=Address.objects.filter(user_id=user_id)
    return render(request,"address_management.html",{'data':data})

def delete_address(request,id):
    data=Address.objects.get(id=id)
    data.delete()
    return redirect(address_management)

def edit_profile(request,id):
    data = Users.objects.get(id=id)
    if request.method=='POST':
        username = request.POST['username']
        email = request.POST['email']
        phone =request.POST['phone']
        password =request.POST['password']
        data_tb=Users.objects.get(id=id)
        data_tb.username=username
        data_tb.email=email
        data_tb.phone=phone
        data_tb.password=password
        data_tb.save()
        messages.info(request,'Updated successfully')
        return redirect(edit_profile,id)
    return render(request,"update.html",{'data':data})

def user_order_management(request):
    user_id=request.session.get('user_id')
    data=OrderProduct.objects.filter(user=user_id)
    for i in data:
        print(i.status)
    return render(request,'user_order_management.html',{'data':data})

def user_cancel_order(request,id):
    data=OrderProduct.objects.get(id=id)
    print("gfshjkghkshgbklrshk",data)
    data.ordered=True
    data.save()
    return redirect(user_order_management)



def user_order_detailed_view(request,id):
    data=OrderProduct.objects.get(id=id)
    return render(request,'user_order_detailed_view.html',{'i':data})

def payment_methods(request,order_total):
    if 'user_id' in request.session:
        id = request.session.get('user_id')
        cart=Cart.objects.filter(user_id=id)
        print("cart 123",cart)
        # order = Order.objects.get(payment_id=id)
        a= order_total
       
    return render(request,'paypal_checkout.html',{'cart':cart,'total':a})

def payment_confirm(request,order_total):
    if 'user_id' in request.session:
        id = request.session.get('user_id')
        cart=Cart.objects.filter(user_id=id)
        user_id = request.session.get('user_id')
        data1=Users.objects.get(id=user_id)
        body = json.loads(request.body)
        print("nothing to worry",body)
        reg=Payment()
        reg.user=data1
        reg.payment_id = body['transId']
        reg.payment_method = 'Paypal'
        reg.amount_paid = order_total
        reg.status= body['status']
        reg.save()
        if 'not_valid' in request.session:
            user=data1.id
            b=request.session.get('not_valid')
            print("cod_coupan_id",b)
            cou=Coupan_applied.objects.create(coupan=b,user=user)
            cou.save()
            del request.session['not_valid']
        data=Order()
        data.user=data1
        data.payment=reg
        selected_address_id=request.session.get('address_session')
        print("rijin raju",selected_address_id)
        data.address=Address.objects.get(id=selected_address_id)
        yr = int(datetime.date.today().strftime('%Y'))
        dt = int(datetime.date.today().strftime('%d'))
        mt = int(datetime.date.today().strftime('%m'))
        d = datetime.date(yr,mt,dt)
        current_date = d.strftime("%Y%m%d") #20210305
        data.order_number = current_date + str(reg.id)
        data.order_total=order_total
        data.save()
        for i in cart:
            data2=OrderProduct()
            data2.order=data
            data2.payment=reg
            data2.user=data1
            data2.product=product.objects.get(id=i.product_id.id)
            data2.quantity=i.quantity
            data2.product_price=i.product_id.price
            data2.save()  
        for item in cart:
            product1 = product.objects.get(id=item.product_id.id)
            product1.stock -= int(item.quantity)
            product1.save()                  
        cart.delete()
        data={
            'transId': reg.payment_id,
        }
        return JsonResponse(data)       

def payment_complete(request):
     return render(request,'order_successfully.html')

def payment_methods_razorpay(request,id):
    print(id)
    if 'razorpay_payment_for_order' in request.session:
        del request.session['razorpay_payment_for_order']
    if 'user_id' in request.session:
        usrr=request.session.get('user_id')
        user=Users.objects.get(id=usrr)
        order = Order.objects.get(payment_id=id)
        a= order.order_total

        client = razorpay.Client(auth=("rzp_test_LwvtAxokPKoVoO", "qOifWLiWmcQcfFjFmCOOUJVr"))

        data = { "amount": a*100, "currency": "INR", "receipt": "order_rcptid_11" }
        payment = client.order.create(data=data)
        print(payment)
        cart = OrderProduct.objects.filter(payment_id=id)
        print("cart 123",cart)
        request.session['razorpay_payment_for_order']=payment
        
    return render(request,'razorpay_checkout.html',{'cart':cart,'total':a,'Razorpay_payment_id':id,'order':order,'payment':payment})

@csrf_exempt
def razor_pay(request,id):
    if 'user_id' in request.session:
        order = Order.objects.get(payment_id=id)
        userid=request.session.get('user_id')
        user=Users.objects.get(id=userid)
        payment=request.session.get('razorpay_payment_for_order')
        pay = Payment.objects.get(id=id)
        pay.payment_method = 'razorpay'
        pay.status = payment['status']
        pay.payment_id = payment['id']
        pay.user = user
        actual_amount=payment['amount']
        actual_amount=actual_amount/100
        pay.amount_paid = actual_amount
        pay.save()
        cart1=Cart.objects.filter(user_id=userid)
        for item in cart1:
            product1 = product.objects.get(id=item.product_id.id)
            product1.stock -= int(item.quantity)
            product1.save()   
            cart1.delete()
        if 'razorpay_payment_for_order' in request.session:
            del request.session['razorpay_payment_for_order']
    return render(request,'order_successfully.html')

def user_order_returned(request,id):
    if 'user_id' in request.session:
        order= Order.objects.get(id=id)
        order.status = 'Returned'
        order.save()
    return redirect(user_order_management)


def apply_coupan(request):
    if 'user_id' in request.session:
        user=request.session.get('user_id')
        if request.method=='POST':
            coupan_code = request.POST['coupan_code']
            c=Coupan.objects.filter(coupan_code=coupan_code)
            if c:
                coupan=Coupan.objects.get(coupan_code=coupan_code)
                d=Coupan_applied.objects.filter(coupan=coupan.id,user=user)
                if d:
                    messages.info(request,'Already Applied Coupon Code')
                    return render(request,'apply_coupan.html')
                now = timezone.now()
                start_date_and_time=coupan.start_date_and_time
                if start_date_and_time < now:
                    if now < coupan.end_date_and_time:
                        coupan_id=coupan.id
                        print(coupan_code,coupan_id)
                        request.session['coupan_session']=coupan_id
                        return redirect(checkout)
                    else:
                        messages.info(request,'Coupon Expired')
                        return render(request,'apply_coupan.html')
                else:
                    messages.info(request,'Coupon is from coupan.start_date_and_time ')
                    return render(request,'apply_coupan.html')
            else:
                messages.info(request,'invalid Coupon Code')
                return render(request,'apply_coupan.html')        
        return render(request,'apply_coupan.html')
    else:
        return redirect(user_login)

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return

def download(request,productID):
    v=OrderProduct.objects.get(id=productID)
    mydict={
        'customerName':v.user.username,
        'customerEmail':v.user.email,
        'customerMobile':v.user.phone,
        'shipmentAddress':v.order.address.address,
        'orderStatus':v.status,
        'productimage':v.product.image1,
        'productName':v.product.product_name,
        'productPrice':v.product.price,
        'productDescription':v.product.p_description,
    }
    return render_to_pdf('download.html',mydict)




@never_cache
@login_required(login_url=admin_login)
def admin_order_management(request):
    data=OrderProduct.objects.filter(ordered=False)
    return render(request,'admin_order_management.html',{'data':data})



@never_cache
@login_required(login_url=admin_login)
def filter_order(request,status):
    data=OrderProduct.objects.filter(ordered=False,status=status)
    return render(request,'admin_order_management.html',{'data':data})


@never_cache
@login_required(login_url=admin_login)
def admin_cancel_order(request,id):
    data=OrderProduct.objects.get(id=id)
    data.ordered=True
    data.save()
    return redirect(admin_order_management)

@never_cache
@login_required(login_url=admin_login)
def admin_order_detailed_view(request,id):
    data=OrderProduct.objects.get(id=id)
    if request.method == 'POST':
        status=request.POST.get('status_update_adminside')
        print("status",status)
        data=OrderProduct.objects.get(id=id)
        if status == 'Out for Delivery':
            data.out_for_delivery = datetime.datetime.now()
        data.status=status
        data.save()
    return render(request,'admin_order_detailed_view.html',{'i':data})




    
def category_offer_management(request):
    if request.method=='POST':
        category_id = request.POST.get('c_code')
        category=add_category.objects.get(id=category_id)
        start_date_and_time = datetime.datetime.now()
        end_date_and_time = request.POST.get('e_date')
        discount_percentage = request.POST.get('d_percentage')
        a=Category_offer.objects.create(Category=category,start_date_and_time=start_date_and_time,end_date_and_time=end_date_and_time,discount_percentage=discount_percentage)
        a.save()
        messages.info(request,'Created successfully')       
    category=add_category.objects.all()
    return render(request,'category_offer_management.html',{'category':category})

@never_cache
@login_required(login_url=admin_login)
def product_offer_management(request):
    if request.method=='POST':
        product_id = request.POST.get('c_code')
        print('idhajkhbfkjd',product_id)
        product1=product.objects.get(id=product_id)
        start_date_and_time = datetime.datetime.now()
        end_date_and_time = request.POST.get('e_date')
        discount_percentage = request.POST.get('d_percentage')
        a=Product_offer.objects.create(product=product1,start_date_and_time=start_date_and_time,end_date_and_time=end_date_and_time,discount_percentage=discount_percentage)
        a.save()
        messages.info(request,'Created successfully')
    category=product.objects.all()
    return render(request,'product_offer_management.html',{'category':category})

@never_cache
@login_required(login_url=admin_login)    
def view_offers(request):
    product_offer = Product_offer.objects.all()
    category_offer=Category_offer.objects.all()
    return render(request,'offers.html',{'product':product_offer,'category':category_offer})


def delete_category_offer(request,id):
    print(id)
    Category_offer.objects.get(id=id).delete()
    return redirect(view_offers)

def delete_product_offer(request,id):
    print(id)
    Product_offer.objects.get(id=id).delete()
    return redirect(view_offers)    

@never_cache
@login_required(login_url=admin_login)
def coupan_management(request):
    if request.method=='POST':
        coupan_code = request.POST.get('c_code')
        start_date_and_time = request.POST.get('s_date')
        end_date_and_time = request.POST.get('e_date')
        discount_amount = request.POST.get('d_amount')
        maximum_usage = 0
        print(coupan_code,start_date_and_time,type(start_date_and_time),end_date_and_time,type(end_date_and_time),discount_amount,maximum_usage )
        a=Coupan.objects.create(coupan_code=coupan_code,start_date_and_time=start_date_and_time,end_date_and_time=end_date_and_time,discount_amount=discount_amount,maximum_usage=maximum_usage)
        a.save()
        messages.info(request,'Created successfully')
    return render(request,'coupan_management.html')


def view_coupan(request):
    categories = Coupan.objects.all()
    return render(request,'view_coupan.html',{'coupan':categories})    

def delete_coupan_offer(request,id):
    print(id)
    Coupan.objects.get(id=id).delete()
    return redirect(view_coupan)
    


@never_cache
@login_required(login_url=admin_login)
def view_category(request):
    categories = add_category.objects.all()
    return render(request,'view_category.html',{'cat':categories})

@never_cache
@login_required(login_url=admin_login)
def delete_category(request,id):
    print(id)
    add_category.objects.get(id=id).delete()
    return redirect(view_category)


@never_cache
@login_required(login_url=admin_login)
def sales_report_date(request):
    data = OrderProduct.objects.all()
    if request.method == 'POST':
        if request.POST.get('month'):
            month = request.POST.get('month')
            print(month)
            data = OrderProduct.objects.filter(created_at__icontains=month)
            
            if data:
                if SalesReport.objects.all():
                    SalesReport.objects.all().delete()
                    for i in data:
                        sales = SalesReport()
                        sales.productName = i.product.product_name
                        sales.categoryName = i.product.cat_id.category_name
                        sales.date = i.created_at
                        sales.quantity = i.quantity
                        sales.productPrice = i.product_price
                        sales.save()
                    sales = SalesReport.objects.all()
                    total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                    context = { 'sales':sales,'total':total['productPrice__sum']}
                    return render(request,'sales_report_.html',context)
                else:
                    for i in data:
                        sales = SalesReport()
                        sales.productName = i.product.product_name
                        sales.categoryName = i.product.cat_id.category_name
                        sales.date = i.created_at
                        sales.quantity = i.quantity
                        sales.productPrice = i.product_price
                        sales.save()
                    sales = SalesReport.objects.all()
                    total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                    context = { 'sales':sales,'total':total['productPrice__sum']}
                    return render(request,'sales_report_.html',context)
            else:
                messages.warning(request,"Nothing Found!!")
        if request.POST.get('date'):
            date = request.POST.get('date')
            print("0,",date)
            
            date_check = OrderProduct.objects.filter(created_at__icontains=date)
            print(date_check)
            if date_check:
                if SalesReport.objects.all():
                    SalesReport.objects.all().delete()
            
                    for i in date_check:
                        sales = SalesReport()
                        sales.productName = i.product.product_name
                        sales.categoryName = i.product.cat_id.category_name
                        sales.date = i.created_at
                        sales.quantity = i.quantity
                        sales.productPrice = i.product_price
                        sales.save()
                    sales = SalesReport.objects.all()
                    total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                    context = { 'sales':sales,'total':total['productPrice__sum']}
                    return render(request,'sales_report_.html',context)
                else:
                    for i in date_check:
                        sales = SalesReport()
                        sales.productName = i.product.product_name
                        sales.categoryName = i.product.cat_id.category_name
                        sales.date = i.created_at
                        sales.quantity = i.quantity
                        sales.productPrice = i.product_price
                        sales.save()
                    sales = SalesReport.objects.all()
                    total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                    context = { 'sales':sales,'total':total['productPrice__sum']}
                    return render(request,'sales_report_.html',context)
            else:
                messages.warning(request,"Nothing Found!!")
        if request.POST.get('date1'):
            date1 = request.POST.get('date1')
            date2 = request.POST.get('date2')
            data_range = OrderProduct.objects.filter(created_at__gte=date1,created_at__lte=date2)
            if data_range:
                if SalesReport.objects.all():
                    SalesReport.objects.all().delete()
            
                    for i in data_range:
                        sales = SalesReport()
                        sales.productName = i.product.product_name
                        sales.categoryName = i.product.cat_id.category_name
                        sales.date = i.created_at
                        sales.quantity = i.quantity
                        sales.productPrice = i.product_price
                        sales.save()
                    sales = SalesReport.objects.all()
                    total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                    context = { 'sales':sales,'total':total['productPrice__sum']}
                    return render(request,'sales_report_.html',context)
                else:
                    for i in data_range:
                        sales = SalesReport()
                        sales.productName = i.product.product_name
                        sales.categoryName = i.product.cat_id.category_name
                        sales.date = i.created_at
                        sales.quantity = i.quantity
                        sales.productPrice = i.product_price
                        sales.save()
                    sales = SalesReport.objects.all()
                    total = SalesReport.objects.all().aggregate(Sum('productPrice'))
                    context = { 'sales':sales,'total':total['productPrice__sum']}
                    return render(request,'sales_report_.html',context)
            else:
                messages.warning(request,"Nothing Found!!")
    if data:
        if SalesReport.objects.all():
            SalesReport.objects.all().delete()
            for i in data:
                sales = SalesReport()
                sales.productName = i.product.product_name
                sales.categoryName = i.product.cat_id.category_name
                sales.date = i.created_at
                sales.quantity = i.quantity
                sales.productPrice = i.product_price
                sales.save()
            sales = SalesReport.objects.all()
            total = SalesReport.objects.all().aggregate(Sum('productPrice'))
            context = { 'sales':sales,'total':total['productPrice__sum']}
            return render(request,'sales_report_.html',context)

        else:
            for i in data:
                sales = SalesReport()
                sales.productName = i.product.product_name
                sales.categoryName = i.product.cat_id.category_name
                sales.date = i.created_at
                sales.quantity = i.quantity
                sales.productPrice = i.product_price
                sales.save()
            sales = SalesReport.objects.all()
            total = SalesReport.objects.all().aggregate(Sum('productPrice'))
            context = { 'sales':sales,'total':total['productPrice__sum']}
            return render(request,'sales_report_.html',context)
        
    else:
        messages.warning(request,"Nothing Found!!")
    
    return render(request,'sales_report_.html')





    






























    

@never_cache
@login_required(login_url=admin_login)
def export_to_excel(request):
    response = HttpResponse(content_type = 'application/ms-excel')
    response['content-Disposition'] = 'attachment; filename="sales.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Sales Report') #this will generate a file named as sales Report

     # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Product Name','Category','Price','Quantity', ]

    for col_num in range(len(columns)):
        # at 0 row 0 column
        ws.write(row_num, col_num, columns[col_num], font_style)

    
    font_style = xlwt.XFStyle()
    total = 0

    rows = SalesReport.objects.values_list(
        'productName','categoryName', 'productPrice', 'quantity')
    for row in rows:
        total +=row[2]
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    row_num += 1
    col_num +=1
    ws.write(row_num,col_num,total,font_style)

    wb.save(response)

    return response

@never_cache
@login_required(login_url=admin_login)
def export_to_pdf(request):
    prod = product.objects.all()
    order_count = []
    # for i in prod:
    #     count = SalesReport.objects.filter(product_id=i.id).count()
    #     order_count.append(count)
    #     total_sales = i.price*count
    sales = SalesReport.objects.all()
    total_sales = SalesReport.objects.all().aggregate(Sum('productPrice'))



    template_path = 'sales_pdf.html'
    context = {
        'brand_name':prod,
        'order_count':sales,
        'total_amount':total_sales['productPrice__sum'],
    }
    
    # csv file can also be generated using content_type='application/csv
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response

