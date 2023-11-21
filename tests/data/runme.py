from django.contrib.auth.models import User

# create a user in the database as a side-effect of the script for detection
# during testing
User.objects.create_user('fakeuser', 'fake@user.com', 'fakeuser')
