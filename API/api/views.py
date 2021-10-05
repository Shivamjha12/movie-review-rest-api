from django.shortcuts import render, HttpResponse
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from API.models import *
from API.api.serializers import *
from API.api.throttling import *
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.decorators import api_view
from API.api.permissions import *
# from snippets.models import Snippet
# from snippets.serializers import SnippetSerializer
from rest_framework import mixins
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.throttling import AnonRateThrottle,UserRateThrottle

class UserReview_filter(generics.ListAPIView):
    serializer_class = ReviewSerializer

    # def get_queryset(self,*args, **kwargs):
    #     username = self.kwargs['username']
    #     search_username = Reviews.objects.filter(review_by_user__username=username)
    #     return search_username

    def get_queryset(self,*args, **kwargs):
        queryset = Reviews.objects.all()
        username = self.request.query_params.get('username')
        if username is not None:
            queryset = queryset.filter(review_by_user__username=username)
        return queryset
        


class reviewsDetailsCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly]
    throttle_classes =[ReviewCreateThrottle]

    def get_queryset(self):
        return Reviews.objects.all()

    def perform_create(self,serializer):
        pk = self.kwargs.get('pk')
        particular_movies_review = Movies.objects.get(pk=pk)

        review_by_user = self.request.user
        review_queryset = Reviews.objects.filter(movies=particular_movies_review, review_by_user=review_by_user)
        if review_queryset.exists():
            raise ValidationError('Already reviewed this movie')

        if particular_movies_review.no_of_reviews == 0:
            particular_movies_review.avg_review = serializer.validated_data['ratings']
        else:
            particular_movies_review.avg_review = (particular_movies_review.avg_review + serializer.validated_data['ratings'])/2
                # serializer.validated_data['ratings'])
           

        particular_movies_review.no_of_reviews = particular_movies_review.no_of_reviews + 1
        particular_movies_review.save()


        serializer.save(movies=particular_movies_review,review_by_user=review_by_user)

    
class reviewstList(generics.ListAPIView):
    # queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    # throttle_classes =[ReviewListThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['description', 'review_by_user__username','active']
    # permission_classes = [IsAuthenticatedOrReadOnly]
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Reviews.objects.filter(movies=pk)

class movies(generics.ListAPIView):
    queryset = Movies.objects.all()
    serializer_class = MovieSerializer
    # permission_classes = [IsAuthenticated]
    # throttle_classes =[ReviewListThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'movies','avg_review','platform__name']
    # permission_classes = [IsAuthenticatedOrReadOnly]
    # def get_queryset(self):
    #     pk = self.kwargs['pk']
    #     return Reviews.objects.filter(movies=pk)

class reviewsAll(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Reviews.objects.all()
    # permission_classes = [IsReviewUserOrReadOnly]
    serializer_class = ReviewSerializer

    # def get_queryset(self):
    #     pk = self.kwargs['pk']
    #     return Reviews.objects.get(pk=pk)
    

    

#  class reviewstList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
#     queryset = Reviews.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
# class reviewsDetails(mixins.RetrieveModelMixin,generics.GenericAPIView):
#     queryset =  Reviews.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)


class StreamingPlatformsAV(APIView):
    def get(self, request):
        platforms = StreamingPlatforms.objects.all()
        x= StreamingPlatformsSerializer(platforms, many=True,context={'request': request})
        return Response(x.data)
    
    def post(self, request):
        serializers = StreamingPlatforms.objects(data=request.data)
        if serializers.is_valid():
            serializers.save()
        else:
            return Response(serializers.errors)
class StreamingPlatformsDetailview(APIView):

    def get(self, request,pk,*args, **kwargs):
        try:
            platforms = StreamingPlatforms.objects.get(pk=pk)
            x = StreamingPlatformsSerializer(platforms,context={'request': request})
            return Response(x.data)
        except StreamingPlatforms.DoesNotExist:
            return Response({"Error": "Platform not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self,request):
        platforms = StreamingPlatforms.objects(data=request.data)
        if platforms.is_valid():
            platforms.save()
        else:
            return Response(serializers.errors)
            
    def put(self, request,pk,*args, **kwargs):
        platforms = StreamingPlatforms.objects.get(pk=pk)
        x = StreamingPlatformsSerializer(platforms,data = request.data)
        if x.is_valid():
            x.save()
            return Response(x.data)
        else:
            return Response(x.errors)

    def delete(self,request,pk,*args, **kwargs):
        platforms = StreamingPlatforms.objects.get(pk=pk)
        platforms.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class MovieListAV(APIView):
    permission_classes = [AdminOrReadOnly]
    # throttle_classes =[UserRateThrottle,AnonRateThrottle]
    throttle_classes =[ReviewListThrottle,AnonRateThrottle]
    def get(self, request, *args, **kwargs):
         movies = Movies.objects.all()
         x = MovieSerializer(movies,many=True)
         return Response(x.data)

    def post(self, request, *args, **kwargs):
        x = MovieSerializer(data = request.data)
        if x.is_valid():
            x.save()
            return Response(x.data)
        else:
            return Response(x.errors)

class MovieDetailAV(APIView):
    permission_classes = [AdminOrReadOnly]
    throttle_classes =[UserRateThrottle,AnonRateThrottle]

    def get(self, request,pk,*args, **kwargs):
        try:
            movies = Movies.objects.get(pk=pk)
            x = MovieSerializer(movies)
            return Response(x.data)
        except Movies.DoesNotExist:
            return Response({"Error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)


    def put(self, request,pk,*args, **kwargs):
        movies = Movies.objects.get(pk=pk)
        x = MovieSerializer(movies,data = request.data)
        if x.is_valid():
            x.save()
            return Response(x.data)
        else:
            return Response(x.errors)

    def delete(self,request,pk,*args, **kwargs):
        movies = Movies.objects.get(pk=pk)
        movies.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)








# Create your views here.
# @api_view(['GET', 'POST'])
# def movies_list(request):
#     if request.method == 'GET':
#       movies = Movies.objects.all()
#       x = MovieSerializer(movies,many=True)
#       return Response(x.data)
#     if request.method == 'POST':
#        x = MovieSerializer(data = request.data)
#        if x.is_valid():
#            x.save()
#            return Response(x.data)
#        else:
#            return Response(x.errors)


# @api_view(['GET','PUT','DELETE'])
# def movies_details(request,pk):
#     if request.method == 'GET':
#         try:
#              movies = Movies.objects.get(pk=pk)
#              x = MovieSerializer(movies)
#              return Response(x.data)
#         except Movies.DoesNotExist:
#             return Response({"Error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'PUT':
#         movies = Movies.objects.get(pk=pk)
#         x = MovieSerializer(movies,data = request.data)
#         if x.is_valid():
#             x.save()
#             return Response(x.data)
#         else:
#             return Response(x.errors)
        
#     if request.method == 'DELETE':
#         movies = Movies.objects.get(pk=pk)
#         movies.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
