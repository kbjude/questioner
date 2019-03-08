from rest_framework.views import APIView
from rest_framework.response import Response


# index page
# /
class Index(APIView):

    def get(self, request):
        return Response({"The Dojos": "Welcome to Questioner."})
