from django.urls import path 
from .views import home,lg,sign_up,log_out,travaux,mes_travaux,ajouter_travail,travail_details


app_name = 'app'

urlpatterns = [
    path('',home,name='home'),
    path('login/',lg,name="login"),
    path('signup/',sign_up,name="signup"),
    path('logout/',log_out,name="logout"),
    path('travaux/',travaux,name='travaux'),
    path('mestravaux/',mes_travaux,name='mestravaux'),
    path('ajoutertravail/',ajouter_travail,name='ajoutertravail'),
    path('details/<int:pk>',travail_details,name="travail_details" ),
]


