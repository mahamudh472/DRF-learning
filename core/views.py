from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import PersonSerializer
from rest_framework import status, viewsets
from .models import Person

# Create your views here.

class PersonList(APIView):
    def get(self, request):
        persons = Person.objects.all()
        serializer = PersonSerializer(persons, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AnotherList(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer