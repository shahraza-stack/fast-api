FastAPI Prediction Service with Redis

This project implements a prediction service using FastAPI for asynchronous predictions and Redis for storing the prediction results. The service allows users to submit prediction requests and retrieve the results asynchronously.
Approach

The goal of this service is to handle large prediction tasks in an efficient and scalable way. When a request is made for a prediction, the service can process the task asynchronously, allowing the client to check the status of the prediction using a unique prediction_id.

    Asynchronous Processing: If the request header async_mode is set to true, the prediction task is processed in the background using FastAPI's BackgroundTasks.
    Redis Storage: The results of predictions are stored in Redis under a hash, keyed by prediction_id. This allows for quick retrieval of results once the prediction is complete.
    Dockerized Application: Both the FastAPI application and Redis are containerized using Docker, ensuring easy deployment and environment consistency.

Prerequisites

    Docker and Docker Compose installed.
    A running Redis instance (handled by Docker Compose in this case).

How to Run the Project

Follow these steps to build and run the containers using Docker Compose.
1. Navigate to the Project Directory

Open your terminal and change to the project directory:

cd Sych/sych-assesment

2. Build and Start the Containers

Option 1: Using Docker Build and Run

    Build the FastAPI application container:

docker-compose up --build

This will:

    Rebuild both the FastAPI and Redis containers.
    Restart the services.

3. Access the Application

Once the containers are running, you can access the FastAPI application in your browser at:

http://localhost:8080

Troubleshooting

If you encounter any issues:

    Ensure that Docker is running on your machine.

    Check the container logs for errors:

docker logs fastapi-app-container

Verify that Redis is working correctly:

docker-compose logs redis

Test the Application:

    To submit a prediction request asynchronously, use the POST /predict endpoint with the async_mode header set to true.

    Example Request:

curl -X 'POST' \
'http://localhost:8080/predict' \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-H 'async_mode: true' \
-d '{
  "input": "some_input_data"
}'

Response:

{
  "input": "Sample input data for the model",
  "result": "1234"
}

To check the prediction status, use the GET /predict/{prediction_id} endpoint.

Example Request:

curl -X 'GET' 'http://localhost:8080/predict/{prediction_id}'

Response:

    If the prediction is still processing:

{
  "error": "Prediction is still being processed."
}

If the prediction is complete:

{
  "input": "some_input_data",
  "result": "generated_result"
}

If the prediction ID is not found:

            {
              "error": "Prediction ID not found."
            }

Assumptions

    Redis is used for in-memory storage: We assume that Redis is available and working correctly in the environment. It is used here for storing prediction results, making it fast for retrieval.

    The predictions are simple and can be mocked: In this implementation, the prediction is mocked with a random result (uuid.uuid4().int % 10000). In a real-world application, this would be replaced with actual prediction logic (e.g., machine learning models).

    Asynchronous handling is required for scalability: Since prediction tasks can take time, processing them asynchronously is crucial for improving the user experience and system performance.

Alternative Approaches Considered

    Using a Task Queue (e.g., Celery):
        Pros: Using Celery or similar task queues would allow for more robust task management (e.g., retrying failed tasks, scheduling tasks).
        Cons: The complexity of setting up and managing Celery with Redis adds overhead, and for the scope of this project, the background task feature provided by FastAPI is sufficient.

    Storing Results in a Database:
        Pros: Using a relational database (e.g., PostgreSQL) could offer persistent storage and more complex querying capabilities.
        Cons: Redis was chosen here due to its fast, in-memory nature and simplicity for this use case. A database might be overkill unless the data needs to persist for longer periods or requires complex queries.

    Using HTTP Polling vs. WebSocket:
        Pros: WebSocket would provide real-time updates for the client, allowing immediate feedback as soon as the prediction is done.
        Cons: For simplicity, HTTP polling was chosen because it provides a straightforward way to check the status of the prediction.

Troubleshooting

    Redis Connection Issues: If Redis is not starting or FastAPI cannot connect to it, ensure that Redis is running on localhost:6379. If you are using Docker, check the logs for any errors related to Redis initialization.

    Prediction ID not found: If you are getting a 404 Not Found error when checking the prediction status, ensure that the prediction_id you are using is correct and that the prediction was processed correctly.

Conclusion

This project demonstrates an easy-to-deploy FastAPI-based prediction service using Docker and Redis. It handles asynchronous prediction tasks efficiently, with results stored in Redis for quick access. The setup is simple, scalable, and can be easily extended with additional features or more complex prediction logic.