from typing import Callable

from fastapi import FastAPI


def mount(app: FastAPI) -> Callable:
    async def start_app() -> None:
        from app.routes import (
            home_page, 
            
        )
            
        app.include_router( home_page.router )
    
        
    return start_app
