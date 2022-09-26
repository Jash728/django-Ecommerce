from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    # path('category/<category>/', views.CatListView.as_view(), name='category'),

]

handler404 = 'app.views.error_404_view'
