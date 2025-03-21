from fastapi import FastAPI

from api.activity import router as activity_router
from api.building import router as building_router
from api.organization import router as organization_router

app = FastAPI()

app.include_router(organization_router, prefix="/api", tags=["Organization"])
app.include_router(building_router, prefix="/api", tags=["Building"])
app.include_router(activity_router, prefix="/api", tags=["Activity"])


@app.get("/")
def read_root() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}
