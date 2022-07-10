# karakoo-project

 ## Endpoints:
\
1- api/user/: Default actions on user creation, listing, retrieving, and updating endpoints.\
2- api/customer/: Superusers can create, list and retrieve all the users and update all the users, whereas regular users can only list, retreive or update the users they created.
\
3- api/log/: Any user can create logs provided that they enter the user id, customer id and the log message. Also any user can retrieve any logs from other users regardless of user status.\
4- api/customer_contact: Gives the contact information of the customers regardless of whether they registered through the link or not.

## The Flow:\
The user is created and then obtains the contact information of the customer. This is stored in the CustomerContact table. Then upon creation of the potential customer is CustomerContact table, a post_save signal including an email with the registration link is sent to the potential customer. If the customer registers through this link then the customer is saved in the Customer table and the associated customer in the CustomerContact table is updated to match this customer. If the customer does not register they will have no associated customer in the Customer table. So, there are many more potential customers than those actually registered.\
Also, when the Customer info is updated through a patch request, the CustomerContact table's information is updated as well within the permission restrictions imposed in the first version of this assignment.\
## Potential Improvements:\
- The information for the customer in the CustomerContact table and the Customer table after they provide their information should match. I did not have tine to write validations for these but I believe this might be in an important part of this project.\
- Some cleanup in the django admin is required.\
## Tests:\
As usual, run the tests directly by python manage.py test customer in the project root.\

