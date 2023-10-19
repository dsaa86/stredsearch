from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from search.models import *
from search.serializers import *

@api_view(['GET'])
def questionList(request, format=None):
    if request.method == 'GET':
        questions = StackQuestion.objects.all()
        serializer = StackQuestionSerializer(questions, many=True)
        return Response(serializer.data)