
## Requirements

* Python 3.x
* Virtual Environment (venv)

## Local Development Setup

* Create and Configure .env File

Before launching the project, create a .env file by copying the env.example file:
```bash
cp env.example .env
```
Edit the .env file to include your environment-specific configurations (e.g., database credentials, API keys, etc.).

* Create and Activate Virtual Environment

Create a virtual environment and activate it:

For Linux and macOS:

```bash 
python3 -m venv venv
source venv/bin/activate
```

For Windows:

```bash 
python -m venv venv
.\venv\Scripts\activate
```
* Install Dependencies

Install the required dependencies using pip:
```bash 
pip install -r requirements.txt
```

* Run Database Migrations

Run the database migrations using Alembic:
```bash 
alembic upgrade head
```
* Launch the Project
```bash 
python3 main.py
```

## Access the Application
Once the project is running, you can interact with the following URLs:

* API (JSON-based web API): http://localhost:8080/api/v1
* Swagger UI (Interactive API Documentation): http://localhost:8080/docs
* ReDoc (Alternative API Documentation): http://localhost:8080/redoc

## Notes
Ensure your .env file is properly configured before launching the project.
