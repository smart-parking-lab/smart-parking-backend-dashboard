from fastapi import FastAPI, Depends
from dotenv import load_dotenv

from app.core.cors import setup_cors
from app.core.rate_limit import setup_rate_limit
from app.core.auth_middleware import JWTAuthMiddleware
from app.api.auth import router as auth_router
from app.api.vehicle import router as vehicle_router
from app.api.admin import router as admin_router
from app.api.pricing_rules import router as pricing_rules_router
from app.api.parking_sessions import router as parking_sessions_router
from app.api.invoices import router as invoices_router
from app.api.parking_slots import router as parking_slots_router
from app.core.dependencies import security

load_dotenv()


def create_app() -> FastAPI:
    app = FastAPI(
        title="Parking Management System",
        description="API quản lý bãi đỗ xe",
        version="0.1.0",
        dependencies=[Depends(security)]
    )

    print("\n" + "="*50)
    print("🚀 Server is running!")
    print(f"👉 Application:  http://127.0.0.1:9000")
    print(f"📚 Swagger UI:   http://127.0.0.1:9000/docs")
    print("="*50 + "\n")

    setup_cors(app)
    setup_rate_limit(app)
    app.add_middleware(JWTAuthMiddleware)

    app.include_router(auth_router, prefix="/api/v1")
    app.include_router(vehicle_router, prefix="/api/v1")
    app.include_router(admin_router, prefix="/api/v1")
    app.include_router(pricing_rules_router, prefix="/api/v1")
    app.include_router(parking_sessions_router, prefix="/api/v1")
    app.include_router(invoices_router, prefix="/api/v1")
    app.include_router(parking_slots_router, prefix="/api/v1")

    @app.get("/", tags=["Health"])
    def health_check():
        return {"status": "ok", "message": "Parking Management System is running"}

    return app


app = create_app()
