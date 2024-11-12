from typing import Callable

from fastapi import FastAPI


def mount(app: FastAPI) -> Callable:
    async def start_app() -> None:
        from app.routes import (
            home_page, 
            meals,
            
        )
            
        app.include_router( home_page.router )
        app.include_router( meals.router )
        
        
    return start_app
