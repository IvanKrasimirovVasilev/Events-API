# TODO - Events API

Ideas and improvements for future development.

## App
- No empty passwords in User.set_password()
- Remove automatic admin privileges for the first registered user.
- Implement secure admin account creation.
- Add an authenticated password change endpoint.

## Tests
- check that empty passwords are rejected
- Refactor integration tests after completing Docker setup 
- Improve integration tests by using an isolated test database.

## Docker — Future Improvements

- Use Gunicorn or another production-ready WSGI server.
- Consider Docker volumes for persistent SQLite storage in local development.
- Add a Docker health check.
- Run the application as a non-root user inside the container.
- Add Docker Compose for easier configuration and startup.


## Future Improvement: Persistent Database (PostgreSQL)

Currently, the Events API uses SQLite with Render's ephemeral filesystem. Database records may be lost after deployments or service restarts.

**Planned improvements:**
- Replace SQLite with PostgreSQL for production.
- Configure the database connection using `DATABASE_URL`.
- Keep SQLite for local development and automated tests.
- Ensure users, events, and RSVPs persist across deployments.
- Test database persistence after redeploying the application.