from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name = 'myapp'


urlpatterns = [
    url(r"^login/$", auth_views.LoginView.as_view(template_name="login.html"),name='login'),
    url(r"^logout/$", auth_views.LogoutView.as_view(), name="logout"),
    url(r"^signup/$", views.SignUp.as_view(), name="signup"),
    url(r"^drive/$", views.StartDrive, name="drive"),
    url(r"^addprofile/$", views.add_profile.as_view(), name="addprofile"),
    url(r"^mypro/$", views.MyProfile.as_view(), name="mypro"),

]
