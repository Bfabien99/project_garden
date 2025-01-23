import uvicorn
from fastapi import FastAPI
from database import create_database
from routes import organization, project, fake_route

app = FastAPI(title="Project Garden")


@app.on_event("startup")
def initiate():
    create_database()


app.include_router(organization.router)
app.include_router(project.router)
app.include_router(fake_route.router)

if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=8000)
