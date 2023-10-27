import stripe
from django.conf import settings
from rest_framework import serializers

from education.models import Course, Lesson, Payments, Subscription
from education.validators import LinkValidator

stripe.api_key = settings.STRIPE_SECRET_KEY


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [LinkValidator(field='link')]


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.IntegerField(source='lesson_set.all.count', read_only=True)
    lessons = LessonSerializer(source='lesson_set.all', many=True, read_only=True)

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_is_subscribed(self, instance):
        request = self.context.get('request')

        if instance.subscription_set.filter(
            user=request.user,
            course=instance
        ):
            return True
        return False


class CourseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
        validators = [LinkValidator(field='description')]


class PaymentsSerializer(serializers.ModelSerializer):
    payment_data = serializers.SerializerMethodField()

    class Meta:
        model = Payments
        fields = '__all__'

    def get_payment_data(self, instance):
        if instance.stripe_id is not None:
            return stripe.PaymentIntent.retrieve(instance.stripe_id)
        elif instance.payment_method == 'transfer':
            return ['Оплата была произведена переводом до подключения stripe']
        else:
            return ['Оплата наличными']


class PaymentCreateSerializer(serializers.ModelSerializer):
    payment_data = serializers.SerializerMethodField()
    amount = serializers.IntegerField(read_only=True)

    class Meta:
        model = Payments
        fields = '__all__'

    def get_payment_data(self, instance):
        if instance.payment_method == 'cash':
            return ['Оплата наличными']
        elif instance.payment_method == 'transfer':
            pay = stripe.PaymentIntent.create(
                amount=instance.amount,
                currency='usd',
                automatic_payment_methods={'enabled': True,
                                           'allow_redirects': 'never'}
            )
            instance.stripe_id = pay['id']
            instance.save()

            return pay
