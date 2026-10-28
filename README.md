# Evently API

A Flask-based REST API for managing events and RSVPs with different access levels. This API is designed to teach web security best practices through incremental improvements.

## Features

- **Public Events**: Anyone can RSVP without authentication
- **Protected Events**: Requires user authentication to RSVP
- **Admin Events**: Requires admin role to RSVP

## Tech Stack

- Flask 3.0.0
- Flask-SQLAlchemy (SQLite database)
- Flask-CORS
- Flask-JWT-Extended (JWT authentication)

## Setup

1. Create and activate a virtual environment:

   **Windows:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   **Linux/Mac:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```
The API will be available at `http://localhost:5000`

## Running with Docker

Build the Docker image:

```bash
docker build -t events-api .
```

Start the container:

```bash
docker run -d -p 5000:5000 --name events-api-container events-api
```

The API is available at `http://localhost:5000`.

Swagger UI: `http://localhost:5000/apidocs`

Verify the API:

```bash
curl http://localhost:5000/api/health
```

Run the automated tests while the container is running:

```bash
python -m pytest tests/ -v
```

**Test result:** 9 tests passed.

### Container Management

```bash
docker ps                          # List running containers
docker logs events-api-container   # View logs
docker stop events-api-container   # Stop container
docker start events-api-container  # Start existing container
docker rm events-api-container     # Remove stopped container
```

**Note:** SQLite data is stored inside the container and will be lost when the container is removed. This Docker setup is intended for development and testing.

## Automated Tests

The project uses **Pytest** for unit and integration testing.

Run all tests:

```bash
python -m pytest tests/ -v
```

### Unit Tests

- **Password Hashing** — Verifies that user passwords are securely hashed and can be validated.

### Integration Tests

- **Health Check** — Verifies that the API returns a healthy status.
- **User Registration** — Tests successful user registration.
- **User Login** — Tests authentication and JWT token generation.
- **Event Creation** — Tests creating an event with authentication.
- **Event RSVP** — Tests the RSVP functionality.
- **Duplicate Registration** — Verifies that duplicate usernames are rejected.
- **Unauthorized Event Creation** — Ensures unauthenticated users cannot create events.
- **Unauthorized Private RSVP** — Ensures unauthenticated users cannot RSVP to protected events.

**Current status:** 9 tests passing (1 unit test, 8 integration tests).

### Maintaining Test Documentation

**Important:** Whenever a new test is added, modified, or removed, please update this README to keep the test descriptions and total test count accurate.

## Swagger UI Documentation

The API includes interactive Swagger UI documentation. After starting the server:

1. Open your browser and navigate to: `http://localhost:5000/apidocs`

2. You'll see an interactive API documentation interface where you can:
   - Browse all available endpoints
   - See request/response schemas
   - Test endpoints directly from the browser
   - Authenticate using the "Authorize" button (enter your JWT token)

3. To use the "Authorize" button:
   - First, login via `/api/auth/login` to get your JWT token
   - Click the "Authorize" button at the top of the Swagger UI
   - Enter: `Bearer <your_jwt_token>` (replace `<your_jwt_token>` with your actual token)
   - Now you can test protected endpoints directly from Swagger UI

**Alternative**: You can also view the OpenAPI specification directly at `http://localhost:5000/apispec_1.json`

## API Endpoints

### Authentication

- `POST /api/auth/register` - Register a new user
  ```json
  {
    "username": "user123",
    "password": "password123"
  }
  ```

- `POST /api/auth/login` - Login and get JWT token
  ```json
  {
    "username": "user123",
    "password": "password123"
  }
  ```

### Events

- `GET /api/events` - Get all events
- `GET /api/events/<id>` - Get a specific event
- `POST /api/events` - Create a new event (requires authentication)
  ```json
  {
    "title": "Python Meetup",
    "description": "Monthly Python developer meetup",
    "date": "2026-01-15T18:00:00",
    "location": "Tech Hub, Room 101",
    "capacity": 50,
    "is_public": true,
    "requires_admin": false
  }
  ```

### RSVPs

- `POST /api/rsvps/event/<event_id>` - RSVP to an event
  ```json
  {
    "attending": true
  }
  ```

- `GET /api/rsvps/event/<event_id>` - Get all RSVPs for an event

## Authentication

For protected endpoints, include the JWT token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

## Security Notes

This is a basic implementation designed for educational purposes. The following security considerations are intentionally simplified and can be improved in subsequent lessons:

- Password storage (currently using werkzeug, but can be improved)
- JWT token handling
- Input validation
- SQL injection prevention (SQLAlchemy helps, but can be improved)
- Rate limiting
- CORS configuration
- Error handling and information disclosure

## Database

The application uses SQLite by default. The database file (`events.db`) will be created automatically on first run.

**Note**: The first user registered automatically becomes an admin for demo purposes.

