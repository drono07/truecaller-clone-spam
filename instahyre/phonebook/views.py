from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import AllowAny
from .models import MyUser, PhoneEntry, SpamReport, ContactList
from .serializers import UserSerializer, PhoneEntrySerializer, SpamReportSerializer, ContactListSerializer


from rest_framework.authtoken.models import Token

class UserLoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        mobile = request.data.get("mobile")
        password = request.data.get("password")
        user = authenticate(mobile=mobile, password=password)
        if user:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({"message": "Login successful.", "token": token.key}, status=status.HTTP_200_OK)
        return Response({"message": "Invalid credentials. Please try again."}, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful."}, status=status.HTTP_200_OK)

class UserViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    authentication_classes = []


class SpamReportViewSet(viewsets.ModelViewSet):
    queryset = SpamReport.objects.all()
    serializer_class = SpamReportSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def create(self, request, *args, **kwargs):
        user = request.user
        phone_entry_number = request.data.get('phone_entry')
        try:
            phone_entry = PhoneEntry.objects.get(id=phone_entry_number)
        except PhoneEntry.DoesNotExist:
            return Response({"message": "Phone entry not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if SpamReport.objects.filter(user=user, phone_entry=phone_entry).exists():
            phone_entry.spam_score += 1
            phone_entry.save()
            return Response({"message": "Number already marked as spam."}, status=status.HTTP_201_CREATED)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Increase the spam score of the phone entry
        phone_entry.spam_score += 1
        phone_entry.save()
        
        return Response({"message": "Number marked as spam."}, status=status.HTTP_201_CREATED)

class ContactListViewSet(viewsets.ModelViewSet):
    queryset = ContactList.objects.all()
    serializer_class = ContactListSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def get_queryset(self):
        return ContactList.objects.filter(user=self.request.user)

class SearchByNameView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get(self, request, name):
        starts_with_results = PhoneEntry.objects.filter(name__startswith=name)
        contains_results = PhoneEntry.objects.filter(name__icontains=name).exclude(name__startswith=name)
        results = list(starts_with_results) + list(contains_results)
        serializer = PhoneEntrySerializer(results, many=True)
        return Response({'results': serializer.data}, status=status.HTTP_200_OK)

class SearchByNumberView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get(self, request, number):
        if not number.isdigit() or len(number) < 10:
            return Response({'error': 'Invalid phone number format'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            registered_user = MyUser.objects.get(mobile=number)
            is_contact = ContactList.objects.filter(user=request.user, contact_number=registered_user.mobile).exists()
            most_spammed = PhoneEntry.objects.filter(number=number).order_by('-spam_score').first()
            result_info = {
                'name': registered_user.full_name,
                'mobile': registered_user.mobile,
                'email': registered_user.email if is_contact else None,
                'spam_score': most_spammed.spam_score if most_spammed else 0
            }
            return Response({'result': result_info}, status=status.HTTP_200_OK)
        except MyUser.DoesNotExist:
            results = PhoneEntry.objects.filter(number=number)
            serializer = PhoneEntrySerializer(results, many=True)
            return Response({'results': serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'Unexpected error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
