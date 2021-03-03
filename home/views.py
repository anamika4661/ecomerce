from django.shortcuts import render,redirect

# Create your views here.
from django.views.generic.base import View

from home.models import *

from django.contrib.auth.models import User
from django.contrib import messages,auth


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
            messages.error(request,'Username and password do not match.')
            return redirect('home:login')
    return render(request,'signin.html')
