from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import blog, contact

app = FastAPI(
    title="Vikas Madgula Portfolio API",
    description="Backend for vikasmadgula.dev — blog posts and contact form.",
    version="1.0.0",
)

# Allow requests from GitHub Pages frontend + localhost dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://<your-github-username>.github.io",  # ← replace with yours
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(blog.router, prefix="/blog", tags=["Blog"])
app.include_router(contact.router, prefix="/contact", tags=["Contact"])


@app.get("/")
def root():
    return {"status": "ok", "message": "Vikas Madgula Portfolio API"}


@app.get("/health")
def health():
    return {"status": "healthy"}
