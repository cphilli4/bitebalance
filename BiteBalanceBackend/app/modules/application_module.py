from typing import Callable

from fastapi import FastAPI


def mount(app: FastAPI) -> Callable:
    async def start_app() -> None:
        from app.routes import (
            home_page, 
            meal_upload,
            meal_by_date,
            
        )
            
        app.include_router( home_page.router )
        app.include_router( meal_upload.router )
        app.include_router( meal_by_date.router )
        
    return start_app
