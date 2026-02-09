from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from .models import Quote
from .serializers import QuoteSerializer, PublicQuoteSerializer

from rest_framework.exceptions import ValidationError

class QuoteCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = QuoteSerializer(data=request.data)
        if serializer.is_valid():
            quote = serializer.save()  # Save instance
            return Response(
                QuoteSerializer(quote).data,  # <-- serialize the saved object
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QuoteListView(APIView):
    authentication_classes = [TokenAuthentication] 
    permission_classes = [IsAuthenticated]

    def get(self, request):
        quotes = Quote.objects.all().order_by("-created_at")
        serializer = QuoteSerializer(quotes, many=True)
        return Response(serializer.data)


class PublicQuoteLookupView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        email = request.query_params.get("email")

        if not email:
            raise ValidationError({"email": "Email query parameter is required"})

        quotes = Quote.objects.filter(email=email).order_by("-created_at")

        serializer = PublicQuoteSerializer(quotes, many=True)
        return Response(serializer.data)

