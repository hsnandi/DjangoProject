from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework.exceptions import NotFound  
from .models import Client, Project
from .serializers import ClientSerializer, ProjectSerializer

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def create(self, request, *args, **kwargs):
        # Handle assigning users to the project when creating it
        user_ids = request.data.get('users', [])
        project_name = request.data.get('project_name')
        client_id = request.data.get('client')
        created_by = request.data.get('created_by')


        try:
            client = Client.objects.get(id=client_id)
        except Client.DoesNotExist:
            raise NotFound(detail="Client not found.") #Exceptional Handling

        # Create the new project
        project = Project.objects.create(
            project_name=project_name,
            client=client,
            created_by=created_by
        )

        # Add users to the project
        users = User.objects.filter(id__in=user_ids)
        project.users.set(users)

        # Serialize the project and return the response
        serializer = self.get_serializer(project)
        return Response(serializer.data)
