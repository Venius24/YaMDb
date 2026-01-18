#serializers
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from django.core.validators import EmailValidator

User = get_user_model()


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, validators=[EmailValidator()])
    username = serializers.CharField(required=True, max_length=150)

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError("Имя пользователя 'me' запрещено.")
        return value

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')

        # Проверка уникальности (если пользователь уже есть, но это повторный запрос кода)
        user_by_username = User.objects.filter(username=username).first()
        user_by_email = User.objects.filter(email=email).first()

        if user_by_username and user_by_username.email != email:
            raise serializers.ValidationError("Этот username уже занят другим email.")
        if user_by_email and user_by_email.username != username:
            raise serializers.ValidationError("Этот email уже занят другим username.")
            
        return data

class TokenByCodeSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        confirmation_code = attrs.get('confirmation_code')

        try:
            # Ищем пользователя по username
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise AuthenticationFailed('Пользователь не найден')

        # Проверяем код (допустим, он в поле модели)
        if user.confirmation_code != confirmation_code:
            raise AuthenticationFailed('Неверный код подтверждения')

        # Если всё ок — генерируем токены
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }




#views
import uuid
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny


class SignUpView(APIView):
    permission_classes = [] # Доступно без токена

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        username = serializer.validated_data['username']
        
        # Создаем или получаем пользователя
        user, created = User.objects.get_or_create(username=username, email=email)
        
        # Генерируем код (6 цифр или короткий UUID)
        confirmation_code = str(uuid.uuid4())[:6] 
        
        # Сохраняем код пользователю (поле должно быть в модели)
        user.confirmation_code = confirmation_code
        user.save()

        # Отправка письма
        send_mail(
            'Ваш код подтверждения',
            f'Код: {confirmation_code}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class GetTokenByCodeView(TokenObtainPairView):
    permission_classes = [AllowAny] # Доступно без токена

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        confirmation_code = request.data.get('confirmation_code')
        
        user = authenticate(username=username, confirmation_code=confirmation_code)
        
        if user:
            refresh = self.get_token(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)