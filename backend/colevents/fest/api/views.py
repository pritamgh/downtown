import json

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.response import Response

from ..models import Fest, Event, Sponsor
from user.models import CustomUser, UserProfile
from organization.models import Organization

from .serializers import (
    FestSerializer,
)


class HomePage(APIView):
	""" Most recent and most popular events
	usage: home page & also works for fest list page """

	def get(self, request, format=None):

		fests = Fest.objects.filter(fest_delete = False).order_by('-created').order_by('-total_likes')
		fest_list = []
		for fest in fests:
			org = Organization.objects.get(id = fest.organizer.id)
			fest_data = {
				"org_id": org.id,
				"org_type": org.type,
				"org_category": org.org_category,
				"org_name": org.name,
				"fest_id": fest.id,
				"fest_name": fest.name,
				"fest_image": fest.image,
				"fest_website": fest.website,
				"fest_start_date": fest.start_date.strftime('%Y-%m-%d'),
				"total_likes": fest.total_likes
			}
			fest_list.append(fest_data)
		return Response(fest_list, status=status.HTTP_200_OK)


class FestDetails(ListAPIView):
	""" Individual Fest details """

	serializer_class = FestSerializer

	def get_queryset(self):
		queryset = Fest.objects.all()
		fest_id = self.request.query_params.get('festid', None)
		if fest_id is not None:
		    queryset = queryset.filter(id = fest_id)
		return queryset


class FestCreate(APIView):

	def post(self, request, format=None):

		requested_data = json.loads(request.body)
		
		username = requested_data[0]["userid"]
		get_user = CustomUser.objects.get(username = username)
		get_org = Organization.objects.get(user = get_user)

		fest_name = requested_data[1]["name"]
		image = requested_data[1]["image"]
		start_date = requested_data[1]["start_date"]
		end_date = requested_data[1]["end_date"]
		website = requested_data[1]["website"]
		social_media_pages = requested_data[1]["social_media_pages"]

		promo_video = requested_data[1]["promo_video"]
		promo_video_thumbnail = requested_data[1]["promo_video_thumbnail"]

		events = requested_data[1]["event"]
		sponsors = requested_data[1]["event_sponser"]

		manager_email = requested_data[1]["manager_email"]
		manager_name = requested_data[1]["manager_name"]
		manager_phone = requested_data[1]["manager_phone"]

		sec_manager_name = requested_data[1]["sec_manager_name"]
		sec_manager_phone = requested_data[1]["sec_manager_phone"]

		account_holder_name = requested_data[1]["account_holder_name"]
		account_number = requested_data[1]["account_number"]
		ifsc = requested_data[1]["ifsc"]

		""" save events """
		event_list = []
		for event in events:
			name = event.get('eventName')
			rule = event.get('rule')
			ticket = event.get('ticket_price')
			e = Event.objects.create(
				event_name = name,
				event_rules = rule,
				ticket_price = ticket
			)
			e.save()
			event_list.append(e)

		""" save sponsor """
		sponsor_list = []
		for sponsor in sponsors:
			name = sponsor.get('evtSpnName')
			picture = sponsor.get('picture')
			caption = sponsor.get('caption')
			s = Sponsor.objects.create(
				sponsor_name = name,
				sponsor_picture = picture,
				caption = caption
			)
			s.save()
			sponsor_list.append(s)

		try:
			fest_obj = Fest(
				organizer = get_org,
				name = fest_name,
		        image = image,
		        start_date = start_date,
		        end_date = end_date,
		        website = website,
		        social_media_pages = social_media_pages,
		        promo_video = promo_video,
		        promo_video_thumbnail = promo_video_thumbnail,
		        manager_name = manager_name,
		        manager_phone = manager_phone,
		        manager_email = manager_email,
		        sec_manager_name = sec_manager_name,
		        sec_manager_phone = sec_manager_phone,
		        account_holder_name = account_holder_name,
		        account_number = account_number,
		        IFSC = ifsc,
		    )
			fest_obj.save()

			if fest_obj is None:
				for event in event_list:
					Event.objects.filter(id = event.id).delete()

			if fest_obj is None:
				for sponsor in sponsor_list:
					Sponsor.objects.filter(id = sponsor.id).delete()

			""" add events, sponsors into fest """
			fest_obj.events.add(*event_list)
			fest_obj.sponsor.add(*sponsor_list)

			return Response({"msg": "adding fest data successfully"}, 
				status=status.HTTP_201_CREATED)

		except Exception as e:
		    print(e)
		    return Response({"msg": "failed"}, status=status.HTTP_404_NOT_FOUND)


