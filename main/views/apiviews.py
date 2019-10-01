from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from main.models import *
from main.serializers import *


class BlockListAPIView(APIView):
    http_method_names = ['get', 'post']
    permission_classes = (IsAuthenticated,)

    def get_project(self, pk):
        return Project.objects.get(id=pk)

    def get(self, request, pk):
        project = self.get_project(pk)
        blocks = project.blocks.all()
        serializer = BlockSerializer(blocks, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = BlockSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(project_id=pk)
            return Response(serializer.data)
        return Response(serializer.errors)


class BlockDetailAPIView(APIView):
    http_method_names = ['get', 'put', 'delete']

    def get(self, request, pk):
        project = Block.objects.get(id=pk)
        serializer = BlockSerializer(project)
        return Response(serializer.data)

    def put(self, request, pk):
        project = Project.objects.get(id=pk)
        serializer = BlockSerializer(instance=project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        project = Block.objects.get(id=pk)
        project.delete()
        return Response(status=status.HTTP_200_OK)
