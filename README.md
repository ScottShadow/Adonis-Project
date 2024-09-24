# Adonis Project

This is a Flask-based web application designed to track user habits and logs, providing an XP system based on activity frequency.

## Table of Contents

- [Project Overview](#project-overview)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Database Setup](#database-setup)
- [API Endpoints](#api-endpoints)
- [License](#license)

## Project Overview

The **Adonis Project** is a habit-tracking app built with Flask and MySQL, featuring user authentication, habit logging, and an XP-based system to reward consistency. This project includes a dashboard where users can monitor their progress, view logs, and manage habits.

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: MySQL
- **Frontend**: HTML, CSS (with possible JS)
- **Deployment**: Gunicorn (for production) and Flask's development server

## Installation

### Prerequisites

Ensure you have the following installed:

- Python 3.x
- MySQL
- `pip` for installing Python packages

### Steps

1. **Clone the repository:**

   ```bash
   git clone https://github.com/ScottShadow/Adonis-Project.git
   cd Adonis-Project
   ```

2. **Set up virtual environment** (optional, but recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the dependencies** from `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the environment variables:**

   Create a `.env` file or update your environment with your Flask configuration and MySQL connection details:

   ```bash
   FLASK_APP=api.v2.app
   FLASK_ENV=development
   SQLALCHEMY_DATABASE_URI=mysql+pymysql://username:password@localhost/dbname
   SECRET_KEY=your_secret_key
   ```

## Running the Application

1. **Run the app:**

   You can start the app using:

   ```bash
   python -m api.v2.app
   ```

   The application should now be running at `http://127.0.0.1:5000/`.

2. **Run in Production:**

   If deploying, use Gunicorn for better performance in production environments:

   ```bash
   gunicorn -w 4 api.v2.app:app
   ```

## Database Setup

1. **Create a MySQL database:**

   In your MySQL shell or using a GUI like phpMyAdmin:

   ```sql
   CREATE DATABASE adonis_project;
   ```

2. **Apply the database migrations** (if using Flask-Migrate or Alembic):

   ```bash
   flask db upgrade
   ```

3. **(Optional) Seed the database** with initial data if you have a seeder script:

   ```bash
   python -m api.v2.seeder_script  # Adjust to your seeder file path
   ```

## API Endpoints

Here are some key API endpoints that the application supports:

### Authentication

- **POST** `/login` - Log in a user
- **POST** `/signup` - Sign up a new user
- **POST** `/logout` - Log out the current user

### Logs & Habits

- **GET** `/logs` - Retrieve all logs for the current user
- **POST** `/logs` - Create a new log entry
- **PUT** `/logs/<log_id>` - Update a log entry
- **DELETE** `/logs/<log_id>` - Delete a log entry

### User Profile

- **GET** `/profile` - View user profile data
- **PUT** `/profile` - Update profile information

Feel free to expand this section as you add more functionality.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
