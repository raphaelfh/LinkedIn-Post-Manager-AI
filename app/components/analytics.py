import reflex as rx
from app.states.analytics_state import AnalyticsState


def analytics_kpi_card(
    icon: str, title: str, value: rx.Var, color: str
) -> rx.Component:
    return rx.el.div(
        rx.icon(icon, class_name=f"h-6 w-6 {color}"),
        rx.el.p(title, class_name="text-sm font-medium text-stone-500"),
        rx.el.p(value, class_name="text-3xl font-bold text-stone-800"),
        class_name="flex flex-col items-start gap-1 p-4 bg-white rounded-xl border shadow-sm",
    )


def trend_chart() -> rx.Component:
    return rx.el.div(
        rx.el.h3("7-Day Interaction Trend", class_name="font-semibold mb-4"),
        rx.el.div(
            rx.foreach(
                AnalyticsState.trend_data,
                lambda item: rx.el.div(
                    rx.el.div(
                        rx.el.div(class_name="w-full h-full bg-cyan-500 rounded-t-md"),
                        style={"height": item["interactions"].to_string() + "%"},
                        class_name="w-full h-full flex flex-col justify-end",
                    ),
                    rx.el.p(
                        item["date"],
                        class_name="text-xs text-stone-500 mt-1 text-center",
                    ),
                    class_name="flex-1 flex flex-col items-center justify-end",
                ),
            ),
            class_name="flex items-end h-48 gap-4 px-4 pt-4 bg-stone-50/50 rounded-lg border",
        ),
        class_name="bg-white p-6 rounded-xl border shadow-sm",
    )


def top_post_card(post: rx.Var[dict], rank: int) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(f"#{rank}", class_name="font-bold text-lg text-cyan-600"),
            rx.el.p(
                post["content"].to_string()[:60] + "...",
                class_name="text-sm font-medium text-stone-800 truncate",
            ),
            class_name="flex items-center gap-4",
        ),
        rx.el.div(
            rx.el.p(
                post["engagement_rate"].to_string() + "%",
                class_name="font-bold text-lg",
            ),
            rx.el.p("Engagement", class_name="text-xs text-stone-500"),
            class_name="text-right",
        ),
        class_name="flex items-center justify-between p-3 bg-white rounded-lg border hover:bg-stone-50",
    )


def analytics_page() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            rx.el.h1("Post Analytics", class_name="text-3xl font-bold text-stone-800"),
            rx.el.select(
                rx.foreach(
                    AnalyticsState.posts,
                    lambda post: rx.el.option(
                        post["content"].to_string()[:50] + "...",
                        value=post["id"].to_string(),
                    ),
                ),
                on_change=AnalyticsState.select_post,
                value=AnalyticsState.selected_post_id,
                class_name="mt-4 w-full max-w-md p-2 border rounded-lg bg-white shadow-sm",
            ),
            class_name="mb-6",
        ),
        rx.cond(
            AnalyticsState.selected_post,
            rx.el.div(
                rx.el.div(
                    analytics_kpi_card(
                        "thumbs-up",
                        "Likes",
                        AnalyticsState.selected_post["likes"],
                        "text-pink-500",
                    ),
                    analytics_kpi_card(
                        "message-circle",
                        "Comments",
                        AnalyticsState.selected_post["comments"],
                        "text-yellow-500",
                    ),
                    analytics_kpi_card(
                        "zap",
                        "Engagement",
                        AnalyticsState.selected_post["engagement_rate"].to_string()
                        + "%",
                        "text-green-500",
                    ),
                    analytics_kpi_card(
                        "eye", "Reach (Simulated)", "12.3k", "text-blue-500"
                    ),
                    class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6",
                ),
                rx.el.div(
                    trend_chart(),
                    rx.el.div(
                        rx.el.h3(
                            "Top 3 Posts by Engagement", class_name="font-semibold mb-4"
                        ),
                        rx.el.div(
                            rx.foreach(
                                AnalyticsState.top_posts,
                                lambda post, i: top_post_card(post, i + 1),
                            ),
                            class_name="space-y-3",
                        ),
                        class_name="bg-white p-6 rounded-xl border shadow-sm",
                    ),
                    class_name="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-6",
                ),
                class_name="w-full",
            ),
            rx.el.div(
                rx.el.p(
                    "No post selected or data available.", class_name="text-stone-500"
                ),
                class_name="flex items-center justify-center h-64 bg-white rounded-xl border",
            ),
        ),
        class_name="p-6 flex-1",
    )