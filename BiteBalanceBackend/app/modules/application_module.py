from typing import Callable

from fastapi import FastAPI


def mount(app: FastAPI) -> Callable:
    async def start_app() -> None:
        from app.routes import (
            home_page, 
            meal_upload,
            
        )
            
        app.include_router( home_page.router )
        app.include_router( meal_upload.router )
        
    return start_app
