"""
URL configuration for tempotrek project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path # added re_path : https://medium.com/codex/deploying-react-through-djangos-static-files-part-1-dev-setup-8a3a7b93c809
from django.shortcuts import render # added ------------^


# added. 
#Normally you’d put the render_react function in some views.py file, 
# but I put it in urls.py for simplicity since I haven’t added an app to this project.
def render_react(request):
    return render(request, "index.html")

urlpatterns = [
    path("admin/", admin.site.urls),
    # added
    # server as catch-alls. if any other request doesn't match /admin will be redirected to react
    re_path(r"^$", render_react),
    re_path(r"^(?:.*)/?$", render_react)
]
