from django.shortcuts import render ,redirect
from paper.models.teacher import Teacher
from django.contrib.auth.hashers import make_password
from django.views import View

def validatecustomer(teacher):
    error_message=None
    if (not teacher.name):
        error_message = "frist name required"
    elif len(teacher.name) < 4:
        error_message = "First_name must be greater than 4 character"
    elif teacher.isexists():
        error_message = "Email Address Already Registered"

    return error_message


class Signup(View):
    def get(self,request):
        return render(request, 'signup.html')
    def post(self,request):
        postData = request.POST
        name = postData.get('name')
        email = postData.get('email')
        password = postData.get('password')
        phone = postData.get('phone')

        value = {'name': name,
                 'email': email,
                 'phone': phone,
                 }
        error_message = None

        teacher = Teacher(name=name,
                            email=email,
                            password=password,
                            phone=phone)

        error_message = validatecustomer(teacher)

        if not error_message:
            teacher.password = make_password(teacher.password)
            teacher.register()
            return redirect('homepage')

        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'signup.html', data)




