from rest_framework import generics,viewsets
from microblog.models import Post
from microblog.api.serializers import PostSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

#class PostListView(generics.ListAPIView):
#    queryset = Post.published.all()
#    serializer_class = PostSerializer
#class PostDetailView(generics.RetrieveAPIView):
#    queryset = Post.published.all()
#    serializer_class = PostSerializer

#class ListPostView(APIView):
#    def get(self, request,format=None):
#        post = Post.objects.all()

#from rest_framework import viewsets


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.published.all()
    serializer_class = PostSerializer

    def retrieve (self, request, pk):
        post=self.get_object()
        serializer=PostSerializer (post)
        views=post.views.add(request.user) if request.user not in post.views.all() else ""
        return Response (serializer.data)
        
    @action(
              detail=True,
              methods=['get'],
              authentication_classes=[BasicAuthentication],
              permission_classes=[IsAuthenticated]
              )
    def like(self, request, *args, **kwargs):
        post = self.get_object()
        post.likes.add(request.user)
        return Response({'like': True})



#class PostList(APIView):
#    """
#    List all posts, or create a new post.
#    """
#    def get(self, request, format=None):
#        posts = Post.objects.all()
#        serializer = PostSerializer(posts, many=True)
#        return Response(serializer.data)

#    def post(self, request, format=None):
#        serializer = PostSerializer(data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data, status=status.HTTP_201_CREATED)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#class PostDetail(APIView):
#    """
#    Retrieve, update or delete a post instance.
#    """
#    def get_object(self, pk):
#        try:
#            return Post.objects.get(pk=pk)
#        except Post.DoesNotExist:
#            raise Http404

#    def get(self, request, pk, format=None):
#        post = self.get_object(pk)
#        serializer = SnippetSerializer(post)
#        return Response(serializer.data)

#    def put(self, request, pk, format=None):
#        snippet = self.get_object(pk)
#        serializer = PostSerializer(snippet, data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#    def delete(self, request, pk, format=None):
#        snippet = self.get_object(pk)
#        snippet.delete()
#        return Response(status=status.HTTP_204_NO_CONTENT)



#from rest_framework import generics


#class PostList(generics.ListCreateAPIView):
#    queryset = Post.published.all()
#    serializer_class = PostSerializer


#class PostDetail(generics.RetrieveUpdateDestroyAPIView):
#    queryset = Post.published.all()
#    serializer_class = PostSerializer