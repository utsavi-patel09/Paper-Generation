from django.shortcuts import render ,redirect, HttpResponseRedirect
from paper.models.teacher import Teacher
from django.contrib.auth.hashers import make_password,check_password
from django.views import View




class Login(View):

    return_url = None
    def get(self,request):
        Login.return_url = request.GET.get('return_url')
        return render(request, 'login.html')

    def post(self,request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        teacher = Teacher.get_teacher(email)
        error_message = None
        if teacher:
            flag = check_password(password, teacher.password)
            if flag:

                request.session['teacher'] = teacher.id
                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)

                else:
                    Login.return_url = None
                    return redirect('generatepaper')
            else:
                error_message = "Email or Password invalid"
        else:
            error_message = "Email or Password invalid"
        return render(request, 'login.html', {'error': error_message})

def logout(request):
    request.session.clear()
    return redirect('homepage')