# Order Processing Project
## Prerequisites
### Setup Instructions
#### Step 1: Clone the Repository
git clone https://github.com/Hamdi-Hossam/order_processing_system.git
#### Step 2: Creat virtual environment
python -m venv venv
#### Step 3: Activate the virtual environment
source venv/bin/activate (on Linux/Mac) or venv\Scripts\activate (on Windows)
#### Step 4: Install the required packages
pip install -r requirements.txt
#### Step 5: Run the application
python run.py
### Docker Instructions
#### Step 1: Pull the Docker image
docker pull ghcr.io/hamdi-hossam/order-processing-system:flask-order-app
#### Step 2: Run the Docker container
docker run -d -p 5000:5000 ghcr.io/hamdi-hossam/order-processing-system:flask-order-app



# Example API Requests and Responses:

### User End points

**POST** `/api/users/register`
### Note: If no provided role field it will be by default "buyer" 
```json
{
    "username":"Hamdi",
    "email":"hamdihossam461@gmail.com",
    "password":"123456",
    "role":"admin"
}
```
**Response:**
*Status Code:* `201 Created`
```json
{
    "message": "User registered successfully"
}
```


**POST** `/api/users/login`
```json
{
    "email":"hamdihossam461@gmail.com",
    "password":"123456"
}
```
**Response:**
*Status Code:* `200 Ok`
```json
{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMzODU2OTk2LCJpYXQiOjE3MzM4NTY2OTYsImp0aSI6ImJhODVhNDc0OTAyOTQyODg4ZWI0NmNkOGIxZGI2ZDBmIiwidXNlcl9pZCI6NH0.gIbEst9oa0zQ4a8oDcnEM6WDJNiJ6pltA15hhd5oymw"
}
```

# Note: All of the upcoming endpoints are authenticated so you need the token to be able to access it, Login for the token.


### Products End points

**POST** `/api/products/add`

```json
{
    "name":"Product 2",
    "description":"A product added by the admin",
    "price":500,
    "stock":100
}
```

**Response:**
*Status Code:* `201 Created`
```json
{
    "message": "Product added successfully.",
    "product": {
        "description": "A product added by the admin",
        "id": 2,
        "name": "Product 2",
        "price": 500,
        "stock": 100
    }
}
```

**GET** `/api/products/get`

**Response:**
*Status Code:* `200 OK`
```json
{
    "page": 1,
    "per_page": 10,
    "products": [
        {
            "description": "A product added by the admin",
            "id": 1,
            "name": "Product 1",
            "price": 500,
            "stock": 100
        },
        {
            "description": "A product added by the admin",
            "id": 2,
            "name": "Product 2",
            "price": 500,
            "stock": 100
        }
    ],
    "total": 2
}
```

### Orders End points

**POST** `/api/orders/add`
```json
{
    "product_quantities": {
        "2": 10
    }
}
```
**Response:**
*Status Code:* `201 Created`
```json
{
    "message": "Product added successfully.",
    "product": {
        "description": "A product added by the admin",
        "id": 2,
        "name": "Product 2",
        "price": 500,
        "stock": 100
    }
}
```

**GET** `/api/orders/get`

**Response:**
*Status Code:* `200 Ok`
```json
{
    "orders": [
        {
            "created_at": "2025-01-29 15:56:47",
            "id": 1,
            "order_products": [
                {
                    "price": 500,
                    "product_id": 1,
                    "product_name": "Product 1",
                    "quantity": 3
                },
                {
                    "price": 500,
                    "product_id": 2,
                    "product_name": "Product 2",
                    "quantity": 1
                }
            ],
            "payment_status": "Unpaid",
            "status": "Pending",
            "total_amount": 2000,
            "user_id": 2
        }
    ]
}
```

### Payment End point
**POST** `/api/payments/pay/:id`
```json
{
    "card_number":"4111111111111111",
    "card_cvv":"822",
    "card_exp_month":10,
    "card_exp_year":2028
}
```
**Response:**
*Status Code:* `200 OK`
```json
{
    "message": "Payment simulated successfully",
    "order_status": "Completed"
}
```

