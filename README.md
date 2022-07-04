# karakoo-project

Endpoints:

1- api/user/: Default actions on user creation, listing, retrieving, and updating endpoints.\
2- api/customer/: Superusers can create, list and retrieve all the users and update all the users, whereas regular users can only list, retreive or update the users they created.\ 
3- api/log/: Any user can create logs provided that they enter the user id, customer id and the log message. Also any user can retrieve any logs from other users regardless of user status.\
Tests:\
Run the tests directly by python manage.py test customer in the project root.
