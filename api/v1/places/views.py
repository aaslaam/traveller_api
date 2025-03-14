import datetime

from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny

from django.db.models import Q

from places.models import *
from api.v1.places.serializer import *
from api.v1.places.pagination import StandardResultSetPagination

@api_view(['GET'])
def places(request):
    instances = Place.objects.filter(is_deleted=False)
  
    
    q=request.GET.get("q")
    if q:
        ids = q.split(',')
        instances = instances.filter(category__in=ids)

    paginator = StandardResultSetPagination()
    paginated_result = paginator.paginate_queryset(instances, request)


    context = {
        "request": request   
    }
    serializer = PlaceSerializer(paginated_result, many=True, context=context)
    response_data = {
        "status": 3001,
        "count":paginator.page.paginator.count,
        "links":{
            "next": paginator.get_next_link(),
            "previous": paginator.get_previous_link()
        },
        "data": serializer.data
    }
    return Response(response_data)

@api_view(['GET'])
@permission_classes([AllowAny])
def place(request,pk):
    if Place.objects.filter(pk=pk).exists():
        instances = Place.objects.get(pk=pk)
        context = {
            "request": request   
        }
        serielizer = PlaceDetailSerializer(instances,context=context)
        respone_data = {
            "status": 3001,
            "data": serielizer.data
        }
        return Response(respone_data)
    else:
        return Response({
            "status": 3002,
            "message": "Place not found"
        })
    
@api_view (['GET'])
@permission_classes([IsAuthenticated])
def protected(request,pk):
    if Place.objects.filter(pk=pk).exists():
        instances = Place.objects.get(pk=pk)
        context = {
            "request": request   
        }
        serielizer = PlaceDetailSerializer(instances,context=context)
        respone_data = {
            "status": 3001,
            "data": serielizer.data
        }
        return Response(respone_data)
    else:
        return Response({
            "status": 3002,
            "message": "Place not found"
        })
    

@api_view (['POST'])
@permission_classes([IsAuthenticated])
def create_comment(request, pk):
    if Place.objects.filter(pk=pk).exists():
        place = Place.objects.get(pk=pk)
        comment = request.data['comment']
        try:
            parent_comment = request.data['parent_comment']
        except:
            parent_comment = None

        instance =  Comment.objects.create(
            place=place,
            user=request.user,
            comment=comment,
            date=datetime.datetime.now()
        )
        if parent_comment:
            if Comment.objects.filter(pk=parent_comment).exists():
                parent_comment = Comment.objects.get(pk=parent_comment)
            instance.parent_comment = parent_comment
            instance.save()

        respone_data = {
            "status": 3001,
            "message": "succesfully added"
        }
        return Response(respone_data)
    else:
        return Response({
            "status": 3002,
            "message": "Place not found"
        })
    
@api_view (['GET'])
@permission_classes([AllowAny])
def list_comment(request,pk):
    if Place.objects.filter(pk=pk).exists():
        place = Place.objects.get(pk=pk)
        instances = Comment.objects.filter(place=place,parent_comment=None)
        context = {
            "request": request   
        }
        serielizer = CommentSerializer(instances,context=context,many=True)
        respone_data = {
            "status": 3001,
            "data": serielizer.data
        }
        return Response(respone_data)
    else:
        return Response({
            "status": 3002,
            "message": "Place not found"
        })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_place(request, pk):
    if Place.objects.filter(pk=pk).exists():
        instance = Place.objects.get(pk=pk)
        if instance.likes.filter(username=request.user.username).exists():
            instance.likes.remove(request.user)
            message = "Unliked"
        else:
            instance.likes.add(request.user)  # Changed from like to likes
            message = "Liked"
            
        response_data = {
            "status": 3001,
            "message": message
        }
        return Response(response_data)
    
    return Response({
        "status": 3002,
        "message": "Place not found"
    })