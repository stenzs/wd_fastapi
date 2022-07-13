from sqlalchemy.orm import Session
from app.schemas import favorites as favorite_schema, post as post_schema
from app.db.db_models import Favorites, Post


def create_favorites(db: Session, favorite: favorite_schema.CreateFavorite):
    check = db.query(Favorites).where(Favorites.userId == favorite.userId, Favorites.objId == favorite.objId).all()
    if check:
        return False
    db_favorite = Favorites(userId=favorite.userId, objId=favorite.objId)
    db.add(db_favorite)
    db.commit()
    db.refresh(db_favorite)
    return db_favorite


def read_favorites(user_id: int, db: Session, page: int = 1, page_limit: int = 60):
    offset = (page - 1) * page_limit
    query = db.query(Post).where(Favorites.userId == user_id, Post.id == Favorites.objId)
    posts = query.offset(offset).limit(page_limit).all()
    return posts


def delete_favorites(db: Session, user_id: int, obj_id: int):
    delete = db.query(Favorites).where(Favorites.userId == user_id,
                                       Favorites.objId == obj_id).delete(synchronize_session="evaluate")
    db.commit()
    return delete


def get_favorites_posts_page_by_page(db: Session,
                                     page: int = 1,
                                     page_limit: int = 60):
    offset = (page - 1) * page_limit
    query = db.query(Post)

    posts = query.offset(offset).limit(page_limit).all()

    return post_schema.Posts(posts=posts)