from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from .models import *
from .serializers import *
from .tasks import *


class AddNewUser(APIView):
    def get(self, request, name):
        results = StackUserSerializer([{"name": name}], many=True).data

        new_user = StackUser.objects.create(name=name)

        return Response(results)
