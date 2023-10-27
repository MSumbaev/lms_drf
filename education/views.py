from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from education.models import Course, Lesson, Payments, Subscription
from education.paginators import EducationPaginator
from education.permissions import IsNotModerator, IsOwner, IsModerator
from education.serializers import *


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    pagination_class = EducationPaginator

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_serializer_class(self):
        if self.action == 'create':
            return CourseCreateSerializer
        else:
            return CourseSerializer

    def list(self, request, *args, **kwargs):
        queryset = Course.objects.all()

        if not self.request.user.groups.filter(name='moderator'):
            queryset = queryset.filter(owner=self.request.user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(page, many=True)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated, IsNotModerator]
        elif self.action in ['retrieve', 'update', 'partial_update']:
            permission_classes = [IsAuthenticated, IsOwner | IsModerator]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsOwner | IsNotModerator]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsNotModerator]

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = EducationPaginator

    def get_queryset(self):
        queryset = super().get_queryset()

        if not self.request.user.groups.filter(name='moderator'):
            queryset = queryset.filter(owner=self.request.user.pk)

        return queryset


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsNotModerator]


class PaymentsCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        payment = serializer.save()
        payment.user = self.request.user

        if payment.course is not None:
            payment.amount = Course.objects.get(pk=payment.course.pk).price

        if payment.lesson is not None:
            payment.amount = Lesson.objects.get(pk=payment.lesson.pk).price

        print(self.request)
        payment.save()


class PaymentsListAPIView(generics.ListAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'payment_method')
    ordering_fields = ('date_of_payment',)
    permission_classes = [IsAuthenticated]


class SubscriptionCreateAPIView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    # Не работает!!!
    # def perform_create(self, serializer, **kwargs):
    #     subscription = serializer.save()
    #     subscription.user = self.request.user.id
    #     subscription.course = Course.objects.get(id=self.kwargs['pk']).id
    #     subscription.save()

    # Не работает!!!
    # def create(self, request, *args, **kwargs):
    #     new_subscription = Subscription(
    #         user=self.request.user,
    #         course=Course.objects.get(id=self.kwargs['pk'])
    #     )
    #     serializer = self.serializer_class(new_subscription, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        request.data.update(
            {
                'user': request.user.pk,
                'course': Course.objects.get(id=self.kwargs['pk']).pk
            }
        )
        return super(SubscriptionCreateAPIView, self).create(request, *args, **kwargs)


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Subscription.objects.filter(user=self.request.user.pk)
        return queryset

    def get_object(self, *args, **kwargs):
        queryset = self.get_queryset()

        obj = get_object_or_404(queryset, course_id=Course.objects.get(id=self.kwargs['pk']))
        self.check_object_permissions(self.request, obj)
        return obj
