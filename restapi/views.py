from django.contrib.auth.models import Group
from restapi.models import ReuqestToCredit, CustomerProfile
from restapi.serializers import CreditRequestsSerializer, CustomerProfileSerializer
from rest_framework import generics
from rest_framework import permissions

class HasGroupPermission(permissions.BasePermission):
    """
    Ensure user is in required groups.
    """

    def is_in_group(self, user, group_name):
        """
        Takes a user and a group name, and returns `True` if the user is in that group.
        """
        return Group.objects.get(name=group_name).user_set.filter(id=user.id).exists()

    def has_permission(self, request, view):
        # Get a mapping of methods -> required group.
        required_groups_mapping = getattr(view, 'required_groups', {})

        # Determine the required groups for this particular request method.
        required_groups = required_groups_mapping.get(request.method, [])

        # Return True if the user has all the required groups.
        return any([self.is_in_group(request.user, group_name) for group_name in required_groups])


class CustomerProfileList(generics.ListCreateAPIView):
    permission_classes = [HasGroupPermission]
    required_groups = {
        'GET': ['Admins', 'Partners', 'CreditOrgs'],
        'POST': ['Admins'],
    }
    serializer_class = CustomerProfileSerializer
    ordering= ('score', )

    def get_queryset(self):
        queryset = CustomerProfile.objects.all()
        surname = self.request.query_params.get('surname', None)
        if surname is not None:
            queryset = queryset.filter(surname=surname)
        first_name = self.request.query_params.get('first_name', None)
        if first_name is not None:
            queryset = queryset.filter(first_name=first_name)
        middle_name = self.request.query_params.get('middle_name', None)
        if middle_name is not None:
            queryset = queryset.filter(first_name=middle_name)
        ordering = self.request.query_params.get('ordering', None)
        if ordering is not None:
            for field in ordering.split(','):
                queryset = queryset.order_by(field)

        return queryset


class CustomerProfileDetail(generics.RetrieveAPIView):
    permission_classes = [HasGroupPermission]
    required_groups = {
        'GET': ['Admins', 'Partners', 'CreditOrgs']
    }
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer


class SendReuqestToCredit(generics.CreateAPIView):
    permission_classes = [HasGroupPermission]
    required_groups = {
        'POST': ['Admins'],
        'GET': ['Admins']
    }
    queryset = ReuqestToCredit.objects.all()
    serializer_class = CreditRequestsSerializer


class CreditRequestsList(generics.ListAPIView):
    permission_classes = [HasGroupPermission]
    required_groups = {
        'GET': ['Admins', 'CreditOrgs']
    }

    serializer_class = CreditRequestsSerializer
    def get_queryset(self):

        queryset = ReuqestToCredit.objects.all()
        surname = self.request.query_params.get('surname', None)
        if surname is not None:
            queryset = queryset.filter(customer_profile__surname=surname)

        ordering = self.request.query_params.get('ordering', None)
        if ordering is not None:
            for field in ordering.split(','):
                queryset = queryset.order_by(field)
        return queryset


class CreditRequestsDetail(generics.RetrieveAPIView):
    permission_classes = [HasGroupPermission]
    required_groups = {
        'GET': ['Admins', 'CreditOrgs']
    }

    def get_queryset(self):
        return ReuqestToCredit.objects.all()
    serializer_class = CreditRequestsSerializer

    def get(self, request, *args, **kwargs):
        if Group.objects.get(name='CreditOrgs').user_set.filter(id=self.request.user.id).exists():
            rtc = ReuqestToCredit.objects.get(pk=kwargs['pk'])
            rtc.status = 'S'
            rtc.save()
        return self.retrieve(request, *args, **kwargs)
