from search.models import *
from search.serializers import *
from rest_framework import mixins
from rest_framework import generics


class QuestionList(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = StackQuestion.objects.all()
    serializer_class = StackQuestionSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    

class 