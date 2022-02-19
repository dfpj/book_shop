from django.shortcuts import redirect
import requests
import json
from django.conf import settings
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

class PayZarinpal:
    def __init__(self, request,amount):
        self.request = request
        self.amount = amount
        self.MERCHANT = ''
        self.API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
        self.API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
        self.API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
        self.CALLBACKURL = settings.DEFAULT_DOMAIN +'order/verify'
        self.req_header = {"accept": "application/json",
                           "content-type": "application/json'"}
        self.session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

    def ready_to_requeat(self, description, **kwargs):

        req_data = {"merchant_id": self.MERCHANT, "amount": self.amount, "callback_url": self.CALLBACKURL,
                    "description": description, "metadata": kwargs}


        req = self.session.post(url=self.API_REQUEST, data=json.dumps(req_data), headers=self.req_header)

        if len(req.json()['errors']) == 0:
            return True, req.json()['data']['authority']
        else:
            return False, req.json()['errors']['message']

    def send_request(self, authority):
        return redirect(self.API_STARTPAY.format(authority=authority))

    def get_authority_from_request(self):
        return self.request.GET['Authority']

    def verify(self,authority):
        if self.request.GET.get('Status') == 'OK':
            req_data = {
                "merchant_id": self.MERCHANT,
                "amount": self.amount,
                "authority": authority
            }
            req = self.session.post(url=self.API_VERIFY, data=json.dumps(req_data), headers=self.req_header)
            return self._handel_verify(req)
        else:
            return False, 'NOK Transaction failed or canceled by user'

    def _handel_verify(self, req):
        """
            :return:  tuple
            index 0 => boolean is_sucsess
            index 1 => RefId if is_sucsess else error message
        """
        if len(req.json()['errors']) == 0:
            t_status = req.json()['data']['code']
            if t_status == 100:
                RefId = req.json()['data']['ref_id']
                return True, RefId
            elif t_status == 101:
                return False, str(req.json()['data']['message'])
            else:
                return False, str(req.json()['data']['message'])
        else:
            return False, str(req.json()['errors']['message'])
