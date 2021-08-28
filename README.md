# stripe_payment

Project is made with **Python** and **Django Rest Framework**

## Endpoints

- POST /api/v1/create_charge -

request data -

```json
{
    "amount": int,
    "currency": string,
    "description": string,
    "card_number": string,
    "card_exp_month": int,
    "card_exp_year": int,
    "card_cvc": string
}

Example:
{
    "amount": 10000,
    "currency": "INR",
    "description": "First Payment",
    "card_number": "4242424242424242",
    "card_exp_month": 1,
    "card_exp_year": 2025,
    "card_cvc": "100"
}
```

- POST /api/v1/capture_charge/:chargeId - Capture the created charge
- POST /api/v1/create_refund/:chargeId - Refund created charge
- GET /api/v1/get_charges - Get list of all charges

## Dependencies

- Django==3.2.6
- djangorestframework==3.12.4
- stripe==2.60

## Setting Up on Local machine

### Prerequisites

Python 3 is intalled on your system

### Setup

1. Open terminal in stripe_payment directory
1. Run Following commands

```bash
# Create Virual Environment
python -m venv ./venv

# Activate Virtual Environment
./venv/Scripts/Activate

# Install Dependencies
pip install -r requirements.txt
```

### Running the server

Once dependencies are installed run following

```bash
# Sets up migrations scripts to create/update/delete Models if any in database
python manage.py makemigrations

# Runs the migrations
python manage.py migrate
```

Before running the service we need to set `STRIPE_API_KEY` environment variable.

```bash
# Windows Powershell
$ENV:STRIPE_API_KEY = '<your stripe api key>'

# Windows CMD
set STRIPE_API_KEY=<your stripe api key>

# Linux
export STRIPE_API_KEY='<your stripe api key>'
```

Run the server

```bash
python manage.py runserver
```

### Running tests

```bash
python manage.py test
```

## Project Structure

```
Root:
|   - README.md
|
|---stripe_payment
    |   - manage.py
    |   - requirements.txt
    |
    |---payments (module)
    |   |   - apps.py
    |   |   - serializers.py
    |   |   - tests.py
    |   |   - urls.py
    |   |   - utils.py
    |   |   - views.py
    |   |
    |   |---services
    |       - stripe.py
    |
    |---stripe_payment (core App)
            - asgi.py
            - settings.py
            - urls.py
            - wsgi.py
```

### Important files

- **payments/urls.py** - Contains Routes to the endpoints binded with views
- **payments/serializers.py** - Serializing the request
- **payments/views.py** - Entry point to execute code for endpoints
- **payments/services/stripe.py**

### PostMan Collection

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/17277902-a4a594e3-2840-43de-bed9-025fda92b234?action=collection%2Ffork&collection-url=entityId%3D17277902-a4a594e3-2840-43de-bed9-025fda92b234%26entityType%3Dcollection%26workspaceId%3D2eab7260-577b-4ef6-a7d4-1d6948e2e0c8)
