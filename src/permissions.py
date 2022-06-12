from django.contrib.auth.models import Group
from rest_framework.permissions import BasePermission
from .models import StatusContract


class TeamBasePermission(BasePermission):
    """ Permission for each category of user
        - user can only create a client/contract/event according to their authorisation or
        access the data related to them
    """
    message = 'Permission denied. Your not allowed to perform this action'

    def has_permission(self, request, view):
        try:
            HTTP_METHODS = ['GET', 'POST']

            user_group = Group.objects.get(user=request.user)

            if str(user_group.name) == 'sales' and request.method in HTTP_METHODS:
                return True
            if str(user_group.name) == 'support' and request.method == HTTP_METHODS[0]:
                return True
            if str(user_group.name) == 'management' and request.method == HTTP_METHODS[0]:
                return True
        except Exception as e:
            print(e)
        return False


class ContractPermission(TeamBasePermission):
    """ Permission for each category of user
        - user can only access or modify the data related to them
    """

    def has_object_permission(self, request, view, obj):
        try:
            HTTP_METHODS = ['GET', 'UPDATE', 'PATCH']
            user_group = Group.objects.get(user=request.user)
            print("perm", str(user_group.name), str(user_group.name) == 'management')
            contract_status = StatusContract.objects.get(contract=obj)
            if str(user_group.name) == 'sales' and contract_status.sales_contact == request.user and \
                    request.method in HTTP_METHODS:
                return True
            if str(user_group.name) == 'support' and contract_status.support_contact == request.user and \
                    request.method in HTTP_METHODS:
                return True
            if str(user_group.name) == 'management' and request.method in HTTP_METHODS:
                return True
        except KeyError:
            print("This group doesn't exists.")
        except Exception as e:
            print(e)
            self.message = " Access denied. You're not allowed to access this contract"
        return False


class ClientsPermission(TeamBasePermission):
    message = 'Permission denied. Your not allowed to perform this action'

    def has_object_permission(self, request, view, obj):

        try:
            HTTP_METHODS = ['GET', 'UPDATE', 'PATCH']
            user_group = Group.objects.get(user=request.user)
            contract_status = StatusContract.objects.get(contract__client=obj)

            if str(user_group.name) == 'sales' and contract_status.sales_contact == request.user and \
                    request.method in HTTP_METHODS:
                return True
            if str(user_group.name) == 'support' and contract_status.support_contact == request.user and \
                    request.method in HTTP_METHODS:
                return True
            if str(user_group.name) == 'management' and request.method in HTTP_METHODS:
                return True
        except Exception as e:
            print(e)
        self.message = " Access denied. You're not allowed to access this client"
        return False


class EventsPermission(TeamBasePermission):
    message = 'Permission denied. Your not allowed to perform this action'

    def has_object_permission(self, request, view, obj):
        try:
            HTTP_METHODS = ['GET', 'UPDATE', 'PATCH']
            user_group = Group.objects.get(user=request.user)
            contract_status = StatusContract.objects.get(contract=obj.contract)
            if str(user_group.name) == 'sales' and contract_status.sales_contact == request.user and \
                    request.method in HTTP_METHODS:
                return True
            if str(user_group.name) == 'support' and contract_status.support_contact == request.user and \
                    request.method in HTTP_METHODS:
                return True
            if str(user_group.name) == 'management' and request.method in HTTP_METHODS:
                return True
        except Exception as e:
            print(e)
        self.message = " Access denied. You're not allowed to access this event"
        return False
