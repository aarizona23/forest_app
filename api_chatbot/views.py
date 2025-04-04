from rest_framework.views import APIView
from rest_framework.response import Response
from api_chatbot.models import MessageModel
from api_chatbot.utils.openai_chat import get_chatbot_response
from api_chatbot.utils.router import categorize_question
from api_chatbot.utils.context_builder import (
    get_index_summary, get_burned_area_summary, get_deforestation_summary
)
from .serializers import ChatbotMessageSerializer, MessageSerializer

COMMON_INFO = """ The main information about the database for context:
The database stores mean indices of different vegetative indices such as 
'NDVI', 'EVI', 'NDWI', 'NBR', 'SAVI', 'GNDVI', 'SIPI', 'MGRVI', 'TGI', 'VARI', 'GRVI', 'SR', 'CI', 'MSR', 'OSAVI', 'NDMI', 'MSAVI', 'NDRI', 'RECI' for a given area and time (2020–2025 only).
It has data for 2020, 2021, 2023 and 2024 with biweekly intervals.
Indices are derived using sattelite images. Specifically, Sentinel-2 and Landsat sattelites were used to capture those images.
Also, there are availbale burned masks only for Semey Ormany.
In addition, the database has forest masks which are used to retrieve deforestation information.
The database consists of only 4 areas of Kazakhstan, they are:
- 1: Semey Ormany
- 2: Semey Ormany 2
- 3: North KZ
- 4: East KZ
"""

class ChatbotAPIView(APIView):
    def post(self, request):
        serializer = ChatbotMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.validated_data["message"]
        user = request.user if request.user.is_authenticated else None

        # LLM categorizes the question in order to identify which function should be used for context retrieval (RAG)
        parsed = categorize_question(message)
        category = parsed.get("category")
        
        system_prompt = "You are a helpful assistant answering forest monitoring questions using real data.  Available forests and their IDs for identification:" \
        "SemeyOrmany: Semey Ormany, SemeyOrmany2: Semey Ormany 2, NorthKZ: North KZ, EastKZ1: East KZ. Also might be provided additional context abou forests info from 2020 till 2025 (not inclusive) years."
        context = ""

        if category == 1:
            context = get_index_summary(parsed)
            system_prompt += "In the context provided a number of 12 or less index averages throughout the period."
        elif category == 2:
            context = get_burned_area_summary(parsed)
        elif category == 3:
            context = get_deforestation_summary(parsed)
        elif category == 4:
            context = COMMON_INFO

        if context:
            system_prompt += f"\n\nData context:\n{context}"

        # Extract Chat history, 5 last messages for more context of the conversation
        history = MessageModel.objects.filter(user=user).order_by("-created_at")[:5]
        messages = [{"role": "system", "content": system_prompt}]
        for msg in reversed(history):
            messages.append({"role": msg.role, "content": msg.text})
        messages.append({"role": "user", "content": message})

        # Call LLM API to get response
        answer = get_chatbot_response(messages)

        # Store new messages into database to keep track of the converstaion
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