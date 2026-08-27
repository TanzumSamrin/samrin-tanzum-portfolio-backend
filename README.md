# Portfolio Backend

Django REST API backend for a personal portfolio project. This repository provides models, API endpoints, and admin configuration for accounts, blog, projects, portfolio, and interactions.

## Features

- REST API endpoints for portfolio-related resources
- Admin site configuration and user management
- Pagination and basic permissions for endpoints

## Requirements

- Python 3.8+
- See requirements.txt for full dependency list

## Setup (local)

1. Create and activate a virtual environment:

   - Windows (PowerShell):
     powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     

   - Windows (cmd):
     cmd
     python -m venv venv
     venv\Scripts\activate.bat
     

2. Install dependencies:

   bash
   pip install -r requirements.txt
   

3. Apply database migrations:

   bash
   python manage.py migrate
   

4. (Optional) Create a superuser for the admin site:

   bash
   python manage.py createsuperuser
   

5. Run the development server:

   bash
   python manage.py runserver
   

## Running Tests

Run the test suite with:

bash
python manage.py test


## Environment & Configuration

- For production or advanced local setups, provide environment variables (e.g., DJANGO_SECRET_KEY, database config) via a .env file or your environment manager.

## Contributing

Contributions are welcome. Open an issue or submit a pull request with a clear description of changes.

## License

This project does not include a license file. Add a LICENSE if you want to apply an open-source license.

## Contact

If you have questions, open an issue or contact the repository owner.

## Demo Superuser Credentials
- Username: admin1
- Password: admin1