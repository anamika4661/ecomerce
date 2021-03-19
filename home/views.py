from django.shortcuts import render,redirect

# Create your views here.
from django.views.generic.base import View

from home.models import *

from django.contrib.auth.models import User
from django.contrib import messages,auth
from django.core.mail import EmailMultiAlternatives


class BaseView(View):
    views = {}
    views['categories'] = category.objects.all()
    views['brands'] = brand.objects.all()

class HomeView(BaseView):
    def get(self,request):
        #self.views['categories'] = category.objects.all()
        self.views['slider'] = slider.objects.all()
        self.views['ads1'] = ad.objects.filter(rank = 1)
        self.views['ads2'] = ad.objects.filter(rank = 2)
        self.views['ads3'] = ad.objects.filter(rank = 3)
        self.views['ads4'] = ad.objects.filter(rank = 4)
        self.views['ads5'] = ad.objects.filter(rank = 5)
        self.views['ads6'] = ad.objects.filter(rank = 6)
        self.views['ads7'] = ad.objects.filter(rank = 7)
        self.views['ads8'] = ad.objects.filter(rank = 8)
        self.views['item'] = item.objects.all()
        self.views['new_items'] = item.objects.filter(label = 'new')
        self.views['hot_items'] = item.objects.filter(label='hot')
        self.views['sale_items'] = item.objects.filter(label='sale')
        return  render(request,'index.html',self.views)

class ProductDetailView(BaseView):
    def get(self,request,slug):
        category = item.objects.get(slug = slug).category
        self.views['detail_item'] = item.objects.filter(slug = slug)
        self.views['related_item'] = item.objects.filter(category=category)
        return render(request,'product-detail.html',self.views)

class searchview(BaseView):
    def get(self,request):
        query = request.GET.get('query',None)
        if not query:
            return redirect("/")
        self.views['search_query'] = item.objects.filter(
            description__icontains = query
        )
        self.views['searched_for'] = query
        return render(request,'search.html',self.views)
class categoryview(BaseView):
    def get(self,request,slug):
        cat= category.objects.get(slug=slug).id
        self.views['category_items'] = item.objects.filter(category = cat)

        return render(request,'category.html',self.views)
class brandview(BaseView):
    def get(self,request,name):
        cat= brand.objects.get(name=name).id
        self.views['brand_items'] = item.objects.filter(brand = cat)
        return render(request,'brand.html',self.views)

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if password == cpassword:
            if User.objects.filter(username = username).exists():
               messages.error(request,'the username already used.')
               return redirect('home:signup')
            elif User.objects.filter(email = email).exists():
                messages.error(request,'the email already used.')
                return redirect('home:signup')
            else:

                data = User.objects.create_user(
                    first_name = first_name,
                    last_name = last_name,
                    username = username,
                    email = email,
                    password = password
                )
                data.save()
        else:
            messages.error(request, 'the password is invalid.')
            return redirect('home:signup')

    return render(request,'signup.html')

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username,password = password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.error(request, 'the password is invalid.')
            return redirect('home:signin')
    return render(request,'signin.html')

class viewcart(BaseView):
    def get(self,request):
        self.views['carts'] = cart.objects.filter(user = request.user.username)
        return render(request,'cart.html',self.views)

def cart1(request, slug):
    if cart.objects.filter(slug = slug,user = request.user.username).exists():
        quantity = cart.objects.get(slug = slug,user = request.user.username).quantity
        quantity = quantity + 1
        price = item.objects.get(slug = slug).price
        discounted_price = item.objects.get(slug=slug).discounted_price
        if discounted_price > 0:
            total = discounted_price*quantity
        else:
            total = price * quantity

        cart.objects.filter(slug = slug).update(quantity =quantity,total= total)
    else:
        price = item.objects.get(slug=slug).price
        discounted_price = item.objects.get(slug=slug).discounted_price
        if discounted_price > 0:
            total = discounted_price
        else:
            total = price

        data = cart.objects.create(
            user = request.user.username,
            slug = slug,
            item = item.objects.filter(slug = slug)[0],
            total = total
        )
        data.save()
    return redirect('home:cart')

def deletecart(request,slug):
    if cart.objects.filter(slug=slug, user=request.user.username).exists():
        cart.objects.filter(slug=slug, user=request.user.username).delete()
        messages.success(request,'The item is deleted')
    return redirect("home:cart")


def cartminus(request, slug):
    if cart.objects.filter(slug=slug, user=request.user.username).exists():
        quantity = cart.objects.get(slug=slug, user=request.user.username).quantity
        quantity = quantity - 1
        price = item.objects.get(slug=slug).price
        discounted_price = item.objects.get(slug=slug).discounted_price
        if discounted_price > 0:
            total = discounted_price * quantity
        else:
            total = price * quantity

        cart.objects.filter(slug=slug).update(quantity=quantity, total=total)
    return redirect("home:cart")

def contactsave(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        subject = request.POST['subject']
        data = contact.objects.create(
            name = name,
            email = email,
            message = message,
            subject  = subject
        )
        data.save()
        # messages.success("data saved sucecssfully")
        html_content = f"<p> The customer name {name}, mail address {email} and subject {subject} have some message and the message is {message}"
        msg = EmailMultiAlternatives(subject,message,'anmpriya@gmail.com',['anmpriya@gmail.com'])
        msg.attach_alternative(html_content,"text/html")
        msg.send()
    return render(request,'contact.html')


