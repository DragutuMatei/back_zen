from rest_framework import serializers
from .models import Podcast, Breath, Card, CustomUser, Another, Sound, YourModel, Meditation, Yoga

class YourModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = YourModel
        fields = '__all__'

class AnotherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Another
        fields = '__all__'
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email',)
        
class MeditationSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = Meditation
        # fields = ['tags', ]
        fields = '__all__'
        
               
class BreathSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breath
        fields = '__all__'
                      
class SoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sound
        fields = '__all__'

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'
        
class YogaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Yoga
        fields = '__all__'
        
class PodcastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Podcast
        fields = '__all__'