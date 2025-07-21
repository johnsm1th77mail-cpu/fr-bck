from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ContactSerializer
from apps.contact.models import Contact

class ContactView(APIView):
    def get(self, request, *args, **kwargs):
        contacts = Contact.objects.all().order_by('-created_at')
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Message sent successfully!',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message': 'Failed to send message.',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
