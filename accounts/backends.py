# app.backends.py
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

UserModel = get_user_model()




# Custom authentication for only username fields
class CaseInsensitiveUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            case_insensitive_username_field = '{}__iexact'.format(UserModel.USERNAME_FIELD)
            user = UserModel._default_manager.get(**{case_insensitive_username_field: username})
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user




# Custom authentication for username and email fields
class CaseInsensitiveEmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)   
        if '@' in username and '.' in username:
            case_insensitive_username_field = '{}__iexact'.format('email')
        else:
            case_insensitive_username_field = '{}__iexact'.format('username')
        try:
            # Force all usernames & email to all lower case
            user = UserModel._default_manager.get(**{case_insensitive_username_field: username}) 
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user



# def my_password_reset(request, **kwargs):
#     # Override django.contrib.auth.views.password_reset not needed because django does
#     # SELECT FROM "auth_user" WHERE UPPER("auth_user"."email"::text) = UPPER(E'xxx@emaple.com')
#     # But note you may want to manually create an UPPER index in the database for speed.
#     return password_reset(request, **kwargs)



# This backend will work with authentication forms that explicitly set an email field as well as those setting a username field.
class CustomUserModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD, kwargs.get(UserModel.EMAIL_FIELD))
        if username is None or password is None:
            return
        try:
            user = UserModel._default_manager.get(
                Q(username__exact=username) | (Q(email__iexact=username) & Q(email_verified=True))
            )
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user



# We then create a backend similar to the one above that simply checks the related models verified field.
class ExtendedUserModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD, kwargs.get(UserModel.EMAIL_FIELD))
        if username is None or password is None:
            return
        try:
            user = UserModel._default_manager.get(
                Q(username__exact=username) | (Q(email__iexact=username) & Q(verification__verified=True))
            )
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user


# if usernames are case insensitive change Q(username__exact=username) to Q(username__iexact=username).
