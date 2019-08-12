from django.shortcuts import render, redirect
from django.views.generic import View, DetailView
from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import Order
import hmac
import hashlib
import base64
import json


@method_decorator(csrf_exempt, name='dispatch')
class WebhookView(View):
    '''
    @handle_webhook()/@verify_webhook() -> for handling and verifying webhook.
    @post() -> retrieving data from the response and stored in database
    '''
    def verify_webhook(self,data, hmac_header):
        SECRET = 'hush'
        digest = hmac.new(b'self.SECRET', data, hashlib.sha256).digest()
        computed_hmac = base64.b64encode(digest)

        return hmac.compare_digest(computed_hmac, hmac_header.encode('utf-8'))


    def handle_webhook(self, request):
        ''' Validates the HMAC signature from shopify. If not there, deny request.'''
        data = request.body
        verified = self.verify_webhook(data, request.headers.get('X-Shopify-Hmac-SHA256'))

        if not verified:
            return HttpResponse(401)
        return HttpResponse(200)


    def post(self,request, *args, **kwargs):
        ''' receiving data and storing in database'''
        data = request.body.decode('utf8')  # decode() is used to remove b in json''
        p_data = json.loads(data)
        orderno = p_data.get('order_number')
        customer_name  = p_data.get('customer').get('first_name')+' '+ p_data.get('customer').get('last_name')
        customer_email = p_data.get('customer').get('email')
        customer_phone = p_data.get('customer').get('default_address').get('phone')
        total_price    = p_data.get('total_price')
        subtotal_price = p_data.get('subtotal_price')

        order = Order()
        order.orderno = orderno
        order.customer_name = customer_name
        order.customer_email = customer_email
        order.customer_phone = customer_phone
        order.total_price = total_price
        order.subtotal_price = subtotal_price
        order.save()

        status = self.handle_webhook(request)
        return HttpResponse(data,content_type='application/json', status=None)


class OrderDetail(View):
    '''for order related logic (to display orders)'''
    def get(self, request, *args, **kwargs):
        orders = Order.objects.all()
        return render(request, 'myApp/show.html', {'orders':orders})


class ContactUpdate(UpdateView):
    ''' edit phone/email n stored in database'''
    model = Order
    fields = ['customer_email', 'customer_phone']
