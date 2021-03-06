from django.contrib.auth.models import User, Group
from rest_framework.response import Response
from rest_framework.views import APIView

from telerehabilitation_API.authentication.models import Therapist
from telerehabilitation_API.authentication.serializers import TherapistSerializer


class TherapistViewSet(APIView):
    def get(self, request, format=None):
        return Response(TherapistSerializer(Therapist.objects.all(), many=True).data)

    def post(self, request):
        if 'username' not in request.data.keys() and \
           'email' not in request.data.keys() and \
           'first_name' not in request.data.keys() and \
           'last_name' not in request.data.keys():
            return Response({}, status=400)
        else:
            new_therapist = User.objects.create_user(request.data['username'], request.data['email'], '123456789')
            new_therapist.first_name = request.data['first_name']
            new_therapist.last_name = request.data['last_name']
            new_therapist.save()
            therapist_group = Group.objects.get(name="Therapist")
            therapist_group.user_set.add(new_therapist)
            Therapist.objects.create(user_id=new_therapist.id)
            return Response({}, status=201)
