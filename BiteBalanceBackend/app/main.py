from fastapi import FastAPI
from api.images import router as images_router
from db.session import check_db_connection

app = FastAPI()

# Check MongoDB connection on startup
@app.on_event("startup")
async def startup_db_client():
    connection = await check_db_connection()
    if not connection:
        print("Could not connect to MongoDB.")

app.include_router(images_router, prefix="/api")