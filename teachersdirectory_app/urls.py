from django.urls import path
from . import views


urlpatterns = [
    path('',views.IndexPage,name = 'index'),
    path('teachers_view/',views.TeachersList,name='teachers_view'),
    path('teachers_list/',views.Dashboard,name='teachers_list'),
    path('create_teachers/',views.Createteachers,name = 'create_teachers'),
    path('view_profile/<int:pk>',views.ViewProfile,name='view_profile'),
    path('bulkimport/', views.BulkImporter,name='bulkimport'),
    path('search_results/',views.SearchData,name='search_results'),
    path('logout/',views.Logout,name='logout'),
]
