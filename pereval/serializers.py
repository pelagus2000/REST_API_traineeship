from rest_framework import serializers
from .models import Pereval
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

    class Meta:
        model = Pereval
        fields = ['id', 'beauty_title', 'title', 'other_titles', 'connect',
                  'level', 'status', 'area', 'tourist', 'coords', 'photo']
        read_only_fields = ['status']

    def create(self, validated_data):
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