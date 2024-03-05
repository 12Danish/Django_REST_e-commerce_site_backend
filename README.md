# Construction site backend

**This project is under development**

The project is built on the **Django-REST framework**, with sqlite database configuration

## Project description:
This is a backend for an e-commerce site. It has functionality for both **buyers** and **sellers**.

### Features:

  **Seller functionality**:
- Sellers can register/login to create/update/delete their products.
- They can view the comments posted by different customers on thwir products
- Sellers receive an email with details for the new order.

   **Buyer functionality**:
- Buyers can view products uploaded by different sellers.
- They can search for specific products or a category of products.
- They can complete their order while continuing as guest or creating an account
- If they have an account then their information will be saved and their order history will be maintained
- Buyers on completing their transaction receive a system generated pdf receipt and an email.

## Project structure

The main project folder is : 
**backend -> backend**
Main files within beckend":
- settings.py : Having main configurations for the project
- urls.py : Having urls for the project. They lead towards the API urls which then further point to specific urls

### Apps:
The project consists of the following apps:
 - **backend -> API**: This has models, serializers, mixins, permission/authentiction classes used across the entire project. Its url configurations contain urls which lead to specific applications
 - **backend -> Seller** : This app has views specific to the seller with url configurations for different views
 - **backend -> Buyer** : This has models, serializers,views speciifc to the buyer and url configurations which lead to different views.
 - **backend ->** UserManagement : This app handles user login/logout and other authentication/authorization related activities

## Setup Instructions.

### Dependencies:
You must have python, django/django-REST, django-corsheaders installed on you pc.

- Pull the code onto your machine
- Activate virtual env
- Make migrations to the database by running:
  ```
  python3 manage.py makemigrations
  python3 manage.py migrate
  ```
- Run development server:
  ```
  python3 manage.py runserver
  ```

  
