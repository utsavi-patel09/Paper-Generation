
from django.shortcuts import render ,redirect, HttpResponseRedirect
from django.views import View
from django.conf import settings
import os
from paper.models.samplepaper import Samplepaper
from paper.models.generatedpaper import GeneratedPaper
from paper.models.teacher import Teacher
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404


class Samplepapers(View):

    def get(self,request):
        pdfs = Samplepaper.objects.all()
        return render(request, 'samplepaper.html', {'pdfs': pdfs})

    def post(self,request):
        pdfs = Samplepaper.objects.all()
        return render(request, 'samplepaper.html', {'pdfs': pdfs})



class Generatedpaper(View):
    def get(self, request):
        teacher_id = request.session.get('teacher')
        papers = GeneratedPaper.get_paper_by_teacher(teacher_id)
        teacher = get_object_or_404(Teacher, id=request.session.get('teacher'))
        return render(request, "previous.html", {"papers": papers,"teacher": teacher})

    def post(self, request):
        paper_id = request.POST.get("paper_id")
        if paper_id:
            try:
                paper = GeneratedPaper.objects.get(id=paper_id)
                paper.delete()
            except GeneratedPaper.DoesNotExist:
                pass  # Optional: handle not found case
        teacher_id = request.session.get('teacher')
        papers = GeneratedPaper.get_paper_by_teacher(teacher_id)
        teacher = get_object_or_404(Teacher, id=request.session.get('teacher'))
        return render(request, "previous.html", {"papers": papers,"teacher": teacher})



