from django.shortcuts import render , HttpResponse , redirect
from django.views import View
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.mixins import LoginRequiredMixin


class Home(View):
    def get(self , request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return render(request , "core/home.html")


    def post(self , request):
        user = authenticate(username = request.POST['username'] , password=request.POST['password'])
        if user is not None:
            login(request , user)
            return redirect("dashboard")
        else :
            return render(request , "core/home.html" , {"error" : "کاربری با این مشخصات پیدا نشد"})


class Dashboard(LoginRequiredMixin , View):

    def get(self , request):
        return render(request,'core/dashboard/main.html')


class Logout(LoginRequiredMixin , View ):

    def get(self , request):
        logout(request)
        return redirect("home")