import json

from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from ..models import Organization
from user.models import CustomUser
from fest.models import Fest

from .serializers import (
    OrganizationSerializer,
)


class OrganizationList(ListAPIView):
    """
    GET:
    List up all organizations.
    """
    queryset = Organization.objects.filter(organization_delete=False)
    serializer_class = OrganizationSerializer
    filter_fields = ('type', 'name')


class OrganizationCreate(APIView):
    """
    POST:
    Create organization.
    """

    def post(self, request, format=None):

        requested_data = json.loads(request.body)
        print(requested_data)
        # print(request.data["image"])
        """ insert into base user """
        username = requested_data["org_id"]
        email = requested_data["org_id"]
        password = requested_data["org_password"]
        base_user = CustomUser(username=username,
                               email=email, is_normaluser=False)
        base_user.set_password(password)
        # base_user.save()

        get_org = CustomUser.objects.get(username=username)
        print("get organization", get_org.id)

        try:
            """ getting request data """
            org_type = requested_data['type']
            org_category = requested_data["org_category"]
            org_name = requested_data["name"]
            org_address = requested_data["address"]
            org_image = requested_data["image"]
            org_description = requested_data["description"]
            website = requested_data["website"]
            main_coordinator_name = requested_data["main_coordinator_name"]
            main_coordinator_phone = requested_data["main_coordinator_phone"]
            main_coordinator_email = requested_data["main_coordinator_email"]
            sub_coordinator_name = requested_data["sub_coordinator_name"]
            sub_coordinator_phone = requested_data["sub_coordinator_phone"]
            sub_coordinator_email = requested_data["sub_coordinator_email"]
            event_team = requested_data["team"]
            event_manager_name = requested_data["manager_name"]
            event_manager_phone = requested_data["manager_phone"]

            """ update & saving into organization table """
            Organization.objects.filter(user=get_org.id).update(
                type=org_type,
                org_category=org_category,
                name=org_name,
                address=org_address,
                image=org_image,
                description=org_description,
                website=website,
                main_coordinator_name=main_coordinator_name,
                main_coordinator_phone=main_coordinator_phone,
                main_coordinator_email=main_coordinator_email,
                sub_coordinator_name=sub_coordinator_name,
                sub_coordinator_phone=sub_coordinator_phone,
                sub_coordinator_email=sub_coordinator_email,
                team=event_team,
                manager_name=event_manager_name,
                manager_phone=event_manager_phone,
            )

            return Response({"msg": "adding organisation data successfully"},
                            status=status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return Response({"msg": "failed"},
                            status=status.HTTP_404_NOT_FOUND)


class OrganizationUpdate(APIView):
    """
    POST/PUT:
    Update/Edit Organization.
    """

    def post(self, request, format=None):

        requested_data = json.loads(request.body)

        username = requested_data[0]["userid"]
        get_user = CustomUser.objects.get(username=username)

        Organization.objects.filter(user=get_user).update(
            name=requested_data[1]["name"],
            address=requested_data[1]["address"],
            website=requested_data[1]["website"],
        )

        return Response({"msg": "Updated"}, status=status.HTTP_200_OK)


class OrganizationDashboard(APIView):
    """
    GET:
    Specific Organization Dashboard [Auth Mandatory].
    """

    def get(self, request, format=None):

        try:
            get_user = CustomUser.objects.get(username=request.GET['userid'])
            get_org = Organization.objects.get(user=get_user)

            org_data = {
                "name": get_org.name,
                "type": get_org.type,
                "category": get_org.org_category,
                "website": get_org.website,
                "address": get_org.address,
                "image": get_org.image
            }

            fest_list = Fest.objects.filter(organizer=get_org)
            fest_data = []
            for obj in fest_list:

                event_list = obj.events.all()
                event_data = []
                for eve_obj in event_list:
                    event = {
                        "id": eve_obj.id,
                        "event_name": eve_obj.event_name,
                        "event_rules": eve_obj.event_rules,
                        "ticket_price": round(eve_obj.ticket_price, 2)
                    }
                    event_data.append(event)

                sponsor_list = obj.sponsor.all()
                sponsor_data = []
                for sponsor_obj in sponsor_list:
                    sponsor = {
                        "id": sponsor_obj.id,
                        "sponsor_name": sponsor_obj.sponsor_name,
                        "sponsor_picture": sponsor_obj.sponsor_picture,
                        "caption": sponsor_obj.caption
                    }
                    sponsor_data.append(sponsor)

                fest = {
                    "id": obj.id,
                    "name": obj.name,
                    "image": obj.image,
                    "start_date": obj.start_date.strftime('%Y-%m-%d'),
                    "end_date": obj.end_date.strftime('%Y-%m-%d'),
                    "website": obj.website,
                    "social_media_pages": obj.social_media_pages,
                    "promo_video": obj.promo_video,
                    "promo_video_thumbnail": obj.promo_video_thumbnail,
                    "events": event_data,
                    "sponsor": sponsor_data,
                    "manager_name": obj.manager_name,
                    "manager_phone": obj.manager_phone,
                    "manager_email": obj.manager_email,
                    "sec_manager_name": obj.sec_manager_name,
                    "sec_manager_phone": obj.sec_manager_phone,
                    "account_holder_name": obj.account_holder_name,
                    "account_number": obj.account_number,
                    "IFSC": obj.IFSC
                }
                fest_data.append(fest)

            result_set = {
                "organization": org_data,
                "fest": fest_data
            }

            return Response(result_set, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"msg": "Data Not found"},
                            status=status.HTTP_404_NOT_FOUND)


class OrganizationLogin(APIView):
    """
    POST:
    SignIn/LogIn Organization.
    """

    def post(self, request, format=None):
        userid = request.data['email']
        password = request.data['password']
        user = authenticate(username=userid, password=password)
        if not user:
            return Response({"error": "Login failed"},
                            status=status.HTTP_401_UNAUTHORIZED)

        token, created = Token.objects.get_or_create(user=user)

        auth_data = {
            "user": user.username,
            "token": token.key
        }

        return Response(auth_data, status=status.HTTP_200_OK)
