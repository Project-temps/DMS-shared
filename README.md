# DMS

DMS (Data Management System) combines Django with Dash to provide interactive dashboards and APIs for handling data ingestion, processing and visualization.

## Setup

1. Clone the repository and create a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure environment variables (for development add them to `.env` or your shell profile):
   ```bash
   export DJANGO_SECRET_KEY=your_secret_key
   export DJANGO_DEBUG=True
   ```
   The application uses SQLite by default, but you can adjust database settings in `myproject/settings.py`.
4. Run migrations:
   ```bash
   python manage.py migrate
   ```
5. Create an admin user:
   ```bash
   python manage.py createsuperuser
   ```
6. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Usage

After starting the server, visit `http://127.0.0.1:8000` to access the web interface and dashboards. Log in with the superuser credentials to manage data and users.
