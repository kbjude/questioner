from rest_framework.response import Response
from rest_framework.views import APIView


class Index(APIView):
    @classmethod
    def get(self, request):
        return Response({"The Dojos": "Welcome to Questioner."})
