"""myapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,patterns,include
from django.contrib import admin
from login.views import *

urlpatterns = patterns('',
    url(r'^admin/', admin.site.urls),
    url(r'^$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', logout_page),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'), # If user is not login it will redirect to login page
    url(r'^register/$', register),
    url(r'^register/success/$', register_success),
    url(r'^home/$', home),
    url(r'^home/CardMenu/$', CardMenu),
    url(r'^home/CardMenu/Addcard/$', Addcard),
    url(r'^home/CardMenu/Modifycard/$', Modifycard),
    url(r'^home/CardMenu/Modifycard/Modifycarddetails/$', Modifycarddetails),
    url(r'^home/AndroidGrid/$', AndroidGrid),
    url(r'^home/iOSGrid/$', iOSGrid),
    url(r'^home/ReferralConfig/$', ReferralConfig),
    url(r'^home/ReferralConfig/ReferralConfigVal/$', ReferralConfigVal),
    url(r'^AccessForbidden/$', AccessForbidden),
)


#urlpatterns = [
#    url(r'^admin/', admin.site.urls),
#    url(r'^login/', include('login.urls', namespace="login")),
#]
