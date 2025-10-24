import reflex as rx
from typing import Literal
import logging
from sqlalchemy import text
from app.models import Post


class ManagementState(rx.State):
    posts: list[Post] = []
    filter_status: Literal["All", "Published", "Draft", "Scheduled"] = "All"
    search_query: str = ""

    @rx.event
    async def on_load_posts(self):
        if not self.posts:
            await self._fetch_posts()

    async def _fetch_posts(self):
        try:
            async with rx.asession() as session:
                result = await session.execute(
                    text(
                        "SELECT id, content, publication_date, status, likes, comments, engagement_rate, media_urls, created_at FROM posts ORDER BY publication_date DESC"
                    )
                )
                posts_from_db = result.mappings().all()
                posts_list = []
                for p in posts_from_db:
                    post_dict = dict(p)
                    post_dict["publication_date"] = p.publication_date.isoformat()
                    if post_dict.get("media_urls") is None:
                        post_dict["media_urls"] = []
                    posts_list.append(post_dict)
                self.posts = posts_list
        except Exception as e:
            logging.exception(f"Error fetching posts for management: {e}")

    @rx.var
    def filtered_posts(self) -> list[Post]:
        posts_to_filter = self.posts
        if self.filter_status != "All":
            posts_to_filter = [
                p for p in posts_to_filter if p["status"] == self.filter_status
            ]
        if self.search_query:
            posts_to_filter = [
                p
                for p in posts_to_filter
                if self.search_query.lower() in p["content"].lower()
            ]
        return posts_to_filter

    @rx.event
    def set_filter_status(
        self, status: Literal["All", "Published", "Draft", "Scheduled"]
    ):
        self.filter_status = status

    @rx.event
    def set_search_query(self, query: str):
        self.search_query = query

    @rx.event
    async def archive_post(self, post_id: int):
        yield rx.toast.info(f"Post {post_id} archived (simulated).")