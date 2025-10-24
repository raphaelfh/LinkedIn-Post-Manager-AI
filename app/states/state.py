import reflex as rx
from typing import Literal
import datetime
import random
import logging
from sqlalchemy import text
from app.models import Post


class DashboardState(rx.State):
    nav_items: list[dict[str, str]] = [
        {"label": "Dashboard", "icon": "layout-dashboard", "href": "/"},
        {"label": "Create Post", "icon": "file-plus-2", "href": "/create-post"},
        {"label": "Management", "icon": "folder-kanban", "href": "/management"},
        {"label": "Analytics", "icon": "bar-chart-3", "href": "/analytics"},
        {"label": "Settings", "icon": "settings", "href": "/settings"},
    ]
    db_connection_status: Literal["connected", "connecting", "error"] = "connecting"

    @rx.var
    def active_page(self) -> str:
        return self.router.page.path.replace("/", "").capitalize() or "Dashboard"

    posts: list[Post] = []
    current_page: int = 1
    items_per_page: int = 5
    sort_by: str = "publication_date"
    sort_ascending: bool = False

    @rx.event
    async def on_load(self):
        if not self.posts:
            await self._fetch_posts()

    async def _fetch_posts(self):
        self.db_connection_status = "connecting"
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
                self.db_connection_status = "connected"
                if not self.posts:
                    await self._generate_dummy_posts(local_only=False)
        except Exception as e:
            self.db_connection_status = "error"
            logging.exception(f"Error fetching from DB: {e}")
            await self._generate_dummy_posts(local_only=True)

    async def _generate_dummy_posts(self, local_only: bool = True):
        statuses: list[Literal["Published", "Draft", "Scheduled"]] = [
            "Published",
            "Draft",
            "Scheduled",
        ]
        dummy_posts = []
        for i in range(20):
            pub_date = datetime.date.today() - datetime.timedelta(
                days=random.randint(0, 30)
            )
            post_dict = {
                "id": i + 1,
                "content": f"This is a sample LinkedIn post number {i + 1}. Let's discuss the future of AI in modern web development. #AI #WebDev #Reflex",
                "publication_date": pub_date.isoformat(),
                "status": random.choice(statuses),
                "likes": random.randint(5, 500),
                "comments": random.randint(0, 100),
                "engagement_rate": round(random.uniform(0.5, 15.0), 2),
                "media_urls": [],
                "created_at": datetime.datetime.now().isoformat(),
            }
            dummy_posts.append(post_dict)
        async with self:
            self.posts = dummy_posts
        if not local_only:
            try:
                async with rx.asession() as session:
                    for post_data in dummy_posts:
                        await session.execute(
                            text("""INSERT INTO posts (id, content, publication_date, status, likes, comments, engagement_rate, media_urls)
                                     VALUES (:id, :content, :publication_date, :status, :likes, :comments, :engagement_rate, :media_urls)
                                     ON CONFLICT (id) DO NOTHING;"""),
                            post_data,
                        )
                    await session.commit()
            except Exception as e:
                logging.exception(f"Could not save dummy posts to DB: {e}")

    @rx.var
    def total_posts(self) -> int:
        return len(self.posts)

    @rx.var
    def total_likes(self) -> int:
        return sum(
            (post["likes"] for post in self.posts if post["status"] == "Published")
        )

    @rx.var
    def total_comments(self) -> int:
        return sum(
            (post["comments"] for post in self.posts if post["status"] == "Published")
        )

    @rx.var
    def avg_engagement(self) -> float:
        published_posts = [p for p in self.posts if p["status"] == "Published"]
        if not published_posts:
            return 0.0
        total_engagement = sum((p["engagement_rate"] for p in published_posts))
        return round(total_engagement / len(published_posts), 2)

    @rx.var
    def sorted_posts(self) -> list[Post]:
        return sorted(
            self.posts, key=lambda p: p[self.sort_by], reverse=not self.sort_ascending
        )

    @rx.var
    def paginated_posts(self) -> list[Post]:
        start = (self.current_page - 1) * self.items_per_page
        end = start + self.items_per_page
        return self.sorted_posts[start:end]

    @rx.var
    def total_pages(self) -> int:
        return -(-len(self.posts) // self.items_per_page)

    @rx.event
    def set_page(self, page_num: int):
        self.current_page = max(1, min(page_num, self.total_pages))

    @rx.event
    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1

    @rx.event
    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1

    @rx.event
    def set_sort_by(self, column: str):
        if self.sort_by == column:
            self.sort_ascending = not self.sort_ascending
        else:
            self.sort_by = column
            self.sort_ascending = True
        self.current_page = 1