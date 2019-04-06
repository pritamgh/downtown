import hashlib
import json
import urllib.parse
import urllib.request

from random import randint

from django.conf import settings

from django.core.mail import EmailMessage
from django.shortcuts import render
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Payment
from fest.models import Event
from fest.models import Fest
from organization.models import Organization


def make_payment(email, first_name, last_name, contact, amount, host):
	posted={}
	posted["email"] = email
	posted["contact"] = contact
	posted["firstname"] = first_name
	posted["lastname"] = last_name
	posted["amount"] = amount
	posted["productinfo"] = 'Ticket Price'
	posted["surl"] = settings.HOST+'api/payment/Success/'
	posted["furl"] = settings.HOST+'api/payment/Failure/'
	posted["service_provider"] = 'payu_paisa'
	posted["curl"] = ''
	posted["address1"] = ''
	posted["address2"] = ''
	posted["city"] = ''
	posted["state"] = ''
	posted["country"] = ''
	posted["zipcode"] = ''
	posted["udf1"] = ''
	posted["udf2"] = ''
	posted["udf3"] = ''
	posted["udf4"] = ''
	posted["udf5"] = ''
	posted["udf6"] = ''
	posted["udf7"] = ''
	posted["udf8"] = ''
	posted["udf9"] = ''
	posted["udf10"] = ''
	posted["pg"] = ''

	return posted


# generate a random transaction Id.
def get_transaction_id():
    hash_object = hashlib.sha256(str(randint(0,9999)).encode("utf-8"))
    txnid = hash_object.hexdigest().lower()[0:32]
    return txnid


class PaymentGateway(APIView):

	def post(self, request, format=None):

		requested_data = json.loads(request.body)

		first_name = requested_data['firstname']
		last_name = requested_data['lastname']
		email = requested_data['email']
		fest_id = requested_data['fest_id']
		event_id = requested_data['event_id']
		amount = float(requested_data['ticket_price'])
		amount = str(amount)
		host = requested_data['host']
		contact = requested_data['mobile']

		posted = make_payment(email, first_name, last_name, contact, amount, host)

		""" PayU credentials of Aditya """
		MERCHANT_KEY = "mEbZSxM6"
		key="mEbZSxM6"
		SALT = "LykuqA5m06"
		PAYU_BASE_URL = "https://sandboxsecure.payu.in/_payment"

		txnid = get_transaction_id()
		posted["txnid"] = txnid
		posted["key"] = key

		hashSequence = "key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5|udf6|udf7|udf8|udf9|udf10"
		hash_string = ''
		hashVarsSeq = hashSequence.split('|')
		for i in hashVarsSeq:
			try:
				hash_string += str(posted[i])
			except Exception:
				hash_string += ''
			hash_string += '|'
		hash_string += SALT
		hashh = hashlib.sha512(hash_string.encode('utf-8')).hexdigest().lower()
		action = PAYU_BASE_URL

		fest = Fest.objects.get(id = fest_id)
		org_id = fest.organizer.id
		payment_obj = Payment(
			first_name = first_name,
			last_name = last_name,
			email = email,
			phone = contact,
			login_type = "F",
			fest_id = fest_id,
			event_id = event_id,
			org_id = org_id,
			amount = amount,
			transaction_id = txnid,
			status = "I"
		)
		payment_obj.save()

		return Response([{"posted":posted, "hashh":hashh, "MERCHANT_KEY":MERCHANT_KEY, "txnid":txnid, "hash_string":hash_string,
			"action":PAYU_BASE_URL}])


@csrf_protect
@csrf_exempt
def success(request):
	c = {}
	c.update(csrf(request))
	status=request.POST.get("status")
	firstname=request.POST.get("firstname")
	amount=request.POST.get("amount")
	txnid=request.POST.get("txnid")
	posted_hash=request.POST.get("hash")
	key=request.POST.get("key")
	productinfo=request.POST.get("productinfo")
	email=request.POST.get("email")
	salt = "LykuqA5m06"
	try:
		additionalCharges=request.POST["additionalCharges"]
		retHashSeq=additionalCharges+'|'+salt+'|'+status+'|||||||||||'+email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+key
	except Exception:
		retHashSeq = salt+'|'+status+'|||||||||||'+email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+key
	hashh=hashlib.sha512(retHashSeq.encode('utf-8')).hexdigest().lower()
	if(hashh !=posted_hash):
		print("Invalid Transaction. Please try again")
	else:
		print("Thank You. Your booking status is ", status)
		print("Your Transaction ID for this transaction is ",txnid)
		print("We have received a payment of Rs. ", amount)

	Payment.objects.filter(transaction_id = txnid).update(status = 'S')

	return render(request, 'payment/sucess.html', {"txnid":txnid, "status":status, "amount":amount})


