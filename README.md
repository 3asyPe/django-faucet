# Django Faucet

This project is a Django-based faucet application that allows users to request funds to be sent to their Ethereum wallet addresses. The application uses Celery for background tasks and Redis as the message broker.

## Features

- API endpoint to request funds
- API endpoint to get transaction statistics
- Celery tasks to check pending transactions
- Dockerized setup for easy deployment

## Prerequisites

- Docker
- Docker Compose

## Getting Started

### Clone the Repository

```sh
git clone git@github.com:3asyPe/django-faucet.git
cd django-faucet
```

## Build and Run the Containers

Use Docker Compose to build and run the containers:

```sh
docker-compose up --build
```

This command will:

Build the Docker images.
Start the PostgreSQL, Redis, Django, Celery, and Celery Beat services.

## Access the Application
The Django application will be available at http://localhost:8000.

## API Endpoints
- Fund API: ```POST /fund```
  - Request body: ```{ "wallet_address": "your_wallet_address" }```
  - Response: ```{ "transaction_id": "transaction_id" }```
- Stats API: ```GET /stats```
  - Response: ```{ "successful_transactions": count, "failed_transactions": count }```