Welcome to the Apiday backend interview exercise!

## Getting Started

First, create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Then, install the dependencies:

```bash
pip install -r requirements.txt
```

Then, apply the migrations:

```bash
pip manage.py migrate
```

Create a user for your application:

```bash
python3 manage.py createsuperuser
```

Add a fake questionnaire:

```bash
python3 manage.py create_questionnaire
```

And finally, run the server:

```bash
python3 manage.py runserver
```

Open [http://localhost:8000/swagger/](http://localhost:8000/swagger/) with your browser to browse the API documentation.

:warning: For the endpoints to work, you will need to be authenticated.
You can specify the user and password in the "basic auth" section in the modal after clicking on the `Authorize` button.

## Learn More

To learn more about Django and Django REST framework, take a look at the following resources:

- [Django Documentation](https://docs.djangoproject.com/en/5.1/)
- [Django REST framework Documentation](https://www.django-rest-framework.org/)

## Goal

The goal of the exercise is to add the "share question" feature to the project.
Apiday customers answer reporting campaigns (called questionnaires internally)
to provide information and follow the regulations.
Sometimes they don't have the information and instead of inviting a colleague
on the platform and create a new account, they should be able to send a link
to colleagues that can then answer.
This link should be authenticated with a token.

To do this:
- an endpoint to create a secure random token should be created
- the two endpoints related to the questions (listing the questions and answering the questions) should be available with a "token" authentication (so without being authenticated as a regular user)

### Expectations

We don't recommend spending more than 2 hours on this exercise.

* The endpoints should work as described above
* Please take any opportunities to improve the code (refactoring the structure,
  adding methods for common logic, etc.), we will talk about these during the
  interview
  * When dealing with this point, if you run out of time, it would be helpful to
    you to at least have some notes about what you would do, so we can discuss
    it during the interview

Not required, but helpful:
* The new feature should have tests

### Technical details

Tokens should be stored in the database to avoid long tokens (JWT signature is long) and to be able to invalidate them.
The token should expire after 7 days.

The token will be sent to the backend in a header (no constraint on the name but `Authorization` is recommended).

You can add the `Authorization` header to your requests in Swagger by setting the parameter in the modal after clicking on the `Authorize` button.
