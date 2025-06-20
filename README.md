# Lead Redirect Service

FastAPI-based service for lead redirection and management.

## Prerequisites

- Docker and Docker Compose
- Python 3.12+ (for local development)

## Environment Variables

The service can be configured using the following environment variables:

- `WWW_SH_HOST` - Host to bind the service (default: 0.0.0.0)
- `WWW_SH_PORT` - Port to run the service on (default: 8000)
- `WWW_SH_WORKER` - Number of workers (default: CPU cores * 2 + 1)

## Quick Start

1. Clone the repository:
```bash
git clone <repository-url>
cd lead-redirect-service
```

2. Start the service using Docker Compose:
```bash
docker-compose up --build
```

The service will be available at http://localhost:8000

## Local Development

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the service:
```bash
./start
```

## API Documentation

Once the service is running, you can access:
- Swagger UI documentation at `/docs`
- ReDoc documentation at `/redoc`

## Project Structure

```
.
├── app/
│   ├── endpoints/    # API endpoints
│   ├── schemas/     # Pydantic models
│   ├── services/    # Business logic
│   └── settings/    # Application configuration
├── docker-compose.yml
├── Dockerfile
├── main.py          # Application entry point
└── start           # Start script
``` 