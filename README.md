# 📚 Book Management System

Book Management System with AI integration.

This project works as a complete book management system with AI-powered features.

## 🚀 Features

The project contains 5 modules:

1. Users  
   - Create users  
   - Get users  

2. Authentication  
   - Login API  
   - Token-based authentication  

3. Books  
   - Create, update, delete books  
   - Other book-related operations  

4. Reviews  
   - Add ratings and reviews for books  

5. AI Features  
   - Book summaries  
   - Book recommendations  

## ⚙️ Setup

### Environment Variables (.env)

Add the following details in the `.env` file:

DATABASE_URL="postgresql+asyncpg://postgres:database_user_name@localhost:5432/database_name"  
DATABASE_URL_SYNC="postgresql+psycopg://postgres:database_user_name@localhost:5432/database_name"

Replace the database configuration with your own database details.

Add a secret key:

SECRET_KEY="any_random_secret_key"

### Python Virtual Environment

Create a virtual environment:

python -m venv env

Activate environment:

env\Scripts\activate

### Install Requirements
Navigate to the `app` folder and run:

pip install -r requirements.txt

## 🗄️ Database Migrations

Create migrations:

alembic revision --autogenerate -m "initial migrations"

Apply migrations:

alembic upgrade head

## 🤖 AI Integration Setup

Create a Hugging Face account and generate a secret key.

Add the key in `.env`:

AI_MODEL_KEY="your_huggingface_secret_key"

You can also change the AI model by updating:

AI_MODEL="your_preferred_model"

## ▶️ Run the Project

uvicorn main:app --reload

## 📖 API Documentation

After running the project locally, access the API documentation:

http://localhost:8000/docs

## 🧪 Running Test Cases

Run test cases using the following commands:

User module:  
pytest -v tests/users_tests.py

Book module:  
pytest -v tests/books_tests.py

Review module:  
pytest -v tests/review_tests.py

## 🔐 API Testing

First, create a user:

POST /api/v1/user/

Use a valid email and password.

Then login to get the auth token:

POST /api/v1/auth/login/

These are the only APIs that do not require authentication.

All other APIs require an auth token.

Provide the token in request headers:

Authorization: Bearer {auth_token}

## 📂 Project Structure

├── app/  
│   ├── ai_features/        # API services related to AI features  
│   ├── alembic/            # Database migration history  
│   ├── api/                # API route handlers (v1)  
│   ├── auth/               # Login and authentication handling  
│   ├── books/              # Book CRUD operations  
│   ├── core/               # Configuration, security, database connection  
│   ├── reviews/            # Book reviews and ratings  
│   ├── tests/              # Pytest test suite  
│   └── users/              # User handling  

├── .env                    # Environment variables (Git ignored)  
├── main.py                 # Application entry point  
├── requirements.txt        # Project dependencies
