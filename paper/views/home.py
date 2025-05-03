from django.shortcuts import render ,redirect

from django.views import View
class index(View):
    def get(selfself,request):

        return render(request, 'index.html')

