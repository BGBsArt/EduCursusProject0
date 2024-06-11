from django.urls import path
from EduCursus import views

# <int:id> ---- Capturer l'id / Expression reguliere / identifiant numérique
urlpatterns = [
    path('', views.indexhome, name="indexhome"),
    path('register', views.register, name="register"),
    path('login', views.logIn, name="login"),
    path('logout', views.log0ut, name="logout"),
    path('adminLogin', views.adminLogin, name="adminLogin"),
    path('adminAdd', views.adminAdd, name="adminAdd"),
    path('adminPage/<int:id>/', views.adminPage, name = "adminPage"),
    path('activate/<uidb64>/<token>', views.activate, name="activate"),
    path('delete-student/<int:delete_id>/', views.delecteStud, name="delecteStud"),
    path('update-student/<int:update_id>/', views.updateData, name="updateData"),
    path('cursusInform/<int:id>/', views.cursusInform, name ="cursusInform"),
    path('nom_et_prenom/recherche/', views.search, name = "search"),
    path('recherche/standard/', views.searchStandard, name = "searchStandard"), 
    path('lookCursus/<str:nom>/<str:prenom>/', views.lookcursus, name="lookcursus"),
    path('adminConnecter/<int:user_id>/', views.adminconnecter, name="adminConnecter"),

]