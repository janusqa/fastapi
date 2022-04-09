table_users = """
CREATE TABLE IF NOT EXISTS public.users
(
    user_id SERIAL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    user_created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    CONSTRAINT users_pkey PRIMARY KEY (user_id)
);
"""

table_posts = """
CREATE TABLE IF NOT EXISTS public.posts
(
    post_id SERIAL,
    user_id INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    published BOOLEAN NOT NULL DEFAULT true,
    post_created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    CONSTRAINT posts_pkey PRIMARY KEY (post_id),
    CONSTRAINT posts_users_fkey FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
);
"""

table_votes = """
CREATE TABLE IF NOT EXISTS public.votes
(
    post_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    vote_created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    CONSTRAINT votes_pkey PRIMARY KEY (post_id, user_id),
    CONSTRAINT votes_users_fkey FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
    CONSTRAINT votes_posts_fkey FOREIGN KEY (post_id) REFERENCES posts (post_id) ON DELETE CASCADE
);
"""
