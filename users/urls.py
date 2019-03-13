from . import views

urlpatterns = [
    path("auth/login/", views.Login.as_view(), name="login"),
    path("auth/signup/", views.SignUp.as_view(), name="signup"),
]
