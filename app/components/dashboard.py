import reflex as rx
from app.states.state import DashboardState


def kpi_card(
    icon: str, title: str, value: rx.Var[str | int | float], color_class: str
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name="h-6 w-6"),
            class_name=f"p-3 rounded-full bg-opacity-20 {color_class}",
        ),
        rx.el.div(
            rx.el.p(title, class_name="text-sm font-medium text-stone-500"),
            rx.el.p(value, class_name="text-2xl font-bold text-stone-800"),
            class_name="flex flex-col",
        ),
        class_name="flex items-center gap-4 p-4 bg-white rounded-xl border border-stone-200 shadow-sm",
    )


def status_badge(status: rx.Var[str]) -> rx.Component:
    return rx.match(
        status,
        (
            "Published",
            rx.el.div(
                rx.icon("square_check", class_name="h-3 w-3 mr-1.5"),
                "Published",
                class_name="inline-flex items-center rounded-full bg-green-100 px-2.5 py-0.5 text-xs font-semibold text-green-800 w-fit",
            ),
        ),
        (
            "Draft",
            rx.el.div(
                rx.icon("disc_3", class_name="h-3 w-3 mr-1.5"),
                "Draft",
                class_name="inline-flex items-center rounded-full bg-yellow-100 px-2.5 py-0.5 text-xs font-semibold text-yellow-800 w-fit",
            ),
        ),
        (
            "Scheduled",
            rx.el.div(
                rx.icon("clock", class_name="h-3 w-3 mr-1.5"),
                "Scheduled",
                class_name="inline-flex items-center rounded-full bg-blue-100 px-2.5 py-0.5 text-xs font-semibold text-blue-800 w-fit",
            ),
        ),
        rx.el.div(
            "Unknown",
            class_name="inline-flex items-center rounded-full bg-stone-100 px-2.5 py-0.5 text-xs font-semibold text-stone-800 w-fit",
        ),
    )


def sortable_header(title: str, column_name: str) -> rx.Component:
    is_sorting = DashboardState.sort_by == column_name
    return rx.el.th(
        rx.el.button(
            title,
            rx.cond(
                is_sorting,
                rx.icon(
                    rx.cond(
                        DashboardState.sort_ascending,
                        "arrow-up-narrow-wide",
                        "arrow-down-wide-narrow",
                    ),
                    class_name="ml-2 h-4 w-4",
                ),
                rx.icon(
                    "chevrons-up-down",
                    class_name="ml-2 h-4 w-4 opacity-30 group-hover:opacity-100 transition-opacity",
                ),
            ),
            on_click=lambda: DashboardState.set_sort_by(column_name),
            class_name="flex items-center group font-semibold uppercase tracking-wider",
        ),
        class_name="px-6 py-3 text-left text-xs text-stone-500",
    )


def posts_table() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2("Recent Posts", class_name="text-xl font-bold text-stone-800"),
            class_name="px-6 py-4",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        sortable_header("Content", "content"),
                        sortable_header("Date", "publication_date"),
                        sortable_header("Status", "status"),
                        sortable_header("Engagement", "engagement_rate"),
                    )
                ),
                rx.el.tbody(
                    rx.foreach(
                        DashboardState.paginated_posts,
                        lambda post: rx.el.tr(
                            rx.el.td(
                                rx.el.p(
                                    post["content"].to_string()[:50] + "...",
                                    class_name="font-medium text-stone-800 truncate max-w-sm",
                                ),
                                class_name="px-6 py-4",
                            ),
                            rx.el.td(
                                post["publication_date"],
                                class_name="px-6 py-4 text-stone-500",
                            ),
                            rx.el.td(
                                status_badge(post["status"]), class_name="px-6 py-4"
                            ),
                            rx.el.td(
                                rx.el.p(
                                    post["engagement_rate"].to_string() + "%",
                                    class_name=rx.cond(
                                        post["engagement_rate"] > 5,
                                        "font-semibold text-green-600",
                                        "font-medium text-stone-600",
                                    ),
                                ),
                                class_name="px-6 py-4",
                            ),
                            class_name="border-b border-stone-200 hover:bg-stone-50 transition-colors",
                        ),
                    ),
                    class_name="bg-white",
                ),
                class_name="min-w-full",
            ),
            class_name="overflow-x-auto",
        ),
        rx.el.div(
            rx.el.p(
                f"Page {DashboardState.current_page} of {DashboardState.total_pages}",
                class_name="text-sm text-stone-600",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("chevron-left", class_name="h-4 w-4"),
                    "Prev",
                    on_click=DashboardState.prev_page,
                    disabled=DashboardState.current_page <= 1,
                    class_name="flex items-center gap-1 px-3 py-1.5 text-sm font-medium text-stone-700 bg-white border border-stone-300 rounded-md hover:bg-stone-50 disabled:opacity-50 disabled:cursor-not-allowed",
                ),
                rx.el.button(
                    "Next",
                    rx.icon("chevron-right", class_name="h-4 w-4"),
                    on_click=DashboardState.next_page,
                    disabled=DashboardState.current_page >= DashboardState.total_pages,
                    class_name="flex items-center gap-1 px-3 py-1.5 text-sm font-medium text-stone-700 bg-white border border-stone-300 rounded-md hover:bg-stone-50 disabled:opacity-50 disabled:cursor-not-allowed",
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="flex items-center justify-between px-6 py-3 border-t border-stone-200",
        ),
        class_name="bg-white rounded-xl border border-stone-200 shadow-sm overflow-hidden",
    )


def dashboard_page() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            rx.el.h1("Dashboard", class_name="text-3xl font-bold text-stone-800"),
            rx.el.div(
                kpi_card(
                    "file-text",
                    "Total Posts",
                    DashboardState.total_posts,
                    "bg-blue-100 text-blue-600",
                ),
                kpi_card(
                    "thumbs-up",
                    "Total Likes",
                    DashboardState.total_likes,
                    "bg-pink-100 text-pink-600",
                ),
                kpi_card(
                    "message-square",
                    "Total Comments",
                    DashboardState.total_comments,
                    "bg-yellow-100 text-yellow-600",
                ),
                kpi_card(
                    "zap",
                    "Avg. Engagement",
                    DashboardState.avg_engagement.to_string() + "%",
                    "bg-green-100 text-green-600",
                ),
                class_name="grid gap-6 sm:grid-cols-2 lg:grid-cols-4 mt-6",
            ),
            posts_table(),
            class_name="flex flex-col gap-8 p-4 sm:p-6",
        ),
        class_name="flex-1 overflow-y-auto bg-stone-100",
    )