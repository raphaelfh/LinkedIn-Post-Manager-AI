import reflex as rx
import random
import datetime
from app.models import Post
from typing import TypedDict
import logging
from sqlalchemy import text


class DailyInteraction(TypedDict):
    date: str
    interactions: int


class AnalyticsState(rx.State):
    posts: list[Post] = []
    selected_post_id: str = ""
    trend_data: list[DailyInteraction] = []

    @rx.event
    async def on_load_analytics(self):
        if not self.posts:
            await self._fetch_posts()

    async def _fetch_posts(self):
        try:
            async with rx.asession() as session:
                result = await session.execute(
                    text(
                        "SELECT id, content, publication_date, status, likes, comments, engagement_rate, media_urls, created_at FROM posts WHERE status = 'Published' ORDER BY publication_date DESC"
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
                if self.posts and (not self.selected_post_id):
                    self.selected_post_id = str(self.posts[0]["id"])
                    self._generate_trend_data()
        except Exception as e:
            logging.exception(f"Error fetching posts for analytics: {e}")

    @rx.var
    def selected_post(self) -> Post | None:
        if not self.selected_post_id:
            return None
        for p in self.posts:
            if str(p["id"]) == self.selected_post_id:
                return p
        return None

    @rx.var
    def top_posts(self) -> list[Post]:
        return sorted(
            [p for p in self.posts if p["status"] == "Published"],
            key=lambda p: p["engagement_rate"],
            reverse=True,
        )[:3]

    def _generate_trend_data(self):
        self.trend_data = []
        for i in range(7):
            date = datetime.date.today() - datetime.timedelta(days=6 - i)
            self.trend_data.append(
                {"date": date.strftime("%b %d"), "interactions": random.randint(5, 50)}
            )

    @rx.event
    def select_post(self, post_id: str):
        self.selected_post_id = post_id
        self._generate_trend_data()