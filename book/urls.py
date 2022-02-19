from django.urls import path
from . import views

app_name = 'book'


urlpatterns = [
  path('download/<token_link>/',views.DownloadFileView.as_view(),name='download_file'),
  path('<int:book_id>/',views.DetailBookView.as_view(),name='detail'),
  path('', views.HomeView.as_view(), name='home'),
]
