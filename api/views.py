from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import ProjectSerializer
from projects.models import Project, Review

@api_view(['GET'])
def getProjects(request):
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getProject(request, pk):
    project = Project.objects.get(id=pk)
    serializer = ProjectSerializer(project)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def voteProject(request, pk):
    project = Project.objects.get(id=pk)
    user = request.user.profile
    data =request.data

    review, created = Review.objects.get_or_create(
        owner=user,
        project=project
    )
    review.value = data['value']
    review.save()
    project.getVoteCount

    serializer = ProjectSerializer(project)
    return Response(serializer.data)