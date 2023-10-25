from rest_framework import views, status
from rest_framework.response import Response
from users.authentication import CustomJWTAuthentication
from rest_framework.permissions import IsAuthenticated
from gpt.serializers import ConversationSerializer
from gpt.models import ConversationExplainer


class ConversationView(views.APIView):
    serializer_class = ConversationSerializer
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        qs = ConversationExplainer.objects.all()
        serializer = self.serializer_class(qs, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)