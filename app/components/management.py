import reflex as rx
from app.states.management_state import ManagementState
from app.components.dashboard import status_badge


def filter_pill(status: str) -> rx.Component:
    is_active = ManagementState.filter_status == status
    return rx.el.button(
        status,
        on_click=lambda: ManagementState.set_filter_status(status),
        class_name=rx.cond(
            is_active,
            "px-4 py-1.5 rounded-full text-sm font-semibold bg-cyan-600 text-white shadow-sm",
            "px-4 py-1.5 rounded-full text-sm font-semibold bg-white text-stone-700 border border-stone-200 hover:bg-stone-50",
        ),
    )


def post_card(post: rx.Var[dict]) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                post["content"].to_string()[:150] + "...",
                class_name="text-sm text-stone-700 leading-relaxed",
            ),
            rx.el.div(
                status_badge(post["status"]),
                rx.el.p(
                    f"Published on {post['publication_date']}",
                    class_name="text-xs text-stone-500",
                ),
                class_name="flex justify-between items-center mt-4",
            ),
            class_name="p-4",
        ),
        rx.el.div(
            rx.el.button(
                rx.icon("pencil", class_name="h-4 w-4 mr-2"),
                "Edit",
                class_name="flex-1 flex items-center justify-center p-2 text-sm font-medium text-stone-600 hover:bg-stone-100 hover:text-cyan-700 transition-colors",
            ),
            rx.el.a(
                rx.icon("bar-chart-2", class_name="h-4 w-4 mr-2"),
                "Analytics",
                href="/analytics",
                class_name="flex-1 flex items-center justify-center p-2 text-sm font-medium text-stone-600 hover:bg-stone-100 hover:text-cyan-700 transition-colors border-l border-r",
            ),
            rx.el.button(
                rx.icon("archive", class_name="h-4 w-4 mr-2"),
                "Archive",
                on_click=lambda: ManagementState.archive_post(post["id"]),
                class_name="flex-1 flex items-center justify-center p-2 text-sm font-medium text-red-500 hover:bg-red-50 hover:text-red-700 transition-colors",
            ),
            class_name="flex border-t",
        ),
        class_name="bg-white rounded-xl border border-stone-200 shadow-sm overflow-hidden flex flex-col",
    )


def management_page() -> rx.Component:
    return rx.el.main(
        rx.el.h1("Post Management", class_name="text-3xl font-bold text-stone-800"),
        rx.el.div(
            rx.el.div(
                rx.foreach(["All", "Published", "Draft", "Scheduled"], filter_pill),
                class_name="flex items-center gap-2",
            ),
            rx.el.div(
                rx.icon("search", class_name="h-5 w-5 text-stone-400"),
                rx.el.input(
                    placeholder="Search posts...",
                    on_change=ManagementState.set_search_query,
                    class_name="bg-transparent w-full focus:outline-none text-sm",
                ),
                class_name="flex items-center gap-2 px-4 py-2 bg-white border border-stone-200 rounded-full w-full max-w-xs",
            ),
            class_name="flex justify-between items-center mt-6 mb-6",
        ),
        rx.el.div(
            rx.foreach(ManagementState.filtered_posts, post_card),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
        ),
        class_name="p-6 flex-1",
    )