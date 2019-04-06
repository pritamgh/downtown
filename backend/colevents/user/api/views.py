import json

from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import CustomUser, UserProfile
from fest.models import Fest, Event
from payment.models import Payment


class UserLogin(APIView):

    def post(self, request, format=None):

        requested_data = json.loads(request.body)

        user = CustomUser.objects.filter(email=requested_data['email'])

        if not user:
            email = requested_data['email']
            password = "default"
            fname = requested_data['firstName']
            lname = requested_data['lastName']
            provider = requested_data['provider']
            if provider == "GOOGLE":
                login_type = "G"
            elif provider == "FACEBOOK":
                login_type = "F"
            base_user = CustomUser(username=email, email=email,
                                   password=password, first_name=fname,
                                   last_name=lname, is_organization=False)
            base_user.save()
            get_normaluser = CustomUser.objects.get(email=email)
            UserProfile.objects.filter(user=get_normaluser.id).update(
                social_auth_login_type=login_type)
        else:
            last_login = timezone.now()
            CustomUser.objects.filter(username=user[0].username).update(
                last_login=last_login)

        get_user = CustomUser.objects.get(email=requested_data['email'])
        get_user_profile = UserProfile.objects.get(user=get_user)
        fests_liked = get_user_profile.fest_liked.all()
        events_booked = Payment.objects.filter(email=requested_data['email'])

        fests_liked_data = []
        for fest_obj in fests_liked:
            get_fest = Fest.objects.get(id=fest_obj.id)
            fest = {
                "id": get_fest.id,
                "name": get_fest.name,
                # "image": get_fest.image,
                "date": get_fest.start_date,
            }
            fests_liked_data.append(fest)

        events_booked_data = []
        for obj in events_booked:
            get_event = Event.objects.get(id=obj.fest_id)
            event = {
                "id": get_event.id,
                "name": get_event.event_name,
                "ticket_id": "123",
                "ticket_price": get_event.ticket_price,
                "booking_date": obj.created.strftime('%Y-%m-%d'),
            }
            events_booked_data.append(event)

        result_set = {
            "liked_fests": fests_liked_data,
            "booked_events": events_booked_data,
        }

        return Response(result_set, status=status.HTTP_200_OK)


class FestDislike(APIView):

    def get(self, request, format=None):

        get_user = CustomUser.objects.get(email=request.GET['email'])
        get_user_profile = UserProfile.objects.get(user=get_user)
        fests_liked = get_user_profile.fest_liked.all()
        events_booked = Payment.objects.filter(email=request.GET['email'])

        fests_liked_data = []
        for fest_obj in fests_liked:
            get_fest = Fest.objects.get(id=fest_obj.id)
            fest = {
                "id": get_fest.id,
                "name": get_fest.name,
                # "image": get_fest.image,
                "date": get_fest.start_date,
            }
            fests_liked_data.append(fest)

        events_booked_data = []
        for obj in events_booked:
            get_event = Event.objects.get(id=obj.fest_id)
            event = {
                "id": get_event.id,
                "name": get_event.event_name,
                "ticket_id": "123",
                "ticket_price": get_event.ticket_price,
                "booking_date": obj.created.strftime('%Y-%m-%d'),
            }
            events_booked_data.append(event)

        result_set = {
            "liked_fests": fests_liked_data,
            "booked_events": events_booked_data,
        }

        return Response(result_set, status=status.HTTP_200_OK)
