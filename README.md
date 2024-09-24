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

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/ScottShadow/Adonis-Project.git
    cd Adonis-Project
    ```

2.  **Set up virtual environment** (optional, but recommended):

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install the dependencies** from `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

    ## MySQL Installation & Setup

    ### Step 1: Install MySQL

    #### On Ubuntu/Debian:

    1. Update your package index:

       ```bash
       sudo apt update
       ```

    2. Install MySQL:

       ```bash
       sudo apt install mysql-server
       ```

    3. Secure your MySQL installation:

       ```bash
       sudo mysql_secure_installation
       ```

    Follow the on-screen instructions to set a root password and remove any insecure default settings.

    #### On macOS (using Homebrew):

    1. Install MySQL via Homebrew:

       ```bash
       brew install mysql
       ```

    2. Start the MySQL service:

       ```bash
       brew services start mysql
       ```

    3. Set up the root user (you'll be prompted to create a root password):

       ```bash
       mysql_secure_installation
       ```

    #### On Windows:

    1. Download the [MySQL Installer](https://dev.mysql.com/downloads/installer/) for Windows.
    2. Run the installer and choose **MySQL Server** during setup.
    3. Follow the prompts to set up a root password.
    4. Make sure MySQL is added to your system PATH during installation.

    ### Step 2: Set Up MySQL User and Database

    Once MySQL is installed, follow these steps to create the database and user that your app will use:

    1. **Log in to the MySQL server:**

       ```bash
       sudo mysql -u root -p
       ```

       You'll be prompted to enter the root password you set during installation.

    2. **Create a new MySQL database:**

       ```sql
       CREATE DATABASE adonis_project;
       ```

    3. **Create a new MySQL user** (in this case, `root` is already used, but you can add a different user if necessary):

       ```sql
       CREATE USER 'root'@'localhost' IDENTIFIED BY '56213';
       ```

    You can replace `'root'` with a new username, and `'56213'` with your preferred password if you don't want to use the root user directly.

    4. **Grant all privileges** on the database to the user:

       ```sql
       GRANT ALL PRIVILEGES ON adonis_project.* TO 'root'@'localhost';
       ```

    5. **Flush privileges** to apply changes:

       ```sql
       FLUSH PRIVILEGES;
       ```

    6. **Exit** the MySQL shell:

       ```bash
       exit;
       ```

    ### Step 3: Configure Your Flask App to Use MySQL

    Your app uses the following environment variable for the database:

    ```python
    inside the `/api/v2/app.py` file
    DATABASE_URL = os.getenv("DATABASE_URL", "mysql://root:56213@localhost/adonis_project")
    ```

    If you're using `SQLAlchemy`, Flask will automatically pick this up and connect to the MySQL database using the provided credentials.

    ### Step 4: Test the Connection

    1. Run your Flask app with the configured MySQL database:

       ```bash
       python -m api.v2.app
       ```

    2. Check if the app connects successfully to the MySQL database and runs without issues.

    ***

    ### Extra Tips

    - **Connection Issues**: If MySQL is refusing connections, check if the MySQL service is running:

      ```bash
      sudo service mysql status
      ```

      On macOS, use:

      ```bash
      brew services start mysql
      ```

    - **Ports**: Make sure MySQL is running on the correct port (default is `3306`). You can check the port in your `my.cnf` file.

4.  **Configure the environment variables:**

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

   ```bash
   gunicorn -w 4 api.v2.app:app
   or
   waitress-serve --port=5000 api.v2.app:app
   ```

## API Endpoints

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

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
