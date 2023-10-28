from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from .models import *
from .serializers import *
from .tasks import *
import django_rq

class GetUserByName(APIView):
    def get(self, request, display_name):
        try:
            users = StackUser.objects.all().filter(display_name=display_name)
            results = StackUserSerializer(users, many=True).data
            return Response(results)
        except Exception as e:
            raise APIException(e)


class AddNewUser(APIView):
    def get(self, request, display_name, user_id):
        results = StackUserSerializer([{"display_name": display_name, "user_id": user_id}], many=True).data

        new_user = StackUser.objects.create(display_name=display_name, user_id=user_id)

        task_queue = django_rq.get_queue("default", autocommit=True, is_async=True)

        data = {"display_name": display_name, "user_id": user_id}

        task_queue.enqueue(task_execute, data)

        # task_execute.delay(name)

        return Response(results)
