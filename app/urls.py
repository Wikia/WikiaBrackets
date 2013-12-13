from django.conf.urls import patterns, include, url
from app import views

urlpatterns = patterns('',
                       url(r'active_campaigns/?', views.active_campaigns),
                       url(r'campaign/(\d+)/?', views.campaign_data),
                       url(r'opponents/?', views.opponents),
                       url(r'vote/(\d+)/(\d+)/?', views.vote),
)
