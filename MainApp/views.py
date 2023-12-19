from rest_framework.views import APIView
from rest_framework.response import Response
from urllib.parse import urljoin
from django.core.files.base import ContentFile
from django.http import FileResponse
from .serializers import UploadFileSerializer
from MainApp import services
from django.core.files.storage import default_storage
import asyncio
import uuid, json, os
from django.conf import settings
from time import time


class AsyncTradingView(APIView):
    def post(self, request, format=None):
        serializer = UploadFileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        timeframe = serializer.validated_data["timeframe"]
        csv_file = serializer.validated_data["file"]
        candles = asyncio.run(services.process_csv(csv_file, timeframe))
        json_data = json.dumps([candle.to_dict() for candle in candles])
        file_path = default_storage.save(
            f'downloads/{f"candles_data_{int(time())}.json"}', ContentFile(json_data)
        )
        return Response(
            {
                "message": "File processed.",
                "download_url":urljoin(request.build_absolute_uri('/'), f"{settings.MEDIA_URL}downloads/candles_data_{int(time())}.json") if settings.DEBUG  else urljoin(request.build_absolute_uri('/'),f"download/candles_data_{int(time())}.json") 
            }
        )


class FileDownloadView(APIView):
    def get(self, request, file_name):
        file_path = os.path.join(settings.MEDIA_ROOT, "downloads", file_name)

        if os.path.exists(file_path):
            return FileResponse(
                open(file_path, "rb"), as_attachment=True, filename=file_name
            )
        else:
            return Response({"error": "File not found"}, status=404)
