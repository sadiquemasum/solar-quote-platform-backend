# Solar Quote Platform Backend

## Overview

A full-stack solar quotation platform with Django backend API and React + TypeScript frontend.

---

## Backend

### Requirements

- Python 3.14
- Django 6.0
- Django REST Framework
- ...

### Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate

## Create a superuser for the admin access
python manage.py createsuperuser

## run the development server
python manage.py runserver

## The admin app page should now be running in development mode, typically accessible at
http://localhost:8000/admin

## API Endpoints

### Create a Quote
**POST** `/api/quotes/`
- Description: Create a new quote.

### Dashboard Quotes
**GET** `/api/quotes/dashboard/`
- Description: Retrieve quotes for the authenticated user's dashboard.
- Authentication: Required

### Public Quotes by Email
**GET** `/api/quotes/public/?email=<email>`
- Description: Retrieve public quotes associated with a specific email.
- Parameters:
  - `email` (query) – Email address to filter public quotes.
```
