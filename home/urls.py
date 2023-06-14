from django.urls import path,re_path
from . import views #manually added

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('about/', views.about, name='about'),
    path('profile/', views.profile, name='profile'),
    path('contact', views.contact, name='contact'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='login'),
    path('add-todo', views.add_task, name='add-todo'),
    path('delete-todo/<int:id>', views.delete_task, name='delete-todo'),
    path('done-todo/<int:id>', views.done_task, name='done-todo'),
    path('reset-todo/<int:id>', views.reset_task, name='reset-todo'),
    path('edit-todo/<int:id>', views.edit_task, name='edit-todo')
]