from django.urls import path
from faq.views import Create_FAQ, Update_FAQ, FAQList, delete_faq

urlpatterns = [
    path('create_faq/', Create_FAQ, name='create_faq'),
    path('update_faq/<int:pk>/', Update_FAQ, name='update_faq'),
    path('faq_list/', FAQList, name='faq_list'),
    path('delete_faq/<int:pk>/', delete_faq, name='delete_faq'),
]
