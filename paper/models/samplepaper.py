from django.db import models

class Samplepaper(models.Model):
    title = models.CharField(max_length=255)
    marks = models.IntegerField(default="0")
    description = models.CharField(max_length=100,default="")
    pdf_file = models.FileField(upload_to='pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
