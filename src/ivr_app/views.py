from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import stripe
from django.conf import settings

from ivr_app.models import CardError
from ivr_app.serializers import PaymentSerializer
import datetime

stripe.api_key = settings.STRIPE_PUBLISHABLE_KEY


class PaymentView(APIView):
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = PaymentSerializer

    def post(self, request):
        token = ""
        error = {}
        try:
            token = stripe.Token.create(card={
                "number": request.data['cc_num'],
                "exp_month": request.data['exp_month'],
                "exp_year": request.data['exp_year'],
                "cvc": request.data['cvc']
            },
            )
            return Response({'response': token})

        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            # This error occurs when the data entered is incorrect
            error = create_dict_error(e)
        except stripe.error.RateLimitError as e:
            # This happens when the waiting time extends more than normal
            error = create_dict_error(e)
        except stripe.error.InvalidRequestError as e:
            # When the request is invalid
            error = create_dict_error(e)
        except stripe.error.AuthenticationError as e:
            # Error with the auth
            error = create_dict_error(e)
        except stripe.error.APIConnectionError as e:
            # Connection error with the Strip api
            error = create_dict_error(e)
        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            error = create_dict_error(e)
        except Exception as e:
            # Something else happened, completely unrelated to Stripe
            return Response({'Error': 'Error completely unrelated to Stripe'})

        return Response({'Error': error})


def create_dict_error(e):
    error = {}
    body = e.json_body
    err = body.get('error', {})
    error['message'] = err.get('message')
    error['code'] = e.code
    error['status'] = e.http_status
    error['date'] = datetime.datetime.now()

    save_error = CardError(**error)
    save_error.save()
    print('Error log inserted with exit')

    return error
