import reflex as rx
from app.states.create_post_state import CreatePostState


def media_preview(url: str) -> rx.Component:
    return rx.el.div(
        rx.el.image(src=url, class_name="w-24 h-24 object-cover rounded-lg"),
        rx.el.button(
            rx.icon("x", class_name="h-4 w-4"),
            on_click=lambda: CreatePostState.remove_media(url),
            class_name="absolute top-1 right-1 bg-black/50 text-white rounded-full p-0.5 hover:bg-black/75",
        ),
        class_name="relative",
    )


def ai_assistant() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("sparkles", class_name="h-6 w-6 text-cyan-600"),
                rx.el.h2("AI Assistant", class_name="text-lg font-bold"),
                class_name="flex items-center gap-2",
            ),
            rx.el.button(
                rx.icon("x", class_name="h-5 w-5"),
                on_click=CreatePostState.toggle_ai_assistant,
                class_name="p-1 rounded-full hover:bg-stone-200",
            ),
            class_name="flex items-center justify-between p-4 border-b",
        ),
        rx.el.div(
            rx.foreach(
                CreatePostState.chat_history,
                lambda message: rx.el.div(
                    rx.el.p(message["content"]),
                    class_name=rx.cond(
                        message["role"] == "user",
                        "bg-blue-100 text-blue-900 p-3 rounded-lg self-end",
                        "bg-stone-100 text-stone-900 p-3 rounded-lg self-start",
                    ),
                ),
            ),
            class_name="flex-1 p-4 space-y-4 overflow-y-auto",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.input(
                    placeholder="Your prompt...",
                    on_change=CreatePostState.set_ai_prompt,
                    class_name="flex-1 bg-transparent focus:outline-none",
                    default_value=CreatePostState.ai_prompt,
                ),
                rx.el.button(
                    rx.icon("arrow-up", class_name="h-5 w-5"),
                    on_click=CreatePostState.process_ai_prompt,
                    disabled=CreatePostState.ai_processing
                    | (CreatePostState.ai_prompt.length() == 0),
                    class_name="p-2 rounded-full bg-cyan-600 text-white disabled:bg-cyan-300",
                ),
                class_name="flex items-center p-2 border rounded-full",
            ),
            rx.cond(
                CreatePostState.ai_response != "",
                rx.el.button(
                    "Use This Content",
                    on_click=CreatePostState.use_ai_content,
                    class_name="w-full mt-2 py-2 px-4 bg-green-600 text-white font-semibold rounded-lg hover:bg-green-700",
                ),
                None,
            ),
            class_name="p-4 border-t",
        ),
        class_name="flex flex-col h-full bg-white border-l",
    )


def create_post_page() -> rx.Component:
    return rx.el.div(
        rx.el.main(
            rx.el.h1("Create a Post", class_name="text-3xl font-bold text-stone-800"),
            rx.el.div(
                rx.el.textarea(
                    default_value=CreatePostState.post_content,
                    on_change=CreatePostState.set_post_content,
                    placeholder="What do you want to talk about?",
                    max_length=3000,
                    class_name="w-full h-48 p-4 border rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-cyan-500",
                ),
                rx.el.div(
                    rx.el.p(
                        f"{CreatePostState.character_count} / 3000",
                        class_name=rx.cond(
                            CreatePostState.character_count > 3000,
                            "text-red-500",
                            "text-stone-500",
                        ),
                    ),
                    class_name="text-right text-sm mt-1",
                ),
                class_name="bg-white p-6 rounded-xl border border-stone-200 shadow-sm",
            ),
            rx.el.div(
                rx.upload.root(
                    rx.el.div(
                        rx.icon("cloud_upload", class_name="h-10 w-10 text-stone-400"),
                        rx.el.p(
                            rx.el.strong("Click to upload", class_name="text-cyan-600"),
                            " or drag and drop",
                        ),
                        rx.el.p(
                            "PNG, JPG, GIF up to 50MB",
                            class_name="text-xs text-stone-500",
                        ),
                        class_name="flex flex-col items-center justify-center gap-1 p-6 border-2 border-dashed border-stone-300 rounded-lg text-center",
                    ),
                    id="media_upload",
                    accept={
                        "image/png": [".png"],
                        "image/jpeg": [".jpg", ".jpeg"],
                        "image/gif": [".gif"],
                        "video/mp4": [".mp4"],
                    },
                    max_size=52428800,
                    multiple=True,
                    on_drop=CreatePostState.handle_upload(
                        rx.upload_files(upload_id="media_upload")
                    ),
                    class_name="w-full cursor-pointer",
                ),
                rx.cond(
                    rx.selected_files("media_upload").length() > 0,
                    rx.el.div(
                        rx.foreach(
                            rx.selected_files("media_upload"),
                            lambda file: rx.el.div(
                                file, class_name="text-sm p-2 bg-stone-100 rounded"
                            ),
                        ),
                        rx.el.div(
                            rx.el.button(
                                "Clear",
                                on_click=rx.clear_selected_files("media_upload"),
                                class_name="text-sm text-cyan-600 hover:underline",
                            ),
                            rx.el.button(
                                "Upload",
                                on_click=CreatePostState.handle_upload(
                                    rx.upload_files(upload_id="media_upload")
                                ),
                                class_name="px-4 py-1.5 bg-cyan-600 text-white rounded-md text-sm font-semibold",
                            ),
                            class_name="flex items-center gap-4 mt-2",
                        ),
                        class_name="mt-4 space-y-2",
                    ),
                    None,
                ),
                rx.cond(
                    CreatePostState.uploaded_media_urls.length() > 0,
                    rx.el.div(
                        rx.foreach(CreatePostState.uploaded_media_urls, media_preview),
                        class_name="flex flex-wrap gap-4 mt-4",
                    ),
                    None,
                ),
                class_name="bg-white p-6 rounded-xl border border-stone-200 shadow-sm mt-6",
            ),
            rx.el.div(
                rx.el.button(
                    "Save Draft",
                    on_click=CreatePostState.save_draft,
                    class_name="px-6 py-2 border border-stone-300 rounded-lg font-semibold hover:bg-stone-100",
                ),
                rx.el.div(
                    rx.el.input(type="date", class_name="border rounded-lg px-3 py-2"),
                    rx.el.input(type="time", class_name="border rounded-lg px-3 py-2"),
                    rx.el.button(
                        "Schedule",
                        class_name="px-6 py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700",
                    ),
                    class_name="flex items-center gap-2",
                ),
                rx.el.button(
                    "Publish",
                    on_click=CreatePostState.publish_post,
                    class_name="px-6 py-2 bg-cyan-600 text-white rounded-lg font-semibold hover:bg-cyan-700",
                ),
                class_name="flex justify-between items-center mt-6",
            ),
            class_name="p-6 space-y-6 flex-1",
        ),
        rx.el.aside(
            rx.cond(
                CreatePostState.ai_assistant_open,
                ai_assistant(),
                rx.el.button(
                    rx.icon("sparkles", class_name="h-6 w-6"),
                    on_click=CreatePostState.toggle_ai_assistant,
                    class_name="m-4 p-3 bg-white rounded-full shadow-lg hover:bg-stone-100",
                ),
            ),
            class_name=rx.cond(
                CreatePostState.ai_assistant_open,
                "w-full md:w-96 transition-all duration-300 ease-in-out",
                "w-auto transition-all duration-300 ease-in-out",
            ),
        ),
        class_name="flex flex-1",
    )