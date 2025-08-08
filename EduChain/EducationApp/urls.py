from django.urls import path

from . import views

urlpatterns = [path("", views.index, name="index"),
		path("Register.html", views.Register, name="Register"),
		path("RegisterAction", views.RegisterAction, name="RegisterAction"),
	        path("StudentLogin.html", views.StudentLogin, name="StudentLogin"),
	        path("StudentLoginAction", views.StudentLoginAction, name="StudentLoginAction"),
		path("EducationLogin.html", views.EducationLogin, name="EducationLogin"),
		path("EducationLoginAction", views.EducationLoginAction, name="EducationLoginAction"),
		path("AccessData.html", views.AccessData, name="AccessData"),
		path("AccessDataAction", views.AccessDataAction, name="AccessDataAction"),
		path("ShareData.html", views.ShareData, name="ShareData"),
		path("ShareDataAction", views.ShareDataAction, name="ShareDataAction"),
		path("ViewData", views.ViewData, name="ViewData"),
		path("DownloadFileDataRequest", views.DownloadFileDataRequest, name="DownloadFileDataRequest"),
]