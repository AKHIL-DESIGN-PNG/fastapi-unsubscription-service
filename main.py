import sys
sys.path.append("C:/CodeTru")
from fastapi import FastAPI
from unsubscription_service.routes.unsubscribe import unsubscribe_router
from unsubscription_service.get_subscriptions import router as subscriptions_router
from unsubscription_service.unsubscriptions_view import view_router
from unsubscription_service.search import router as search_router

app = FastAPI()

app.include_router(unsubscribe_router, prefix="/unsubscribe")
app.include_router(view_router, prefix="/view")
app.include_router(subscriptions_router, prefix="/subscriptions")
app.include_router(search_router, prefix="/search")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)