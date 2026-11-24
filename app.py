
from flask import Flask, jsonify, request
import redis

app = Flask(__name__)

# Connect to Redis
r = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True
)

# Rate limit settings
LIMIT = 5
WINDOW = 60

# Atomic Fixed Window Counter
rate_limiter = r.register_script("""
local current = tonumber(redis.call('GET', KEYS[1]) or '0')
local limit = tonumber(ARGV[1])
local window = tonumber(ARGV[2])

if current >= limit then
    return {-1, redis.call('TTL', KEYS[1])}
end

local count = redis.call('INCR', KEYS[1])

if count == 1 then
    redis.call('EXPIRE', KEYS[1], window)
end

return {count, redis.call('TTL', KEYS[1])}
""")

@app.route("/")
def home():
    return "Rate Limiter Application is Running! This is for testing only. Developed by Atanu Paul"

@app.route("/api/resource")
def resource():

    user_id = request.remote_addr or "unknown"
    key = f"rate_limit:{user_id}"

    result = rate_limiter(
        keys=[key],
        args=[LIMIT, WINDOW]
    )

    count = int(result[0])
    remaining_time = max(0, int(result[1]))

    if count == -1:
        return jsonify({
            "status": "blocked",
            "message": "Rate limit exceeded!",
            "retry_after": remaining_time
        }), 429

    return jsonify({
        "status": "success",
        "message": "Request allowed!",
        "requests_used": count,
        "remaining_requests": LIMIT - count,
        "window_seconds": remaining_time
    }), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)