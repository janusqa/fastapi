# db concerns
from app.db.db import dbconnect, ResultIter
from app.db.db import database_driver

# fastapi concerns
from typing import Optional, List, Union
from fastapi import Response, status, HTTPException

# schemas concerns
import app.api.schemas_pd as schemas_pd


def get_latest_post(user: schemas_pd.UserResponse, response: Response):
    post_found = None
    try:
        with dbconnect() as curr:
            sql = """
                SELECT 
                    *,
                    (
                        SELECT 
                            COUNT(post_id)
                        FROM votes
                        WHERE votes.post_id = posts.post_id
                    ) AS votes                     
                FROM posts 
                INNER JOIN 
                    users ON posts.user_id = users.user_id 
                ORDER BY posts.post_created_at 
                DESC
            """
            curr.execute(sql)
            post_found = next(ResultIter(curr, 1), None)
        if post_found:
            post_found.update(
                {
                    "votes": post_found["votes"],
                    "owner": {
                        "user_id": post_found["user_id"],
                        "email": post_found["email"],
                        "user_created_at": post_found["user_created_at"],
                    },
                }
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Resource does not exist",
            )
    except HTTPException as error:
        response.status_code = error.status_code
        return {"detail": error.detail}
    except (Exception, database_driver.Error) as error:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"detail": str(error)}
    return post_found


def get_post(post_id: int, user: schemas_pd.UserResponse, response: Response):
    post_found = None
    try:
        with dbconnect() as curr:
            sql = """
                SELECT 
                    *,
                    (
                        SELECT 
                            COUNT(post_id)
                        FROM votes
                        WHERE votes.post_id = posts.post_id
                    ) AS votes 
                FROM posts 
                INNER JOIN 
                    users ON posts.user_id = users.user_id 
                WHERE posts.post_id = %s
            """
            query_parameters = (post_id,)
            curr.execute(sql, query_parameters)
            post_found = next(ResultIter(curr, 1), None)
        if post_found:
            post_found.update(
                {
                    "votes": post_found["votes"],
                    "owner": {
                        "user_id": post_found["user_id"],
                        "email": post_found["email"],
                        "user_created_at": post_found["user_created_at"],
                    },
                }
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Resource with id {post_id} does not exist",
            )
    except HTTPException as error:
        response.status_code = error.status_code
        return {"detail": error.detail}
    except (Exception, database_driver.Error) as error:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"detail": str(error)}
    return post_found


def update_post(
    post_id: int,
    post: schemas_pd.Post,
    user: schemas_pd.UserResponse,
    response: Response,
):
    try:
        with dbconnect() as curr:
            sql = """
                UPDATE posts 
                SET 
                    title = %s, 
                    content = %s, 
                    published = %s 
                WHERE 
                    post_id = %s 
                    AND 
                    user_id = %s 
                RETURNING 
                    *,
                    (
                        SELECT 
                            COUNT(post_id)
                        FROM votes
                        WHERE votes.post_id = posts.post_id
                    ) AS votes                      
            """
            query_parameters = (
                post.title,
                post.content,
                post.published,
                post_id,
                user.user_id,
            )
            curr.execute(sql, query_parameters)
            new_post = next(ResultIter(curr, 1), None)
        if new_post:
            new_post.update(
                {
                    "votes": new_post["votes"],
                    "owner": user,
                },
            )
            response.status_code = status.HTTP_201_CREATED
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Resource with ID:{post_id} does not exist for user with ID:{user.user_id}",
            )
    except HTTPException as error:
        response.status_code = error.status_code
        return {"detail": error.detail}
    except (Exception, database_driver.Error) as error:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"detail": str(error)}
    return new_post


def delete_post(post_id: int, user: schemas_pd.UserResponse, response: Response):
    try:
        with dbconnect() as curr:
            sql = """
                DELETE 
                FROM posts 
                WHERE post_id = %s AND user_id = %s 
                RETURNING 
                    *,
                    (
                        SELECT 
                            COUNT(post_id)
                        FROM votes
                        WHERE votes.post_id = posts.post_id
                    ) AS votes                       
            """
            query_parameters = (post_id, user.user_id)
            curr.execute(sql, query_parameters)
            delete_post = next(ResultIter(curr, 1), None)
        if delete_post:
            delete_post.update(
                {
                    "votes": delete_post["votes"],
                    "owner": user,
                },
            )
            response.status_code = status.HTTP_204_NO_CONTENT
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Resource with ID:{post_id} for owner with ID:{user.user_id} does not exist",
            )
    except HTTPException as error:
        response.status_code = error.status_code
        return {"detail": error.detail}
    except (Exception, database_driver.Error) as error:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"detail": str(error)}
    return delete_post


def create_post(
    post: schemas_pd.Post, user: schemas_pd.UserResponse, response: Response
):
    try:
        with dbconnect() as curr:
            sql = """
                INSERT 
                INTO posts (user_id, title, content, published) 
                VALUES (%s, %s, %s, %s) 
                RETURNING *
            """
            query_parameters = (user.user_id, post.title, post.content, post.published)
            curr.execute(sql, query_parameters)
            new_post = next(ResultIter(curr, 1), None)
        if new_post:
            new_post.update(
                {
                    "votes": 0,
                    "owner": user,
                },
            )
            response.status_code = status.HTTP_201_CREATED
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unable to add to resource",
            )
    except HTTPException as error:
        response.status_code = error.status_code
        return {"detail": error.detail}
    except (Exception, database_driver.Error) as error:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"detail": str(error)}
    return new_post


def get_posts(
    response: Response,
    limit: int,
    skip: int,
    search: str,
    user: schemas_pd.UserResponse,
):
    posts = None
    try:
        with dbconnect() as curr:
            query_params = (skip, limit)
            if search:
                query_params = (search, skip, limit)
                sql = """
                    WITH query_index AS (
                        SELECT 
                            post_id
                        FROM posts 
                        INNER JOIN users 
                        ON posts.user_id = users.user_id 
                        WHERE title ~ %s
                        OFFSET %s
                        LIMIT %s
                    )
                    SELECT 
                        *,
                        (
                            SELECT 
                                COUNT(post_id)
                            FROM votes
                            WHERE votes.post_id = posts.post_id
                        ) AS votes 
                    FROM posts
                    INNER JOIN users
                    ON posts.user_id = users.user_id
                    INNER JOIN query_index 
                    USING (post_id);
                """
            else:
                query_params = (skip, limit)
                sql = """
                    WITH query_index AS (
                        SELECT 
                            post_id
                        FROM posts 
                        INNER JOIN users 
                        ON posts.user_id = users.user_id 
                        OFFSET %s
                        LIMIT %s
                    )
                    SELECT 
                        * ,
                        (
                            SELECT 
                                COUNT(post_id)
                            FROM votes
                            WHERE votes.post_id = posts.post_id
                        ) AS votes                         
                    FROM posts
                    INNER JOIN users
                    ON posts.user_id = users.user_id
                    INNER JOIN query_index 
                    USING (post_id);
                """
            curr.execute(sql, query_params)
            posts = list(ResultIter(curr))
        if posts and len(posts) > 0:
            list(
                map(
                    lambda post: post.update(
                        {
                            "votes": post["votes"],
                            "owner": {
                                "user_id": post["user_id"],
                                "email": post["email"],
                                "user_created_at": post["user_created_at"],
                            },
                        }
                    ),
                    posts,
                )
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No post availiable.",
            )
    except HTTPException as error:
        response.status_code = error.status_code
        return {"detail": error.detail}
    except (Exception, database_driver.Error) as error:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"detail": str(error)}
    return posts
