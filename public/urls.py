from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
	path('',views.homepage,name="homepage"),
    path('createpublic/',views.newPublic,name="createPublic"),
    path('login/', views.user_login, name="user_login"),
    path('login/publicmenu/',views.publicmenu),
    path('login/newComp/',views.newCompliant),
    path('login/police/',views.caseDisplay),
    path('login/police/case/<int:postid>/',views.caseDetails),
    path('login/viewComp/',views.viewCompliant),
    path('login/viewComp/case/<int:postid>/',views.viewComplaintDetails),
    path('login/viewcriminal/',views.viewCriminals),
    path('login/viewunidentifiedbodies/',views.viewUnidentBodies),
    path('login/newMissingperson/',views.newMissingPerson),
    path('contact/',views.contact,name="contact"),
    path('login/police/case/<int:postid>/delete/<int:id>/',views.delete),
    path('login/police/case/<int:postid>/delete/<int:id>/public/case/',views.caseDisplay),
]
