# Aktos Project

## Overview
The Aktos Project is a Django-based web application designed for a collection agency to manage and retrieve account data for their clients. It provides functionality to ingest CSV data files containing account information and offers APIs to filter and retrieve the data based on various parameters.

## Features
- **Data Ingestion**: Ingest CSV files containing account and consumer data.
- **Account Management**: Manage accounts, consumers, and debts for multiple clients and agencies.
- **Filtering API**: Retrieve accounts using flexible query parameters like balance range, consumer name, and debt status.
- **Pagination**: Paginated API responses for efficient data handling.
- **Scalable Design**: Supports modeling for multiple agencies and clients.

## Requirements
- Python 3.10 or higher
- Django 5.0.3
- Django REST Framework

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd aktos_project
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```bash
   python manage.py migrate
   ```

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

## API Endpoints
### `/accounts`
Retrieve a list of accounts for a collection agency and their clients. Supports filtering by the following query parameters:
- **min_balance**: Minimum balance to filter accounts by (inclusive).
- **max_balance**: Maximum balance to filter accounts by (inclusive).
- **consumer_name**: Filter accounts by the consumer's name.
- **status**: Filter accounts by the debt status (e.g., `in_collection`, `collected`).

#### Example Requests
1. `GET /accounts?min_balance=100&max_balance=1000&status=in_collection`
2. `GET /accounts?min_balance=100.23&status=collected&consumer_name=john`

### `/upload-csv` 
Upload a CSV file containing account data for ingestion.

## Pagination
The API uses **offset-based pagination**:
- **Pros**: Simple to implement and works well for datasets with a predictable size.
- **Cons**: Performance may degrade for very large datasets due to increasing offsets.

## Configuration
- **Settings**: Update `config/settings.py` to configure database, allowed hosts, and other settings.
- **Environment Variables**: Use environment variables to manage sensitive data like `SECRET_KEY`.

## Testing
Run the test suite to ensure the application works as expected:
```bash
python manage.py test
```

## Deployment
Deploy the application to a platform like Heroku or AWS. We used Render, but is your choice
Ensure the following:
- Use a production-ready database (e.g., PostgreSQL).
- Configure environment variables for sensitive data.

## Future Improvements
- Add support for real-time updates to account data.
- Implement advanced filtering and sorting options.
- Optimize database queries for large datasets.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