class FestUpdate(APIView):

	def post(self, request, format=None):

		requested_data = json.loads(request.body)

		username = requested_data[0]["userid"]
		get_user = CustomUser.objects.get(username = username)

		events = requested_data[1]["event"]
		for event in events:
			Event.objects.filter(id = event.get('id')).update(
				event_name = event.get('eventName'),
				event_rules = event.get('rule'),
				ticket_price = event.get('ticket_price')
			)

		sponsors = requested_data[1]["event_sponser"]
		for sponsor in sponsors:
			Sponsor.objects.filter(id = sponsor.get('id')).update(
				sponsor_name = sponsor.get('evtSpnName'),
				sponsor_picture = sponsor.get('picture'),
				caption = sponsor.get('caption') 
			)

		Fest.objects.filter(id = requested_data[1]["id"]).update(
			name = requested_data[1]["name"],
			image = requested_data[1]["image"],
			start_date = requested_data[1]["start_date"],
			end_date = requested_data[1]["end_date"],
			website = requested_data[1]["website"],
			social_media_pages = requested_data[1]["social_media_pages"],
			promo_video = requested_data[1]["promo_video"],
			promo_video_thumbnail = requested_data[1]["promo_video_thumbnail"],
			manager_email = requested_data[1]["manager_email"],
			manager_name = requested_data[1]["manager_name"],
			manager_phone = requested_data[1]["manager_phone"],
			sec_manager_name = requested_data[1]["sec_manager_name"],
			sec_manager_phone = requested_data[1]["sec_manager_phone"],
			account_holder_name = requested_data[1]["account_holder_name"],
			account_number = requested_data[1]["account_number"],
			IFSC = requested_data[1]["ifsc"]
		)

		return Response({"msg": "Updated"}, status=status.HTTP_200_OK)


class FestDelete(APIView):

	def delete(self, request, format=None):
		fest = Fest.objects.get(id = request.GET['festid'])
		events = fest.events.all()
		for event in events:
			e = Event.objects.get(id = event.id)
			e.delete()
		sponsors = fest.sponsor.all()
		for sponsor in sponsors:
			s = Sponsor.objects.get(id = sponsor.id)
			s.delete()
		fest.events.remove()
		fest.sponsor.remove()
		fest.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)


class FestLiked(APIView):

	def post(self, request, format=None):

		requested_data = json.loads(request.body)

		user_email = requested_data["email"]
		fest_id = requested_data["festData"].get("fest_id")
		like = requested_data["like"]

		get_user = CustomUser.objects.get(email = user_email)
		user_profile = UserProfile.objects.get(user = get_user)

		fest = Fest.objects.get(id = fest_id)

		total_likes = 0 if fest.total_likes is None else fest.total_likes
		if like == True:
			likes_add = total_likes + 1
			likes_count = likes_add
			user_profile.fest_liked.add(fest)
			msg = "Liked"
		else:
			likes_subtract = total_likes - 1
			likes_count = likes_subtract
			user_profile.fest_liked.remove(fest)
			msg = "Disliked"

		Fest.objects.filter(id = fest_id).update(total_likes = likes_count)

		return Response({"msg": msg}, status=status.HTTP_200_OK)
