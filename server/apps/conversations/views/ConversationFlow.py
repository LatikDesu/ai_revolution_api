from rest_framework import views, status
from rest_framework.response import Response
from users.authentication import CustomJWTAuthentication
from rest_framework.permissions import IsAuthenticated
from conversations.serializers import ConversationFlowSerializer
from conversations.models import ConversationFlow, Conversation


class ConversationFlowView(views.APIView):
    serializer_class = ConversationFlowSerializer
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        qs = ConversationFlow.objects.all()
        serializer = self.serializer_class(qs, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        try:
            conversation_id = request.data.get('conversation')
            question = request.data.get('_input')

            conversation = Conversation.objects.get(id=conversation_id)
            conversation.title = question
            conversation.save()

            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Conversation.DoesNotExist:
            return Response({'detail': 'Беседа не найдена.'}, status=status.HTTP_404_NOT_FOUND)
