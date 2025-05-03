from django.urls import path
from .views import home,signup,Login,samplepaper,static,generate
from django.conf import settings

urlpatterns = [

    path('', home.index.as_view(), name='homepage'),
    path('signup', signup.Signup.as_view(), name="signup"),
    path('login', Login.Login.as_view(), name="login"),
    path('logout', Login.logout, name="logout"),
    path('samplepaper', samplepaper.Samplepapers.as_view(), name="samplepaper"),
    path('about', static.About.as_view(), name="about"),
    path('profile', static.Profile.as_view(), name="profile"),
    path('contact', static.contact_view, name="contact"),
path('generatedpaper', samplepaper.Generatedpaper.as_view(), name="generatedpaper"),
path('generatepaper', generate.generate_pdf, name="generatepaper"),
]
