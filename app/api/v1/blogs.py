from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.api.deps import get_db, get_current_user, require_admin
from app.models.blog import Blog
from app.models.user import User
from app.schemas.blog import BlogCreate, BlogUpdate, BlogRead

router = APIRouter(prefix="/blogs", tags=["blogs"])


@router.post("/", response_model=BlogRead, status_code=status.HTTP_201_CREATED)
def create_blog(
    blog_in: BlogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> BlogRead:
    blog = Blog(
        title=blog_in.title,
        content=blog_in.content,
        is_published=blog_in.is_published,
        owner_id=current_user.id,
    )
    db.add(blog)
    db.commit()
    db.refresh(blog)
    return blog


@router.get("/", response_model=List[BlogRead])
def list_blogs(
    db: Session = Depends(get_db),
) -> List[BlogRead]:
    blogs = db.exec(select(Blog)).all()
    return blogs


@router.get("/{blog_id}", response_model=BlogRead)
def get_blog(
    blog_id: int,
    db: Session = Depends(get_db),
) -> BlogRead:
    blog = db.exec(select(Blog).where(Blog.id == blog_id)).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog


@router.put("/{blog_id}", response_model=BlogRead)
def update_blog(
    blog_id: int,
    blog_in: BlogUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> BlogRead:
    blog = db.exec(select(Blog).where(Blog.id == blog_id)).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    if blog.owner_id != current_user.id and current_user.role.name != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to edit this blog",
        )

    update_data = blog_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(blog, field, value)

    db.add(blog)
    db.commit()
    db.refresh(blog)
    return blog


@router.delete("/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(
    blog_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    blog = db.exec(select(Blog).where(Blog.id == blog_id)).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    if blog.owner_id != current_user.id and current_user.role.name != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to delete this blog",
        )
    db.delete(blog)
    db.commit()
    return None

