import reflex as rx
from typing import TypedDict, Literal
import asyncio
import datetime
import logging
import uuid
from app.supabase_client import db
from app.models import Post
from sqlalchemy import text


class ChatMessage(TypedDict):
    role: Literal["user", "assistant"]
    content: str


class CreatePostState(rx.State):
    post_content: str = ""
    uploaded_media_urls: list[str] = []
    ai_assistant_open: bool = False
    ai_prompt: str = ""
    ai_response: str = ""
    ai_processing: bool = False
    chat_history: list[ChatMessage] = []

    @rx.event
    def set_post_content(self, content: str):
        self.post_content = content

    @rx.event
    def set_ai_prompt(self, prompt: str):
        self.ai_prompt = prompt

    @rx.event
    def on_load_posts(self):
        return

    @rx.var
    def character_count(self) -> int:
        return len(self.post_content)

    @rx.event
    async def handle_upload(self, files: list[rx.UploadFile]):
        if db is None:
            yield rx.toast.error("Storage not configured. Cannot upload files.")
            return
        for file in files:
            upload_data = await file.read()
            file_extension = file.name.split(".")[-1]
            file_name = f"{uuid.uuid4()}.{file_extension}"
            try:
                db.storage.from_("media").upload(
                    file=upload_data,
                    path=file_name,
                    file_options={"content-type": file.content_type},
                )
                public_url = db.storage.from_("media").get_public_url(file_name)
                self.uploaded_media_urls.append(public_url)
            except Exception as e:
                logging.exception(f"Failed to upload {file.name}: {e}")
                yield rx.toast.error(f"Failed to upload {file.name}.")
        yield rx.clear_selected_files("media_upload")

    @rx.event
    def remove_media(self, url: str):
        self.uploaded_media_urls.remove(url)
        if db is not None:
            try:
                file_name = url.split("/")[-1]
                db.storage.from_("media").remove([file_name])
            except Exception as e:
                logging.exception(f"Failed to remove file from storage: {e}")

    @rx.event
    def toggle_ai_assistant(self):
        self.ai_assistant_open = not self.ai_assistant_open

    @rx.event
    async def process_ai_prompt(self):
        if not self.ai_prompt.strip():
            return
        self.ai_processing = True
        self.ai_response = ""
        self.chat_history.append({"role": "user", "content": self.ai_prompt})
        user_prompt = self.ai_prompt
        self.ai_prompt = ""
        yield
        await asyncio.sleep(1.5)
        response_text = f"This is an AI-generated response for: '{user_prompt}'. It could be a more detailed and professional post about this topic, ready for LinkedIn."
        self.ai_response = response_text
        self.chat_history.append({"role": "assistant", "content": response_text})
        self.ai_processing = False

    @rx.event
    def use_ai_content(self):
        self.post_content = self.ai_response
        self.ai_response = ""
        self.ai_assistant_open = False
        return rx.toast.success("AI content inserted!")

    async def _create_post_in_db(self, status: Literal["Draft", "Published"]):
        if not self.post_content.strip():
            yield rx.toast.error("Post content cannot be empty.")
            return
        try:
            async with rx.asession() as session:
                await session.execute(
                    text("""
                        INSERT INTO posts (content, publication_date, status, media_urls)
                        VALUES (:content, :publication_date, :status, :media_urls)
                    """),
                    {
                        "content": self.post_content,
                        "publication_date": datetime.date.today(),
                        "status": status,
                        "media_urls": list(self.uploaded_media_urls),
                    },
                )
                await session.commit()
            self.post_content = ""
            self.uploaded_media_urls = []
            message = f"Post successfully saved as {status.lower()}!"
            toast_method = rx.toast.info if status == "Draft" else rx.toast.success
            yield toast_method(message)
            yield rx.redirect("/")
        except Exception as e:
            logging.exception(f"Database Error on post creation: {e}")
            yield rx.toast.error(
                f"Failed to save post. Please check connection and try again."
            )

    @rx.event
    async def save_draft(self):
        async for event in self._create_post_in_db(status="Draft"):
            yield event

    @rx.event
    async def publish_post(self):
        async for event in self._create_post_in_db(status="Published"):
            yield event