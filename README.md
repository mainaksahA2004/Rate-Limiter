
# Rate Limiter Using Flask and Redis

## Project Overview
This project implements a Fixed Window Counter Rate Limiter using Python Flask and Redis (Memurai).

It limits each client to 5 requests within 60 seconds.

## Technologies Used
- Python
- Flask
- Redis / Memurai
- Postman

## Features
- Request counting
- Fixed Window Counter algorithm
- Automatic key expiration using TTL
- HTTP 429 response when the limit is exceeded
- Atomic request processing using Redis Lua scripting

## Installation

Install the required packages:

pip install -r requirements.txt

## Run the Application

python app.py

## Rate Limit Configuration
- Maximum Requests: 5
- Time Window: 60 seconds

## Expected Results
- First 5 requests: HTTP 200 (Allowed)
- 6th request: HTTP 429 (Blocked)

## Database
Redis stores the request counter for each client IP address.
The counter automatically expires after 60 seconds.
