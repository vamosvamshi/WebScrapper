from django.conf.urls import url
from basic_app import views

#Template tagging
app_name = "basic_app"

urlpatterns = [
    url(r'relative/$',views.relative,name='relative'),
    url(r'amazon/$',views.amazon,name='amazon'),
    url(r'bestbuy/$',views.bestbuy,name='bestbuy'),
    url(r'ebay/$',views.ebay,name='ebay'),
    url(r'google/$',views.google,name='google'),
    url(r'yahoo/$',views.yahoo,name='yahoo'),
]
