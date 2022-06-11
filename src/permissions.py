from django.contrib.auth.models import Group, User
from rest_framework.permissions import BasePermission
from .models import StatusContract
from django.db.models import Q


class TeamBasePermission(BasePermission):
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
        return False


class ClientsPermission(TeamBasePermission):
    message = 'Permission denied. Your not allowed to perform this action'

    """def has_permission(self, request, view):
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
        return False"""

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
    """def has_permission(self, request, view):
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
        return False"""

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
        return False


"""class SalesContactPermission(BasePermission):


    message = 'Permission denied. Your not allowed to perform this action'

    def has_permission(self, request, view):
        try:
            user_group = Group.objects.get(user=request.user)
            if str(user_group.name) == 'sales' and (request.method == 'GET' or
                                                    request.method == 'POST'):
                return True
        except KeyError:
            print("This group doesn't exists.")
        except Exception as e:
            print(e)
        return False"""

"""    def has_object_permission(self, request, view, obj):
        HTTP_METHODS = ['GET', 'UPDATE', 'PATCH']
        try:
            user_group = Group.objects.get(user=request.user)
            contract_status = StatusContract.objects.get(contract=obj)
            if str(user_group.name) == 'sales' and str(contract_status.sales_contact) == request.user and \
                    (request.method in HTTP_METHODS):
                return True
            if str(user_group.name) == 'management' and (request.method in HTTP_METHODS):
                return True
        except KeyError:
            print("This group doesn't exists.")
        except Exception as e:
            print(e)
        return False"""

"""
class SupportContactPermission(BasePermission):
   User permission for the event team
        - only a support group could perform some action
        - a support can only retrieve client, retrieve and update an event
    Returns:
        boolean: True grants permission otherwise it's forbidden

    message = 'Permission denied. Your not allowed to perform this action'

    def has_permission(self, request, view):
        try:
            user_group = Group.objects.get(user=request.user)
            if (str(user_group.name) == 'support' or str(user_group.name) == 'management') and \
                    (request.method == 'GET' or request.method == 'UPDATE' or request.method == 'PATCH'):
                return True
        except KeyError:
            print("This group doesn't exists.")
        except Exception as e:
            print(e)
        return False

    def has_object_permission(self, request, view, obj):
        HTTP_METHODS = ['GET', 'UPDATE', 'PATCH']
        try:
            user_group = Group.objects.get(user=request.user)
            contract_status = StatusContract.objects.get(contract=obj)
            if str(user_group.name) == 'support' and str(contract_status.support_contact) == request.user and \
                    request.method in HTTP_METHODS:
                return True
            if str(user_group.name) == 'management' and request.method in HTTP_METHODS:
                return True
        except KeyError:
            print("This group doesn't exists.")
        except Exception as e:
            print(e)
        return False
"""
