# Marcos Lopez - Customize django login to check emails first, then username (optional)
from django.contrib.auth.models import User

class BasicBackend:
	def get_user(self, user_id):
		try:
			return User.objects.get(pk=user_id)
		except User.DoesNotExist:
			return None

class EmailBackend(BasicBackend):
	def authenticate(self, username=None, password=None):
		#If username is an email address, then try to pull it up

		if '@' in str(username):
			try:
				user = User.objects.filter(email=username)
				for i in user:
					if i.check_password(password):
						return i


			except User.DoesNotExist:
				return None


		else:
			#We have a non-email address username we should try username
			return None
			# uncomment to try username login fallback
			#try:
			#	user = User.objects.get(username=username)
			#	if user.check_password
			#except User.DoesNotExist:
			#	return None


#		if user.check_password(password):
#			return user
#		else:
			
