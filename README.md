# Django REST Framework Image Upload API

This project is an API developed using Django REST Framework (DRF) which allows users to upload and manage images in PNG or JPG formats. The API is structured around different account tiers offering various functionalities.

## Requirements

- Django
- Django REST Framework
- Docker and docker-compose (optional but recommended for easy setup)

## Features

- **Image Upload**: Users can upload images in PNG or JPG format via HTTP requests.
- **Image Listing**: Users can list all the images they have uploaded.
- **Different Account Tiers**: The API supports different account tiers with various functionalities:
  - **Basic**
    - 200px height thumbnail link
  - **Premium**
    - 200px height thumbnail link
    - 400px height thumbnail link
    - Original image link
  - **Enterprise**
    - 200px and 400px height thumbnail links
    - Original image link
    - Ability to fetch expiring image links (valid between 300 and 30000 seconds)
- **Admin-defined Account Tiers**: Apart from the built-in tiers, admins can create custom tiers with configurable settings through the django-admin interface.
- **Browsable API**: The project utilizes DRF's browsable API, avoiding the need for a custom user UI.

## Setup

### Using Docker (Recommended)

1. Install [Docker](https://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/).
2. Run `docker-compose up` to start the services.
3. The API will be available at `http://localhost:8000`.

### Manual Setup

1. Set up a virtual environment and activate it.
2. Install the required packages using `pip install -r requirements.txt`.
3. Run migrations using `python manage.py migrate`.
4. Create a superuser using `python manage.py createsuperuser`.
5. Start the Django development server using `python manage.py runserver`.
6. The API will be available at `http://localhost:8000`.

## Testing

To run the tests, execute the following command:

```bash
pytest
```

## Usage

### Admin Panel

Administrators can manage users and define various account tiers through the Django admin panel which can be accessed at `http://localhost:8000/admin`.

### API Endpoints

- **Swagger**
  - **Endpoint:** `GET /docs/`
  - **Description:** Swagger.

Here are the key endpoints that the API exposes:

- **Register an account**
  - **Endpoint:** `POST /users/register/`
  - **Description:** Allows users to register.
  - **Parameters:**
    - `email` (string): Users email.
    - `username` (string): Username.
    - `passsword` (string): Users password.

- **Log in into an account**
  - **Endpoint:** `POST /users/login/`
  - **Description:** Allows users to log in.
  - **Parameters:**
    - `username` (string): Username.
    - `passsword` (string): Users password.

- **Upload Image**
  - **Endpoint:** `POST /images/`
  - **Description:** Allows users to upload images in PNG or JPG format.
  - **Parameters:**
    - `img` (file): The image file to upload.

- **List Images**
  - **Endpoint:** `GET /images/`
  - **Description:** Enables users to list all the images they have uploaded.

- **Get Image Data**
  - **Endpoint:** `GET /images/{id}`
  - **Description:** Enables users to see the image they have uploaded.
  - **Parameters:**
    - `id` (UUID): Image UUID

- **Delete Image Data**
  - **Endpoint:** `DELETE /images/{id}`
  - **Description:** Enables users to delete the image they have uploaded.
  - **Parameters:**
    - `id` (UUID): Image UUID

- **Create Expiring Image Link**
  - **Endpoint:** `POST /images/{id}/create_expiring_link/`
  - **Description:** Users with the ability to create links can create expiring link to their image. The expiry time can be specified in seconds, between 300 and 30000 seconds.
  - **Parameters:**
    - `id` (UUID): The ID of the image.
    - `time_to_live` (int): The expiry time for the link, in seconds.

- **Visit Expiring Image Link**
  - **Endpoint:** `GET /images/{id}/link/`
  - **Description:** Endpoint for getting an original photo of expiring link image.
  - **Parameters:**
    - `id` (UUID): The ID of the image.

- **Get photo**
  - **Endpoint:** `GET /imgs/{file_path}/`
  - **Description:** Endpoint for getting a photo from image model.
  - **Parameters:**
    - `file_path` (string): The path of an image.