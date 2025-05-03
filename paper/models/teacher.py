from django.db import models

class Teacher(models.Model):
    name = models.CharField(max_length=50, default='')
    phone = models.CharField(max_length=15, default='')
    email = models.EmailField()
    password = models.CharField(max_length=500)
    profile_picture = models.ImageField(upload_to='teacher_profiles/', default='default_teacher.jpg')

    def register(self):
        self.save()


    @staticmethod
    def get_teacher(email):
        try:
            return Teacher.objects.get(email=email)
        except:
            return False

    def isexists(self):
        if Teacher.objects.filter(email=self.email):
            return True
        else:
            return False