from rest_framework.response import Response
from rest_framework.views import APIView


# index page
# /
class Index(APIView):

    def get(self, request):
        return Response({"The Dojos": "Welcome to Questioner."})
