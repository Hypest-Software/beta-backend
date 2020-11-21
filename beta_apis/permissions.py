from rest_framework.permissions import BasePermission
from django.contrib.auth.models import AnonymousUser
from .jwt_utils import decode_jwt
from .models import User


def check_jwt_token(token):
    data = decode_jwt(token)
    user_id = None
    if data is not None:
        user_id = data.get('sub', None)
    if user_id is None:
        return False, "user id is none"
    # check if this user_id is existing
    user = User.objects.filter(id=user_id).first()
    if user is None:
        return False, "user is not found or active"

    return True, user_id


class UserIdAuthenticated(BasePermission):
    """
    Allow any access with proper 'Authorization' in header.
    That is it must have valid user_id value.
    """

    def has_permission(self, request, view):
        autho = request.META.get('AUTHORIZATION', '')
        has_perm, user_id = check_jwt_token(
            request.META.get('HTTP_AUTHORIZATION', autho))

        print('has_perm:', has_perm, user_id)
        if has_perm is True:
            view.user_id = user_id
        return has_perm


class IsLoggedIn(BasePermission):
    """
    Allows access only to logged in users.
    """

    def has_permission(self, request, view):
        return bool(request.user and type(request.user) is User)


class IsLoggedInOrNone(BasePermission):
    """
    Allows access for everyone.
    """

    def has_permission(self, request, view):
        return bool(request.user is None or (request.user and type(request.user) is User))
