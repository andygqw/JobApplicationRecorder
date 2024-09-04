# Notice

This flask app has been deprecated. <br>
Click [here](https://github.com/andygqw/JATReact-Worker) to check out newly designed, deployed to CloudFlare, React & Node.JS Job Application Tracker.


# Job Application Tracker - Flask App

This is a web application built with Flask for tracking job applications. It allows users to register, log in, and manage their job application details through a user-friendly interface. The application also provides a profile section where users can update their information.

## Features

- **User Authentication**: Users can sign up, log in, and log out securely using Flask's authentication system.
- **Job Application Management**: Add, view, edit, and delete job applications.
- **User Profiles**: Each user can manage their profile information and see the list of jobs they have applied for.
- **Responsive Design**: Optimized for both desktop and mobile devices.
- **Data Storage**: Uses a database to store user and job application data.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.8+
- Flask (install using `pip install flask`)
- Docker (optional for containerized deployment)

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/andygqw/JobApplicationRecorder.git
   cd job-application-tracker
   ```

2. **Create a virtual environment** (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:

   You need to set up the following environment variables in a `.env` file or export them directly in your shell:

   - `FLASK_APP`: Name of the main app file, typically `run.py`.
   - `FLASK_ENV`: Set to `development` for development mode, or `production` for production mode.
   - `SECRET_KEY`: A secret key for session management.
   - `DATABASE_URL`: The URL for the database connection.

7. **Run the app**:

   ```bash
   flask run
   ```

   The application will be accessible at `http://127.0.0.1:5000/`.

## Docker Setup (Optional)

If you prefer to use Docker, a `Dockerfile` is included to easily set up the app.

1. **Build the Docker image**:

   ```bash
   docker build -t job-app-tracker .
   ```

2. **Run the Docker container**:

   ```bash
   docker run -p 5000:5000 job-app-tracker
   ```

   The application will be accessible at `http://127.0.0.1:5000/`.

## License

This project is licensed under the MIT License