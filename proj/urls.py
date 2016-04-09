from django.conf.urls import patterns, include, url
from django.contrib import admin
from vote import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),    
        ]

urlpatterns += views.LocalBake.patterns()
