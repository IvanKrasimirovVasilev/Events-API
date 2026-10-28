# TODO - Events API

Ideas and improvements for future development.

## App
- No empty passwords in User.set_password()

## Tests
- check that empty passwords are rejected
- Refactor integration tests after completing Docker setup 

## Docker — Future Improvements

- Disable Flask debug mode in production.
- Use Gunicorn or another production-ready WSGI server.
- Configure `SECRET_KEY` and `JWT_SECRET_KEY` through environment variables.
- Add Docker volumes for persistent SQLite storage.
- Consider PostgreSQL instead of SQLite for production.
- Add a Docker health check.
- Run the application as a non-root user inside the container.
- Add Docker Compose for easier configuration and startup.
- Automate Docker image builds and tests with GitHub Actions.
- Improve integration tests by using an isolated test database.

