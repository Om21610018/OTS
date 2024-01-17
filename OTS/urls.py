from django.urls import path
from OTS.views import *
app_name='OTS'
urlpatterns=[
    path('',welcome),#landing page
    path('new-candidate',candidateRegistrationForm,name='registrationForm'),
    path('store-candidate',candidateRegistration,name='storeCandidate'),
    path('login',loginView,name='login'),
    path('home',candidateHome,name='userhome'),
    path('test-paper',testPaper,name='testpaper'),
    path('calculate-result',calculateTestResult,name='calculateTest'),
    path('test-history',testResultHistory,name='testHistory'),
    path('result',showTestResult,name='result'),
    path('logout',logoutView,name='logout'),

]