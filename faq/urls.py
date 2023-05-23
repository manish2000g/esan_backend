from django.urls import path
from faq.views import CreateFAQ, UpdateFAQ, FAQList, DeleteFAQ

urlpatterns = [
    path('create-faq/', CreateFAQ, name='create_faq'),
    path('update-faq/', UpdateFAQ, name='update_faq'),
    path('faq-list/', FAQList, name='faq_list'),
    path('delete-faq/', DeleteFAQ, name='delete_faq'),
]
