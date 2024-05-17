from fastapi import FastAPI


def create_app_routers(app: FastAPI):
    """Includes all nested routers into base."""
    # app.include_router(user.router)
    # app.include_router(project.router)
    return app
