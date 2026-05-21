from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

router = APIRouter()


class BlogPost(BaseModel):
    id: int
    slug: str
    title: str
    excerpt: str
    content: str
    tag: str
    published_at: datetime


class BlogPostCreate(BaseModel):
    slug: str
    title: str
    excerpt: str
    content: str
    tag: str = "AI/ML"


# ── In-memory store (replace with MongoDB/PostgreSQL for production) ──
_posts: list[BlogPost] = [
    BlogPost(
        id=1,
        slug="building-rag-pipelines-production",
        title="Building RAG pipelines for production: lessons learned",
        excerpt="What I discovered after building a retrieval-augmented generation system that hit 78% directional accuracy in live market analytics.",
        content="Full post content here...",
        tag="RAG",
        published_at=datetime(2025, 4, 10),
    ),
    BlogPost(
        id=2,
        slug="agentic-workflows-langchain",
        title="Agentic workflows with LangChain: a practical guide",
        excerpt="How I structured multi-step AI agents that coordinate tools, memory, and LLM calls — without losing reliability.",
        content="Full post content here...",
        tag="LangChain",
        published_at=datetime(2025, 3, 22),
    ),
    BlogPost(
        id=3,
        slug="fastapi-serverless-aws",
        title="FastAPI on AWS Lambda: serverless Python at 99% uptime",
        excerpt="Deploying a FastAPI app to AWS Lambda + API Gateway, the gotchas I hit, and how I achieved sub-100ms cold starts.",
        content="Full post content here...",
        tag="AWS",
        published_at=datetime(2025, 2, 14),
    ),
]
_next_id = 4


@router.get("", response_model=list[BlogPost])
def list_posts():
    """Return all published blog posts, newest first."""
    return sorted(_posts, key=lambda p: p.published_at, reverse=True)


@router.get("/{slug}", response_model=BlogPost)
def get_post(slug: str):
    """Return a single post by slug."""
    for post in _posts:
        if post.slug == slug:
            return post
    raise HTTPException(status_code=404, detail="Post not found")


@router.post("", response_model=BlogPost, status_code=201)
def create_post(data: BlogPostCreate):
    """Create a new blog post (protect this with an API key in production)."""
    global _next_id
    post = BlogPost(id=_next_id, published_at=datetime.utcnow(), **data.dict())
    _posts.append(post)
    _next_id += 1
    return post
