from django.urls import path

from .ai_views import AIAssistantView



urlpatterns = [

    path(
        "assistant/",
        AIAssistantView.as_view()
    ),

]