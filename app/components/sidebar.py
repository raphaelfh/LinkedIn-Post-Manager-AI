import reflex as rx
from app.states.state import DashboardState


def nav_item(item: dict) -> rx.Component:
    is_active = item["label"].lower() == DashboardState.active_page.lower()
    return rx.el.a(
        rx.icon(
            item["icon"],
            class_name=rx.cond(
                is_active,
                "h-5 w-5 text-white",
                "h-5 w-5 text-stone-500 group-hover:text-cyan-600 transition-colors",
            ),
        ),
        rx.el.span(
            item["label"],
            class_name=rx.cond(
                is_active,
                "font-semibold text-white",
                "font-medium text-stone-700 group-hover:text-cyan-700 transition-colors",
            ),
        ),
        href=item["href"],
        class_name=rx.cond(
            is_active,
            "flex items-center gap-3 rounded-lg bg-cyan-600 px-3 py-2 transition-all shadow-md",
            "flex items-center gap-3 rounded-lg px-3 py-2 text-stone-900 transition-all hover:bg-stone-100 group",
        ),
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.a(
                rx.icon("linkedin", class_name="h-8 w-8 text-cyan-700"),
                rx.el.span(
                    "Post Manager", class_name="text-xl font-bold text-stone-800"
                ),
                href="/",
                class_name="flex items-center gap-2",
            ),
            class_name="flex h-16 items-center border-b border-stone-200 px-6 shrink-0",
        ),
        rx.el.div(
            rx.el.nav(
                rx.foreach(DashboardState.nav_items, nav_item),
                class_name="flex flex-col gap-1 p-4",
            ),
            rx.el.div(
                rx.match(
                    DashboardState.db_connection_status,
                    (
                        "connected",
                        rx.el.div(
                            rx.icon(
                                "circle_check", class_name="h-4 w-4 text-green-500"
                            ),
                            rx.el.span(
                                "DB Connected",
                                class_name="text-xs font-medium text-stone-500",
                            ),
                            class_name="flex items-center gap-2",
                        ),
                    ),
                    (
                        "connecting",
                        rx.el.div(
                            rx.spinner(class_name="h-4 w-4 text-orange-500"),
                            rx.el.span(
                                "Connecting...",
                                class_name="text-xs font-medium text-stone-500",
                            ),
                            class_name="flex items-center gap-2",
                        ),
                    ),
                    (
                        "error",
                        rx.el.div(
                            rx.icon("circle_x", class_name="h-4 w-4 text-red-500"),
                            rx.el.span(
                                "DB Offline",
                                class_name="text-xs font-medium text-stone-500",
                            ),
                            class_name="flex items-center gap-2",
                        ),
                    ),
                ),
                class_name="mt-auto p-4 border-t border-stone-200",
            ),
            class_name="flex flex-col h-full",
        ),
        class_name="hidden md:flex flex-col border-r bg-stone-50/50 w-64",
    )