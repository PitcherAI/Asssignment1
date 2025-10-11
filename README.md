# Telemetry API

This project provides a simple API to query telemetry data. It's built with FastAPI and uses pandas for data manipulation.

## Setup

1.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the server:**

    ```bash
    uvicorn index:app --reload
    ```

    The server will be running at `http://127.0.0.1:8000`.

## API Usage

### `POST /api`

This endpoint retrieves telemetry metrics for specified regions.

**Request Body:**

The request body should be a JSON object with the following keys:

*   `regions` (list of strings): A list of regions to get metrics for.
*   `threshold_ms` (integer, optional): The latency threshold in milliseconds. Defaults to `180`.

**Example Request:**

```json
{
  "regions": ["us-east-1", "eu-west-1"],
  "threshold_ms": 200
}
```

**Response Body:**

The response is a JSON array of objects, where each object contains the metrics for a region.

*   `region` (string): The name of the region.
*   `avg_latency` (float): The average latency in milliseconds.
*   `p95_latency` (float): The 95th percentile latency in milliseconds.
*   `avg_uptime` (float): The average uptime as a value between 0 and 1.
*   `breaches` (integer): The number of times the latency exceeded the `threshold_ms`.

**Example Response:**

```json
[
  {
    "region": "us-east-1",
    "avg_latency": 150.5,
    "p95_latency": 190.2,
    "avg_uptime": 0.99,
    "breaches": 5
  },
  {
    "region": "eu-west-1",
    "avg_latency": 90.1,
    "p95_latency": 120.5,
    "avg_uptime": 1.0,
    "breaches": 0
  }
]
```