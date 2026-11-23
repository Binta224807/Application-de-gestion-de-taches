from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Task, Project


class AIAssistantView(APIView):

    permission_classes = [IsAuthenticated]


    def post(self, request):

        message = request.data.get(
            "message",
            ""
        ).lower()


        user = request.user


        # Données réelles Django

        total_tasks = Task.objects.filter(
            user=user
        ).count()


        completed_tasks = Task.objects.filter(
            user=user,
            status="done"
        ).count()


        pending_tasks = Task.objects.filter(
            user=user,
            status="todo"
        ).count()


        progress = 0

        if total_tasks > 0:
            progress = int(
                (completed_tasks / total_tasks) * 100
            )


        projects = Project.objects.filter(
            user=user
        ).count()


        overdue_tasks = Task.objects.filter(
            user=user,
            due_date__lt=request._request.date(),
        ).exclude(
            status="done"
        ).count()



        # Réponses intelligentes selon demande


        if "statistique" in message or "progression" in message:

            response = f"""
            Voici votre situation actuelle :

            - Tâches totales : {total_tasks}
            - Tâches terminées : {completed_tasks}
            - Tâches restantes : {pending_tasks}
            - Progression globale : {progress}%
            - Projets actifs : {projects}
            """


        elif "retard" in message:

            response = f"""
            Vous avez actuellement {overdue_tasks}
            tâche(s) en retard.
            """


        elif "organiser" in message or "planifier" in message:

            response = f"""
            Analyse :

            Vous avez {pending_tasks} tâche(s)
            en attente.

            Je vous conseille de commencer par
            les tâches prioritaires puis celles
            avec une date limite proche.
            """


        else:

            response = f"""
            Bonjour {user.username},

            J'ai analysé vos données :

            {total_tasks} tâches enregistrées,
            {completed_tasks} terminées,
            progression à {progress}%.


            Posez-moi une question sur vos tâches,
            vos projets ou votre organisation.
            """


        return Response({

            "response": response.strip(),

            "data": {

                "tasks": total_tasks,

                "completed": completed_tasks,

                "progress": progress,

                "projects": projects

            }

        })