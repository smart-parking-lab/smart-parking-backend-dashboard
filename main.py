from fastapi import FastAPI, Depends
from dotenv import load_dotenv

from src.app.core.cors import setup_cors
from src.app.core.rate_limit import setup_rate_limit
from src.app.core.auth_middleware import JWTAuthMiddleware
from src.app.api.auth import router as auth_router
from src.app.core.dependencies import security

load_dotenv()


def create_app() -> FastAPI:
    
    
    app = FastAPI(
        title="Parking Management System",
        description="API quản lý bãi đỗ xe",
        version="0.1.0",
        dependencies=[Depends(security)]
    )

    setup_cors(app)
    setup_rate_limit(app)
    app.add_middleware(JWTAuthMiddleware)

    app.include_router(auth_router, prefix="/api/v1")

    @app.get("/", tags=["Health"])
    def health_check():
        return {"status": "ok", "message": "Parking Management System is running"}

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
