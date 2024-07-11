from datetime import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core import models as core_models
from core import serializers as core_serializers


class SearchEventAPIView(APIView):
    def get(self, request):
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")

        if not start_date or not end_date:
            return Response(
                {"error": "Please provide start_date and end_date"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            return Response(
                {"error": "Invalid date format. Use YYYY-MM-DD"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        events = core_models.Event.objects.filter(
            start_date__gte=start_date, end_date__lte=end_date
        )
        serializer = core_serializers.EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
