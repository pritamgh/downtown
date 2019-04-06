from rest_framework import serializers
from ..models import Fest, Event, Sponsor


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ('id', 'event_name', 'event_rules', 'ticket_price')


class SponsorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sponsor
        fields = ('id', 'sponsor_name', 'sponsor_picture', 'caption')


class FestSerializer(serializers.ModelSerializer):

    events = EventSerializer(many=True, read_only=True)
    sponsor = SponsorSerializer(many=True, read_only=True)

    class Meta:
        model = Fest
        fields = "__all__"
