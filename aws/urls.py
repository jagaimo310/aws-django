from .import views
from django.urls import path

urlpatterns = [
    # 表示用
    path('main/', views.main),
    path('image/', views.image),
    path('past/', views.past),
    # mainからのフォーム処理
    path('prompt/', views.prompt),
    path('prompt/<int:prompt_id>/', views.prompt_recall),

]