@csrf_protect
@csrf_exempt
def failure(request):
	c = {}
	c.update(csrf(request))
	status=request.POST.get("status")
	firstname=request.POST.get("firstname")
	amount=request.POST.get("amount")
	txnid=request.POST.get("txnid")
	posted_hash=request.POST.get("hash")
	key=request.POST.get("key")
	productinfo=request.POST.get("productinfo")
	email=request.POST.get("email")
	salt = "LykuqA5m06"
	try:
		additionalCharges=request.POST["additionalCharges"]
		retHashSeq=additionalCharges+'|'+salt+'|'+status+'|||||||||||'+email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+key
	except Exception:
		retHashSeq = salt+'|'+status+'|||||||||||'+email+'|'+firstname+'|'+productinfo+'|'+amount+'|'+txnid+'|'+key
	hashh=hashlib.sha512(retHashSeq.encode('utf-8')).hexdigest().lower()
	if(hashh !=posted_hash):
		print("Invalid Transaction. Please try again")
		Payment.objects.filter(transaction_id = txnid).update(status = 'F')
	else:
		print("Thank You. Your booking status is ", status)
		print("Your Transaction ID for this transaction is ",txnid)
		print("We have received a payment of Rs. ", amount)
		return render(request, "payment/Failure.html", c)


def sendSMS(apikey, numbers, message):
    data =  urllib.parse.urlencode({'apikey': apikey, 
    	'numbers': numbers, 'message' : message})
    data = data.encode('utf-8')
    request = urllib.request.Request("https://api.textlocal.in/send/?")
    f = urllib.request.urlopen(request, data)
    fr = f.read()
    return(fr)


@api_view(["GET"])
def thankyou(request):

	txnid = request.GET.get("txnid")
	payment_rec = Payment.objects.filter(transaction_id = txnid)

	payment_data = {}
	for rec in payment_rec:
		payment_id = rec.id
		fest = Fest.objects.get(id = rec.fest_id)
		fest_name = fest.name
		event = Event.objects.get(id = rec.event_id)
		event_name = event.event_name

		payment_data = {
			"first_name": rec.first_name,
			"last_name": rec.last_name,
			"email": rec.email,
			"phone": rec.phone,
			"fest_name": fest.name,
			"event_name": event.event_name,
			"ticket_price": float(rec.amount)
		}

	organization = Organization.objects.get(id = fest.organizer.id)
	organization_name = organization.name

	ticket_id = "p"+str(payment_id)+"f"+str(fest.id)+"c"+str(organization.id)+"e"+str(event.id)
	Payment.objects.filter(transaction_id = txnid).update(ticket_id = ticket_id)
	payment_data["ticket_id"] = ticket_id

	""" Mail sending with template """
	subject = "{} {} please check your booking details".format(payment_data.get("first_name"), payment_data.get("last_name"))
	from_email = settings.EMAIL_HOST_USER
	to = [payment_data.get("email")]
	html_content = "Here’s your unique identification number is {} for {}, {} for the event {}. Please ensure to carry your ID card with you.".format(ticket_id,fest_name,organization_name,event_name)

	msg = EmailMessage(subject, html_content, from_email, to)
	msg.content_subtype = "html"
	msg.send()

	""" SMS sending using textlocal """
	apikey = "aQszfrEuG9A-fDdmx6sXzFLZ35MrbNo8jyVGpdunLN"
	number = payment_data.get("phone")
	if len(ticket_id) > 10:
		ticket_id = ticket_id[:15]
	if len(fest_name) > 10:
		fest_name = fest_name[:10]
	if len(organization_name) > 10:
		organization_name = organization_name[:10]
	if len(event_name) > 10:
		event_name = event_name[:10]
	message = "Your ticket number is "+str(ticket_id)+" for "+str(fest_name)+" "+str(organization_name)+" for the event "+str(event_name)+". Please carry your ID."
	resp =  sendSMS(apikey, number, message)
	return Response(payment_data, status=status.HTTP_200_OK)
