from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers import interval

from app.routes import router as users_router
from app.scheduler import deactivate_inactive_users
from app.settings import Settings

APP_NAME = "Users"

scheduler = BackgroundScheduler()

scheduler.add_job(
    func=deactivate_inactive_users,
    trigger=interval.IntervalTrigger(seconds=60 * 60 * 24),
)


def lifespan(_: FastAPI):
    from app.database import create_all

    Settings()  # Check if our settings are valid
    create_all()  # Create the database tables
    scheduler.start()

    yield

    # Clean up after the app is done


app = FastAPI(
    title=APP_NAME,
    lifespan=lifespan,
    debug=True,  # remove this in production
)

app.include_router(users_router)


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")  # Redirect to the docs


@app.get(
    "/health", include_in_schema=False
)  # This route is not documented and used for health checks of the service
def health():
    return {"status": "ok"}
