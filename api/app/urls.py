from django.urls import path
from . import views


urlpatterns = [
    path('sentence/<type>', views.sentence),
    path('word/<type>', views.word),
    path('grammar/<type>', views.grammar),
    path('quiz/<type>', views.quiz),
    path('rasa/<type>', views.rasa),
    path('minimalPair/<type>', views.minimalPair),
]
