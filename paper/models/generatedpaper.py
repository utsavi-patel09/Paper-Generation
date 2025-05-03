from django.shortcuts import render, redirect
from django.db import models
from . import Teacher

class GeneratedPaper(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)  # Associate with Teacher
    title = models.CharField(max_length=255)
    pdf_file = models.FileField(upload_to="generated_papers/")
    created_at = models.DateTimeField(auto_now_add=True)

    def register(self):
        self.save()

    def __str__(self):
        return f"{self.title} by {self.teacher.name}"

    def get_paper_by_teacher(teacher_id):
        return GeneratedPaper.objects.filter(teacher=teacher_id)

