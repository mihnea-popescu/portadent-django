# Portadent Django Backend

This repository contains the Django backend for Portadent - an AI-powered dental scanning application that helps users identify potential dental issues through photo analysis.

## 🎥 Demo

Check out the [demonstration video](https://www.youtube.com/shorts/uDWKXwFe99M) to see Portadent in action!

## 🌟 Features

- RESTful API built with Django REST Framework
- JWT Authentication
- Celery task queue for asynchronous processing
- OpenAI GPT-4 Vision integration for dental analysis
- PostgreSQL database
- Redis for caching and message broker
- Docker containerization
- Email notifications
- Image processing and resizing
- Password reset functionality
- Automated deployment with GitHub Actions

## 🏗️ Architecture

The application is built using:

- Django 4.2.16
- Python 3.9.6
- PostgreSQL 13
- Redis
- Celery
- Docker & Docker Compose
- Gunicorn for production deployment

## 🚀 Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.9+
- PostgreSQL 13+

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```bash
SECRET_KEY=your-secret-key
DEBUG=True
POSTGRES_DB=your-db-name
POSTGRES_USER=your-db-user
POSTGRES_PASSWORD=your-db-password
EMAIL_HOST=your-email-host
EMAIL_PORT=your-email-port
EMAIL_HOST_USER=your-email-user
EMAIL_HOST_PASSWORD=your-email-password
EMAIL_USE_TLS=True/False
EMAIL_USE_SSL=True/False
FRONTEND_URL=http://localhost:3000
OPENAI_API_KEY=your-openai-key
```

### Installation

1. Clone the repository:

```bash
git clone https://github.com/portadent/backend.git

cd portadent-django
```

2. Build and start the Docker containers:

```bash
docker compose up --build
```

3. Run migrations

```bash
docker exec portadent-django python manage.py migrate
```

## 🔄 Related Projects

- [Portadent Frontend (Next.js)](https://github.com/mihnea-popescu/portadent-nextjs)

## 🛠️ Development

The project uses Docker Compose for development. The development environment includes:

- Django web server
- PostgreSQL database
- Redis for caching and Celery
- Celery worker and beat scheduler
- MailHog for email testing (in debug mode)

## 📦 Deployment

The project includes GitHub Actions workflow for automated deployment. The workflow:

- Triggers on push to master branch
- Builds and tests the application
- Deploys to production server via SSH
- Runs database migrations
- Restarts Docker containers

## 🔒 Security

- JWT authentication for API endpoints
- Password hashing
- CSRF protection
- Environment variable management
- Secure password reset flow

## 📝 API Documentation

Key API endpoints:

- `/auth/` - Authentication endpoints
- `/user/` - User management
- `/scan/` - Scan creation and management
- `/scan-photo/` - Photo upload and management
- `/web-scan/` - Web-based scanning flow
- `/password-reset/` - Password reset functionality

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- Mihnea Popescu [GitHub Profile](https://github.com/mihnea-popescu)

## 🙏 Acknowledgments

- OpenAI for GPT-4 Vision API
- Django community
- Docker community
