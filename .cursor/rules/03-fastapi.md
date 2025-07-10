# FastAPI Development Guidelines

## API Structure
Organize endpoints and dependencies:

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import AsyncGenerator, Optional

# Security
security = HTTPBearer()

# Dependency Injection
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Provide database session."""
    async with async_session() as session:
        yield session

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """Get current authenticated user."""
    token = credentials.credentials
    user = await validate_token(token, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    return user
```

## Request/Response Models
Define clear Pydantic schemas:

```python
from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional, Any
from datetime import datetime

class FiberPredictionRequest(BaseModel):
    """Request model for fiber prediction."""
    
    target_properties: Dict[str, float] = Field(
        ..., 
        description="Target material properties",
        example={"tensile_strength": 500.0, "elastic_modulus": 10.0}
    )
    constraints: Optional[Dict[str, Any]] = Field(
        None, 
        description="Optional constraints for prediction"
    )
    max_results: int = Field(
        10, 
        ge=1, 
        le=100,
        description="Maximum number of recommendations"
    )
    
    @validator("target_properties")
    def validate_properties(cls, v: Dict[str, float]) -> Dict[str, float]:
        """Validate target properties."""
        required_props = {"tensile_strength", "elastic_modulus"}
        if not required_props.issubset(v.keys()):
            raise ValueError(f"Missing required properties: {required_props - v.keys()}")
        
        # Validate ranges
        for prop, value in v.items():
            if value <= 0:
                raise ValueError(f"{prop} must be positive")
        
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "target_properties": {
                    "tensile_strength": 500.0,
                    "elastic_modulus": 10.0,
                    "density": 1.5
                },
                "constraints": {
                    "max_cost": 100.0,
                    "require_organic": True
                },
                "max_results": 5
            }
        }

class FiberRecommendation(BaseModel):
    """Single fiber recommendation."""
    
    fiber_composition: Dict[str, float] = Field(
        ..., 
        description="Fiber blend composition (percentages)"
    )
    predicted_properties: Dict[str, float] = Field(
        ..., 
        description="Predicted material properties"
    )
    match_score: float = Field(
        ..., 
        ge=0.0, 
        le=1.0,
        description="Property match score"
    )
    gots_compliant: bool = Field(
        ..., 
        description="GOTS compliance status"
    )
    processing_method: str = Field(
        ..., 
        description="Recommended processing method"
    )
    
class PredictionResponse(BaseModel):
    """Response model for fiber prediction."""
    
    recommendations: List[FiberRecommendation]
    processing_time: float = Field(..., description="Processing time in seconds")
    model_version: str = Field(..., description="Model version used")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
```

## Async Endpoints
Implement async handlers:

```python
from fastapi import APIRouter, BackgroundTasks
from typing import List
import time

router = APIRouter(prefix="/api/v1", tags=["predictions"])

@router.post(
    "/predict",
    response_model=PredictionResponse,
    status_code=status.HTTP_200_OK,
    summary="Predict fiber replacements",
    description="Predict natural fiber replacements for synthetic polymers"
)
async def predict_fiber_replacement(
    request: FiberPredictionRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    ml_service: MLService = Depends(get_ml_service)
) -> PredictionResponse:
    """Predict natural fiber replacements for target properties."""
    start_time = time.time()
    
    try:
        # Validate request
        await validate_prediction_request(request, db)
        
        # Run prediction
        recommendations = await ml_service.predict(
            target_properties=request.target_properties,
            constraints=request.constraints,
            max_results=request.max_results
        )
        
        # Log prediction in background
        background_tasks.add_task(
            log_prediction,
            user_id=current_user.id,
            request=request,
            recommendations=recommendations
        )
        
        return PredictionResponse(
            recommendations=recommendations,
            processing_time=time.time() - start_time,
            model_version=ml_service.model_version
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Prediction failed"
        )
```

## Error Handling
Implement proper error responses:

```python
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
) -> JSONResponse:
    """Handle validation errors."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": exc.errors(),
            "body": exc.body,
            "type": "validation_error"
        }
    )

@app.exception_handler(ChemistryError)
async def chemistry_exception_handler(
    request: Request,
    exc: ChemistryError
) -> JSONResponse:
    """Handle chemistry-specific errors."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "detail": str(exc),
            "type": "chemistry_error"
        }
    )
```

## Middleware
Add custom middleware:

```python
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import uuid

class RequestIDMiddleware(BaseHTTPMiddleware):
    """Add request ID to all requests."""
    
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        
        return response

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestIDMiddleware)
```

## WebSocket Support
For real-time updates:

```python
from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, Set

class ConnectionManager:
    """Manage WebSocket connections."""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
    
    def disconnect(self, client_id: str):
        self.active_connections.pop(client_id, None)
    
    async def broadcast(self, message: dict):
        for connection in self.active_connections.values():
            await connection.send_json(message)

manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    client_id: str
):
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_json()
            # Process data
            await manager.broadcast({
                "client_id": client_id,
                "data": data
            })
    except WebSocketDisconnect:
        manager.disconnect(client_id)
```