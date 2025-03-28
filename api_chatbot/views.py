from rest_framework.views import APIView
from rest_framework.response import Response
from api_chatbot.models import MessageModel
from api_chatbot.utils.openai_chat import get_chatbot_response
from api_chatbot.utils.router import categorize_question
from api_chatbot.utils.context_builder import (
    get_index_summary, get_burned_area_summary, get_deforestation_summary
)
from .serializers import ChatbotMessageSerializer, MessageSerializer

class ChatbotAPIView(APIView):
    def post(self, request):
        serializer = ChatbotMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.validated_data["message"]
        user = request.user if request.user.is_authenticated else None

        # Step 1: Categorize
        parsed = categorize_question(message)
        category = parsed.get("category")
        print("Category is: ", category)
        
        # Step 2: Prepare context
        system_prompt = "You are a helpful assistant answering forest monitoring questions using real data."
        context = ""

        if category == 1:
            context = get_index_summary(parsed)
        elif category == 2:
            context = get_burned_area_summary(parsed)
        elif category == 3:
            context = get_deforestation_summary(parsed)

        if context:
            system_prompt += f"\n\nData context:\n{context}"

        print("Context is: ", context)

        # Step 3: Prepare chat history
        history = MessageModel.objects.filter(user=user).order_by("-created_at")[:5]
        messages = [{"role": "system", "content": system_prompt}]
        for msg in reversed(history):
            messages.append({"role": msg.role, "content": msg.text})
        messages.append({"role": "user", "content": message})

        # Step 4: GPT call
        answer = get_chatbot_response(messages)

        # Step 5: Store messages
        MessageModel.objects.create(user=user, role="user", text=message)
        MessageModel.objects.create(user=user, role="assistant", text=answer)

        return Response({"response": answer})

class ChatHistoryAPIView(APIView):
    def get(self, request):
        user = request.user if request.user.is_authenticated else None
        if user:
            messages = MessageModel.objects.filter(user=user).order_by('created_at')
        else:
            messages = MessageModel.objects.filter(user__isnull=True).order_by('created_at')
        serializer = MessageSerializer(messages, many=True)
        return Response({"history": serializer.data})