# ice_assessment

This project contains backend code for ICE power assessment test implemented with Django and DRF.


## Getting Started

To run the project, first ensure the source code is cloned.

 1. Ensure you are in the root directory with:

    `cd <path to root directory>`

 2. Install the requirements with:

    `pip install -r requirements.txt`
 3. Create a .env file at the root directory and set Debug and SECRET_KEY environment variables

 4. Shell environment variables:

     `export $(xargs < .env)`

5. Run migrations

    `python manage.py makemigrations`
    `python manahe.py migrate`

6. Create superuser:

    `python manage.py createsuperuser`

7. Start the server with:

    `python manage.py runserver`

8. Run tests

    `python manage.py test`

Link to postman API documentation [Link Here](https://documenter.getpostman.com/view/14940225/2s8YsozvLk#d7893a64-c477-4e92-aa0e-7e0a1ed01d6e)

Note. After creating a user using the signup API, head back to Django admin dashboard on browser and login using the superuser credentials created above and then update the signup user to is_staff. This is to grant the user permission to interact with the API endpoints.
