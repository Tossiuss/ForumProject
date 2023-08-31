from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .utils import send_activation_code, send_password
import random
import string
from django.contrib.auth.hashers import make_password



User = get_user_model()


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=4, required=True)
    password_confirm = serializers.CharField(min_length=4, required=True)
    name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=False)

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'Пользователь с таким email уже зарегистрирован'
            )
        return email

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError(
                'Пароли не совпадают'
            )
        return attrs
    
    def create(self, validated_data):
        # print(validated_data)
        user = User.objects.create_user(**validated_data)
        user.create_activation_code()
        send_activation_code(user.email, user.activation_code)        
        return user
    
    def to_representation(self, instance):
        return {"message": "Аккаунт успешно создан"}


class ActivationSerializer(serializers.Serializer):
    email = serializers.CharField()
    code = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('code')
        if not User.objects.filter(email=email, activation_code=code).exists():
            raise serializers.ValidationError(
                'Пользователь не найден'
            )
        return attrs
    
    
    def create(self, validated_data):
        user = User.objects.get(email=validated_data.get('email'))
        user.is_active = True
        user.activation_code = ''
        user.save()
        return user
    
    def to_representation(self, instance):
        return {"message": "Аккаунт активирован"}


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'Пользователь не найден'
            )
        return email
    
    def validate(self, attrs):
        request = self.context.get('request')
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(username=email,password=password, request=request)

            if not user:
                raise serializers.ValidationError(
                    'Не верный email или пароль'
                )
            
        else:
            raise serializers.ValidationError(
                'Email и password обязательны для заполнения'
            )
        
        attrs['user'] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(min_length=4, required=True)
    new_password = serializers.CharField(min_length=4, required=True)
    new_password_confirm = serializers.CharField(min_length=4, required=True)

    def validate_old_password(self, old_password):
        request = self.context.get('request')
        user = request.user
        if not user.check_password(old_password):
            raise serializers.ValidationError(
                'Введите корректный пароль'
            )
        return old_password
    
    def validate(self, attrs):
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')
        new_password_confirm = attrs.get('new_password_confirm')
        if new_password != new_password_confirm:
            raise serializers.ValidationError(
                'Пароли не совпадают'
            )
        if new_password == old_password:
            raise serializers.ValidationError(
                'Старый и новый пароли совпадают'
            )
        return attrs
    
    def set_new_password(self):
        new_password = self.validated_data.get('new_password')
        user = self.context.get('request').user
        user.set_password(new_password)
        user.save()


class LosePasswordSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'Пользователь не найден'
            )
        return email
    
    def unactivvate_user(self):
        user = User.objects.get(email=self.validated_data.get("email"))
        user.is_staff = False
        user.create_activation_code()

    def to_representation(self, instance):
        return {"message": "Проверьте почту"}


class LosePasswordCompleteSerializer(serializers.Serializer):
    activation_code = serializers.CharField(required=True)
    new_password = serializers.CharField(min_length=4, required=True)

    def validate_activation_code(self, activation_code):
        user = User.objects.filter(activation_code=activation_code, is_staff=False)
        if not user.exists():
            raise serializers.ValidationError('Пользователь не найден')
        return activation_code
    
    def save(self, **kwargs):
        user = User.objects.get(activation_code=self.validated_data.get('activation_code'), is_staff=False)
        user.is_staff = True
        user.activation_code = ''
        user.set_password(self.validated_data.get('new_password'))
        user.save()
        return user

    def to_representation(self, instance):
        return {"message": "Ваш пароль обновлен"}
