from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from .models import *
from .serializers import *
from .tasks import *
import django_rq


class AddNewUser(APIView):
    def get(self, request, name):
        results = StackUserSerializer([{"name": name}], many=True).data

        new_user = StackUser.objects.create(display_name=name, user_id=123456)

        django_rq.enqueue(task_execute, name=name)

        # task_execute.delay(name)

        return Response(results)
