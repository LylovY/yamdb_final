import uuid

from django.core.mail import send_mail
from django.db.models import Avg, F
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from reviews.models import Category, Genre, Review, Title
from users.models import User

from api_yamdb.settings import ADMIN_EMAIL

from .filters import TitleFilter
from .mixins import CreateListDestroyViewSet
from .permissions import (IsAdminOrReadOnly, IsAdminOrSuperuser,
                          IsAuthorOrAdminOrModerator)
from .serializers import (AuthExistUserSerializer, AuthNewUserSerializer,
                          CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          SelfUserSerializer, TitlePostSerializer,
                          TitleSerializer, UserSerializer, UserTokenSerializer)
from .utils import get_tokens_for_user


@api_view(['POST'])
def create_user_send_code(request):
    serializer = AuthExistUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    confirmation_code = uuid.uuid4().hex
    username = serializer.validated_data['username']
    email = serializer.validated_data['email']
    if User.objects.filter(username=username, email=email).exists():
        user = User.objects.get(username=username, email=email)
        message = confirmation_code
        user.code = confirmation_code
        user.save()
        send_mail(
            'Код подтверждения Yamdb',
            message,
            ADMIN_EMAIL,
            [email],
            fail_silently=False,
        )
        return Response('Код отправлен', status=status.HTTP_200_OK)
    serializer = AuthNewUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.validated_data['code'] = confirmation_code
    serializer.save()
    message = confirmation_code
    to_email = serializer.validated_data['email']
    send_mail(
        'Код подтверждения Yamdb',
        message,
        ADMIN_EMAIL,
        [to_email],
        fail_silently=False,
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_token(request):
    serializer = UserTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    code = serializer.validated_data['confirmation_code']
    if User.objects.filter(username=username, code=code).exists():
        user = User.objects.get(username=username, code=code)
        if user.is_superuser:
            user.role = User.ADMIN
        user.save()
        token = get_tokens_for_user(user)
        return Response({'token': token['access']})
    if User.objects.filter(username=username).exists():
        return Response('Неверный код', status=status.HTTP_400_BAD_REQUEST)
    return Response(
        'Пользователь не существует', status=status.HTTP_404_NOT_FOUND
    )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    search_fields = ('username',)
    permission_classes = (IsAdminOrSuperuser,)
    lookup_field = 'username'
    pagination_class = PageNumberPagination

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=(permissions.IsAuthenticated,),
        url_path='me',
    )
    def me_path(self, request):
        if request.method == 'GET':
            user = request.user
            serializer = SelfUserSerializer(user)
            return Response(serializer.data)
        if request.method == 'PATCH':
            user = request.user
            serializer = SelfUserSerializer(
                user, data=request.data, partial=True, many=False
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [
        IsAuthorOrAdminOrModerator,
    ]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        IsAuthorOrAdminOrModerator,
    ]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg(F('reviews__score')))
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleSerializer
        return TitlePostSerializer
