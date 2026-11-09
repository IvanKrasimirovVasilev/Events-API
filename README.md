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

## Production Deployment & CI/CD
The Events API is deployed as a Docker container on Render. GitHub Actions runs automated tests and deploys changes from the main branch after the tests pass.

## Live services
Resource	URL
Production API	https://events-api-ivan.onrender.com
Health check	https://events-api-ivan.onrender.com/api/health
Swagger UI	https://events-api-ivan.onrender.com/apidocs/
OpenAPI specification	https://events-api-ivan.onrender.com/api/openapi.yaml
Docker Hub image	https://hub.docker.com/r/vasilevivan/events-api
GitHub Actions	https://github.com/IvanKrasimirovVasilev/Events-API/actions

### Deployment infrastructure
- Container registry: Docker Hub (vasilevivan/events-api:latest)
- Hosting: Render Web Service (events-api-ivan), Frankfurt region, Free instance
- Container port: 5000; the Flask app binds to 0.0.0.0
- Database: SQLite by default (suitable for this educational demo, not durable production storage)
- Workflow: .github/workflows/ci.yml
- GitHub Environment: production, restricted to deployments from main

### GitHub Environment configuration
Configure the following under Repository Settings → Environments → production:
Name	Type	Purpose
DOCKERHUB_USERNAME	Secret	Docker Hub account used to publish the image
DOCKERHUB_TOKEN	Secret	Docker Hub personal access token with image push permission
RENDER_DEPLOY_HOOK	Secret	Private Render URL used to trigger a deployment
RENDER_BASE_URL	Variable	https://events-api-ivan.onrender.com, used by the smoke test

On the Render service, configure SECRET_KEY and JWT_SECRET_KEY as environment variables with strong, independent values. The application reads them from the environment through config.py. Never commit actual secret values or the Render deploy hook URL to Git.

### Automated deployment workflow
A push to main triggers the following pipeline:
1. Build and test: GitHub Actions builds the Docker image, starts the API container, checks /api/health, runs the pytest suite, and cleans up the test container.
2. Publish: If tests pass, the deploy job logs in to Docker Hub, builds vasilevivan/events-api:latest with the current Git commit SHA, and pushes it.
3. Deploy: GitHub Actions calls the private Render deploy hook to deploy the updated image.
4. Smoke test: The workflow repeatedly requests the production /api/health endpoint until the service reports healthy and its version matches the commit SHA being deployed. This prevents an older healthy container from being mistaken for the new release.
The deploy job runs only for pushes to main, not for pull requests. A failed test prevents deployment.

### Version-aware health check
The Dockerfile accepts a build argument called GIT_SHA and exposes it to the app as an environment variable. The health endpoint returns it as version:
{
  "status": "healthy",
  "version": "8233fa3038175d512b33adc709a75e0505457c18"
}
This example is from the first successful automated deployment (GitHub Actions run #8, November 9, 2026). The version changes with subsequent deployments. A local image built without --build-arg GIT_SHA=... reports "version": "unknown".

To check the live service manually:
curl https://events-api-ivan.onrender.com/api/health

### Manual Docker image build and push
For troubleshooting or manual publishing (requires Docker Hub authentication):
docker build -t vasilevivan/events-api:latest .
docker push vasilevivan/events-api:latest
A manual push alone does not necessarily redeploy the Render service; use the Render dashboard to initiate a new deployment if needed. The normal release path is the GitHub Actions pipeline.

### Operational limitations
- Render Free instances may spin down when idle. The first request after inactivity can take extra time.
- SQLite is not persistent on Render's ephemeral filesystem. Redeployments or instance replacement may erase registered users, events, and RSVPs. Use a managed persistent database (for example PostgreSQL) for a real production service.
- The current container starts Flask's development server. It is acceptable for this learning exercise but should be replaced with a production WSGI server such as Gunicorn before operating a real public service.
- The first registered user becomes an admin. This demo behavior is not suitable for an unrestricted real-world deployment.
- Docker Hub access tokens can expire and may need rotation in GitHub Environment secrets.

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

