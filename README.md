# Organization App

## Purpose
The Organization App is a Django-based application that allows users to retrieve data using a NIP (Numer Identyfikacji Podatkowej) number by interacting with the RegonAPI. This application is designed to facilitate access to organizational data in Poland.

## Getting Started

### Prerequisites
- Docker and Docker Compose installed on your machine.
- An API key from the RegonAPI service. You can obtain your API key by visiting [RegonAPI](https://api.stat.gov.pl/Home/RegonApi).

### Logging In
1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Create a `.env` file in the root directory and add your API key:
   ```
   REGONAPIKEY=your_api_key_here
   ```

### Running the Application
To start the application, run the following command in your terminal:
```
docker-compose up
```
This command will build the Docker containers and start the application. You can access the application at `http://localhost:8000`.

### Running Tests
To run the tests for the application, use the following command:
```
docker-compose run --rm app sh -c "pytest"
```
This command will execute the tests defined in this application.
> `pytest` is configured via `pytest.ini` with the correct Django settings module.

## Documentation
- You can access the Swagger documentation for the API at: [Swagger Documentation](http://localhost:8000/schema/swagger/)
- The Django admin interface can be accessed at: [Admin Interface](http://localhost:8000/admin/)    

Create a superuser:

```bash
docker-compose run --rm app sh -c "python manage.py createsuperuser"
```
## 📮 License

MIT – free to use, modify and distribute.