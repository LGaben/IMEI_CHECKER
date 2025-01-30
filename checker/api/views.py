import requests
import os
import json

from django.conf import settings
from dotenv import load_dotenv
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

load_dotenv()
SERVICE_ID = os.getenv('SERVICE_ID')


class CheckIMEIView(APIView):
    def post(self, request, *args, **kwargs):
        imei = request.data.get('imei')
        token = request.data.get('token')

        if not self.is_valid_imei(imei):
            return Response(
                {'error': 'Invalid IMEI'},
                status=status.HTTP_400_BAD_REQUEST
            )
        response = self.check_imei_with_service(imei, token)
        return Response(
            response,
            status=status.HTTP_200_OK if 'error' not in response
            else status.HTTP_400_BAD_REQUEST
        )

    def is_valid_imei(self, imei):
        # Проверка длины и формата IMEI
        return 8 <= len(imei) <= 15 and imei.isdigit()

    def check_imei_with_service(self, imei, token):
        url = os.getenv('IMEI_CHECK_API_URL')
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        params = json.dumps({
            'deviceId': imei,
            "serviceId": SERVICE_ID
        })
        try:
            response = requests.request(
                "POST",
                url,
                headers=headers,
                data=params
            )
            if response.status_code == 201:
                return response.json()
            else:
                return {
                    'error': 'Service error',
                    'status_code': response.status_code
                }
        except Exception as e:
            return {'error': str(e)}
