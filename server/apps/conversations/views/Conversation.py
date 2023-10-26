from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from conversations.serializers import ConversationSerializer, ConversationFlowSerializer
from conversations.models import Conversation, ConversationFlow


class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def create_conversation(self, request):
        title = request.data.get('title', 'Новая беседа')
        conversation = Conversation.objects.create(
            user=request.user, title=title)
        serializer = self.serializer_class(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def get_user_conversations(self, request):
        conversations = Conversation.objects.filter(user=request.user)
        serializer = self.serializer_class(conversations, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def get_conversation_with_flows(self, request, pk=None):
        try:
            conversation = Conversation.objects.get(pk=pk)
        except Conversation.DoesNotExist:
            return Response({'detail': 'Беседа не найдена.'}, status=status.HTTP_404_NOT_FOUND)

        flows = ConversationFlow.objects.filter(conversation=conversation)
        conversation_serializer = self.serializer_class(conversation)
        flow_serializer = ConversationFlowSerializer(flows, many=True)

        response_data = {
            'conversation': conversation_serializer.data,
            'flows': flow_serializer.data,
        }
        return Response(response_data)

    @action(detail=False, methods=['get'])
    def get_conversation_with_flows(self, request):
        conversation_id = request.GET.get('conversation_id')
        if not conversation_id:
            return Response({'detail': 'Не указан ID беседы.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            conversation = Conversation.objects.get(
                id=conversation_id, user=request.user)
        except Conversation.DoesNotExist:
            return Response({'detail': 'Беседа не найдена или не принадлежит текущему пользователю.'}, status=status.HTTP_404_NOT_FOUND)

        flows = ConversationFlow.objects.filter(conversation=conversation)
        conversation_serializer = self.serializer_class(conversation)
        flow_serializer = ConversationFlowSerializer(flows, many=True)

        response_data = {
            'conversation': conversation_serializer.data,
            'flows': flow_serializer.data,
        }
        return Response(response_data)
