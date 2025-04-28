from rest_framework import serializers
from .models import Pereval, TermsAgreement
from coordinates.serializers import CoordsSerializer
from photo.serializers import ImageSerializer
from tourist.serializers import TouristSerializer
from tourist.models import Tourist
from coordinates.models import Coords
from photo.models import Image


class PerevalSerializer(serializers.ModelSerializer):
    tourist = TouristSerializer()
    coords = CoordsSerializer()
    photo = ImageSerializer()
    terms_token = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Pereval
        fields = ['id', 'beauty_title', 'title', 'other_titles', 'connect',
                  'level', 'status', 'area', 'tourist', 'coords', 'photo', 'terms_token']
        read_only_fields = ['status']

    def validate_terms_token(self, value):
        try:
            agreement = TermsAgreement.objects.get(token=value)
            if not agreement.is_valid:
                raise serializers.ValidationError("Токен соглашения недействителен или уже использован")
        except TermsAgreement.DoesNotExist:
            raise serializers.ValidationError("Токен соглашения не найден")
        return value

    def create(self, validated_data):
        # Удаляем токен из данных перед созданием объекта
        validated_data.pop('terms_token', None)

        tourist_data = validated_data.pop('tourist')
        coords_data = validated_data.pop('coords')
        photo_data = validated_data.pop('photo')

        # Проверяем, существует ли турист с таким email
        tourist = None
        try:
            tourist = Tourist.objects.get(email=tourist_data['email'])
        except Tourist.DoesNotExist:
            tourist = Tourist.objects.create(**tourist_data)

        coords = Coords.objects.create(**coords_data)
        image = Image.objects.create(**photo_data)

        pereval = Pereval.objects.create(
            tourist=tourist,
            coords=coords,
            photo=image,
            **validated_data
        )

        return pereval


# Сериализатор для валидации входных данных при обновлении
class PerevalUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pereval
        fields = ['beauty_title', 'title', 'other_titles', 'connect', 'level', 'area']

    def validate(self, data):
        # Проверяем, что пользователь не пытается редактировать данные туриста
        if hasattr(self.initial_data, 'tourist'):
            raise serializers.ValidationError("Данные туриста редактировать запрещено")
        return data


class PerevalDetailSerializer(serializers.ModelSerializer):
    coords = CoordsSerializer()
    tourist = TouristSerializer(read_only=True)
    photo = ImageSerializer(read_only=True)

    class Meta:
        model = Pereval
        fields = '__all__'


class PerevalListSerializer(serializers.ModelSerializer):
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Pereval
        fields = ['id', 'title', 'beauty_title', 'status', 'created']