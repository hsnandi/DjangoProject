from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.exceptions import NotFound, ValidationError
from .models import Client, Project
from .serializers import ClientSerializer, ProjectSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def create(self, request, *args, **kwargs):
        project_name = request.data.get('project_name')
        client_id = request.data.get('client')
        created_by_id = request.data.get('created_by')
        user_ids = request.data.get('users', [])

        if not (project_name and client_id and created_by_id):
            raise ValidationError("Required fields: 'project_name', 'client', and 'created_by'.")

        client = Client.objects.filter(id=client_id).first()
        if not client:
            raise NotFound("Client not found.")

        created_by = User.objects.filter(id=created_by_id).first()
        if not created_by:
            raise NotFound("Creator user not found.")

        project = Project.objects.create(
            project_name=project_name,
            client=client,
            created_by=created_by
        )

        if user_ids:
            users = User.objects.filter(id__in=user_ids)
            project.users.set(users)

        serializer = self.get_serializer(project)
        return Response(serializer.data)