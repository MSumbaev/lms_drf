from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from education.models import Lesson, Course
from users.models import User


class LessonCreateTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='test@lms.com',
            password='test'
        )
        self.course = Course.objects.create(
            title='Test course',
            owner=self.user
        )

    def test_create_lesson(self):
        self.client.force_authenticate(user=self.user)

        data = {
            "title": "Test lesson",
            "description": "Test description",
            "link": "https://www.youtube.com/watch",
            "course": self.course.pk,
            "owner": self.user.pk
        }

        response = self.client.post(
            reverse('education:lesson_create'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.json(),
            {
                "id": 1,
                "title": "Test lesson",
                "preview": None,
                "description": "Test description",
                "link": "https://www.youtube.com/watch",
                "course": 1,
                "owner": 1
            }
        )


class LessonDestroyTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            email='test@test.com',
            password='test'
        )
        self.course = Course.objects.create(
            title='Test course',
            owner=self.user
        )
        self.lesson = Lesson.objects.create(
            title='Test lesson',
            description='Test description',
            link='https://www.youtube.com/watch',
            course=self.course,
            owner=self.user
        )

    def test_lesson_delete(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(
            reverse('education:lesson_delete',
                    args=[self.lesson.id])
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())


class LessonListTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='test@lms.com',
            password='test'
        )
        self.course = Course.objects.create(
            title='Test course',
            description='Test description',
            owner=self.user
        )
        self.lesson = Lesson.objects.create(
            title='Test lesson',
            description='Test description',
            link='https://www.youtube.com/watch',
            course=self.course,
            owner=self.user
        )

    def test_list_lesson(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            reverse('education:lesson_list'),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                    "count": 1,
                    "next": None,
                    "previous": None,
                    "results": [
                        {
                            "id": self.lesson.pk,
                            "title": "Test lesson",
                            "preview": None,
                            "description": "Test description",
                            "link": "https://www.youtube.com/watch",
                            "course": self.course.pk,
                            "owner": self.user.pk
                        }
                    ]
            }
        )


class LessonRetrieveTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='test@lms.com',
            password='test'
        )
        self.course = Course.objects.create(
            title='Test course',
            description='Test description',
            owner=self.user
        )
        self.lesson = Lesson.objects.create(
            title='Test lesson',
            description='Test description',
            link='https://www.youtube.com/watch',
            course=self.course,
            owner=self.user
        )

    def test_lesson_retrieve(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            reverse('education:lesson_get',
                    args=[self.lesson.id])
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.json(),
            {
                "id": self.lesson.pk,
                "title": "Test lesson",
                "preview": None,
                "description": "Test description",
                "link": "https://www.youtube.com/watch",
                "course": self.course.pk,
                "owner": self.user.pk
            }
        )


class LessonUpdateTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='test@lms.com',
            password='test'
        )
        self.course = Course.objects.create(
            title='Test course',
            description='Test description',
            owner=self.user
        )
        self.lesson = Lesson.objects.create(
            title='Test lesson',
            description='Test description',
            link='https://www.youtube.com/watch',
            course=self.course,
            owner=self.user
        )

    def test_lesson_update(self):
        self.client.force_authenticate(user=self.user)

        data = {
            'title': 'Lesson update',
            'description': 'Description update test',
            'link': 'https://www.youtube.com/watch_test_update'
        }

        response = self.client.patch(
            reverse('education:lesson_update',
                    args=[self.lesson.id]),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.json(),
            {
                "id": self.lesson.pk,
                "title": "Lesson update",
                "preview": None,
                "description": "Description update test",
                "link": "https://www.youtube.com/watch_test_update",
                "course": self.course.pk,
                "owner": self.user.pk
            }
        )
