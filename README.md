# Simple Chat Application

This is a simple chat application built for learning Django. It stores user data and messages in an unencrypted format and uses websockets for client communication. The application uses Daphne, a Django Channels HTTP/WebSocket server, and SQLite for the database.

## Features

- User authentication and management
- Real-time messaging using websockets
- Online user tracking using Redis
- A "Contact Us" form for feedback

## Tech Stack

- Django for the backend
- Daphne as the HTTP/WebSocket server
- SQLite as the database
- Redis for online user tracking
- Docker for containerization

## Running the Application

The application is containerized using Docker. To run it, you need to have Docker installed on your machine. Once you have Docker set up, you can start the application using the following steps:

1. Open a terminal in the project directory.
2. Build the Docker image using the command: `docker-compose build`
3. Run the Docker container using the command: `docker-compose up`

The application will then be accessible at `http://localhost:8000`.

This application is intended for educational purposes. In a production environment, consider using HTTPS and encrypting sensitive data.
