
# Hospital Management System

This Django-based Hospital Management System is designed to manage doctors, patients, appointments, and medical records. The application includes functionality for patients, doctors, and administrators, each with their specific access and permissions.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
  - [Virtual Environment](#virtual-environment)
  - [Install Requirements](#install-requirements)
  - [Database Migrations](#database-migrations)
  - [Create Superuser](#create-superuser)
- [Usage](#usage)
  - [Starting the Server](#starting-the-server)
  - [Admin Access](#admin-access)
  - [API Usage](#api-usage)
- [Caching](#caching)
- [Project Structure](#project-structure)
- [License](#license)

## Features

- User roles: Patient, Doctor, and Admin
- Secure authentication and permission handling
- Manage and view appointments
- Add, edit, and view medical records
- Custom error pages
- API endpoints for appointments and users (with caching)
- Caching implemented to optimize performance

## Prerequisites

- Python 3.10+
- Django 5.1+
- pip (Python package installer)
- Virtualenv (optional but recommended)
- Redis (for caching)

## Setup

### Virtual Environment

1. **Create a virtual environment:**

   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment:**

   - On Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

### Install Requirements

Once the virtual environment is activated, install the required packages:

```bash
pip install -r requirements.txt
```

### Database Migrations

Before running the project, you need to apply the migrations:

```bash
python manage.py migrate
```

### Create Superuser

To access the admin interface, you need to create a superuser:

```bash
python manage.py createsuperuser
```

## Usage

### Starting the Server

To start the Django development server, run:

```bash
python manage.py runserver
```

Access the application at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

### Admin Access

The admin panel can be accessed at [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/).

### API Usage

The application provides APIs to interact with appointments and user data. The following API endpoints are available:

- **Get all appointments**: `GET /api/appointments/`
- **Get specific appointment**: `GET /api/appointments/<id>/`
- **Create appointment**: `POST /api/appointments/`
- **Update appointment**: `PUT /api/appointments/<id>/`
- **Delete appointment**: `DELETE /api/appointments/<id>/`

#### Example API Request (cURL):

To retrieve all appointments:

```bash
curl -X GET http://127.0.0.1:8000/api/appointments/
```

To create a new appointment (ensure authentication headers are included):

```bash
curl -X POST http://127.0.0.1:8000/api/appointments/ -H "Content-Type: application/json" -d '{"doctor": 1, "patient": 2, "scheduled_at": "2024-09-01T10:00:00Z"}'
```

## Caching

Caching is implemented using Django's built-in caching framework with support for Redis as the cache backend. This improves performance by storing frequently accessed data, such as appointments and user-related data, in the cache.

### Caching Configuration

Make sure Redis is installed and running on your system. Then, configure the cache backend in your `settings.py`:

```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

### Cached Views

- **PatientListView**: Cached patient appointments for 15 minutes based on the user ID.
- **AppointmentListView**: Cached appointment lists with pagination and user-specific filters for 15 minutes.

You can manage the cache timeout and keys for different views and APIs.

To clear the cache, you can run:

```bash
python manage.py cache_clear
```

## Project Structure

```
├── config/
│   ├── settings.py            # Main project settings
│   ├── urls.py                # Project URL configurations
├── web/
│   ├── appointments/
│   │   ├── models.py          # Appointment models
│   │   ├── views.py           # Appointment views with caching
│   ├── users/
│   │   ├── models.py          # User models (Patient, Doctor)
│   ├── templates/             # HTML templates
│   ├── static/                # Static files (CSS, JS, Images)
│   ├── media/                 # Uploaded files (e.g., medical reports)
├── manage.py
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation
```

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
