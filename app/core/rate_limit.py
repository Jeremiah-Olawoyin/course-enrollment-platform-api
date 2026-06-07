from time import time
from collections import defaultdict
from fastapi import HTTPException, status, Request

auth_rate_limit_store = defaultdict(list)

RATE_LIMIT = 5
RATE_WINDOW = 60

def get_rate_limiter(max_requests: int = RATE_LIMIT, window: int = RATE_WINDOW):
    def rate_limiter(request: Request):
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            client_ip = forwarded.split(",")[0].strip()
        else:
            client_ip = request.client.host if request.client else "unknown"
        
        current_time = time()
        
        auth_rate_limit_store[client_ip] = [
            t for t in auth_rate_limit_store[client_ip] 
            if current_time - t < window
        ]
        
        if len(auth_rate_limit_store[client_ip]) >= max_requests:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Maximum {max_requests} requests per {window} seconds."
            )
        
        auth_rate_limit_store[client_ip].append(current_time)
    return rate_limiter