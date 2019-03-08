# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import stripe
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from ivr_app.models import CardError, Card, ResponseTransaction
from ivr_app.serializers import CardSerializer

# this is the global strip api key. That is defined in the settings
stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentView(APIView):
    """
    This is the main view. Only allows to make posts
    """
    # this is to ensure that before doing anything, the user is authenticated
    permission_classes = (IsAuthenticated,)
    # This is the serializer of card. In this way, we can specify the
    # fields that we want to go in the post
    serializer_class = CardSerializer

    def post(self, request):
        error = {}
        # its interesting to know the actual user.
        actual_user = str(request.user)
        # we need to try to create a token and create a charge.
        # If there is a problem, it will enter to the corresponding except
        try:
            # variable to verify that the request is correct.
            serializer = CardSerializer(data=request.data)
            # when the fields are not complete
            if serializer.is_valid():
                create_request_info(request.data)
            # if the request is invalid a log is created and the error response is given
            else:
                # this tuple is to save the missing fields in the request.
                empty_fields = ()
                for key in request.data:
                    if request.data[key] is "":
                        empty_fields = (*empty_fields, key)
                error = {'message': 'All the fields should be complete. Missing %s' % str(empty_fields),
                         'code': 'Bad request', 'status': status.HTTP_400_BAD_REQUEST, 'username': actual_user}
                save_error = CardError(**error)
                save_error.save()
                return Response({'Error': error['message']}, status=error['status'])

            # Here, we can create the token
            token = stripe.Token.create(card={
                "number": request.POST.get('cc_num'),
                "exp_month": request.POST.get('exp_month'),
                "exp_year": request.POST.get('exp_year'),
                "cvc": request.POST.get('cvc')
            })

            charge = stripe.Charge.create(
                amount=request.POST.get('amount'),
                currency="usd",
                source=str(token.id),  # obtained with the previous variable
                description=request.POST.get('description')
            )

            # These two functions are to save the successful logs in the corresponding table
            create_response_info(charge)

            return Response({'Success': 'The transactions were successful, '
                                        'the corresponding logs were saved in the database '
                                        'with the most interesting information to know.'})

        except (stripe.error.CardError, stripe.error.RateLimitError,
                stripe.error.InvalidRequestError, stripe.error.AuthenticationError,
                stripe.error.APIConnectionError, stripe.error.StripeError) as e:
            # This error occurs when the data entered is incorrect or
            # or when there is a stripe exception
            error = create_dict_error(e, actual_user)
        except Exception as e:
            # This log will not be saved in the database because we
            # do not know the structure, we only know that it is an unexpected error unrelated to stripe
            return Response({'Error': 'Error completely unrelated to Stripe'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'Error': error}, status=error['status'])


def create_dict_error(e, actual_user):
    """
    This create an dictionary and save in the DB this data
    :param e: This is the error code
    :param actual_user: Actual user in the app
    :return: Return the error dictionary
    """
    body = e.json_body
    err = body.get('error', {})
    error = {'message': err.get('message'), 'code': e.code, 'status': e.http_status, 'username': actual_user}
    save_error = CardError(**error)
    save_error.save()
    print('Error log inserted with exit')
    return error


def create_response_info(response):
    """
    This function is to create a response dictionary and save into the DB.
    :param response: This is the response that we get in a successful create charge.
    :return: Save the data in the DB
    """
    response_dict = {'id': response.id, 'live_mode': response.livemode, 'status': response.status,
                     'currency': response.currency, 'paid': response.paid,
                     'balance_transaction': response.balance_transaction,
                     'object_type': response.object, 'created': response.created, 'id_card': response.source.id,
                     'seller_message': response.outcome.seller_message}
    save_response = ResponseTransaction(**response_dict)
    save_response.save()


def create_request_info(data):
    """
    This function is to create a request dictionary and save into the DB.
    :param data: this is the data that we need to save in the DB
    :return: Save the data in the DB
    """
    cc_num = data.get('cc_num')
    cc_num_masked = cc_num[-4:].rjust(len(cc_num), "X")
    card_dict = {'cc_num': cc_num_masked, 'cvc': "XXX", 'exp_month': data['exp_month'],
                 'exp_year': data.get('exp_year'), 'amount': data.get('amount'), 'description': data.get('description')}
    save_request = Card(**card_dict)
    save_request.save()
