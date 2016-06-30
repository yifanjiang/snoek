from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from social.backends.open_id import OpenIdAuth

# Raw copy of code from http://blog.shopfiber.com/?p=220
class CaseInsensitiveAuthBackend(ModelBackend):
  """
  By default ModelBackend does case _sensitive_ username authentication, which isn't what is
  generally expected.  This backend supports case insensitive username authentication.
  """
  def authenticate(self, username=None, password=None):
    try:
      user = User.objects.get(username__iexact=username)
      if user.check_password(password):
        return user
      else:
        return None
    except User.DoesNotExist:
      return None

class SUSEOpenId(OpenIdAuth):
    name = 'suse'
    URL = 'https://www.suse.com/openid/user/'

    def get_user_id(self, details, response):
        """
        Return user unique id provided by service. For openSUSE
        the nickname is original.
        """
        return details['nickname']

class openSUSEOpenId(OpenIdAuth):
    name = 'opensuse'
    URL = 'https://www.opensuse.org/openid/user/'

    def get_user_id(self, details, response):
        """
        Return user unique id provided by service. For openSUSE
        the nickname is original.
        """
        return details['nickname']
