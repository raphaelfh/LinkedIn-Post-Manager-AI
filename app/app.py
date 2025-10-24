import reflex as rx
import reflex_enterprise as rxe
from app.components.sidebar import sidebar
from app.components.dashboard import dashboard_page
from app.components.create_post import create_post_page
from app.components.management import management_page
from app.components.analytics import analytics_page
from app.states.state import DashboardState
from app.states.create_post_state import CreatePostState
from app.states.management_state import ManagementState
from app.states.analytics_state import AnalyticsState


def index() -> rx.Component:
    return rx.el.div(
        sidebar(),
        dashboard_page(),
        class_name="flex min-h-screen w-full font-['Roboto'] bg-stone-100",
    )


def create_post() -> rx.Component:
    return rx.el.div(
        sidebar(),
        create_post_page(),
        class_name="flex min-h-screen w-full font-['Roboto'] bg-stone-100",
    )


def management() -> rx.Component:
    return rx.el.div(
        sidebar(),
        management_page(),
        class_name="flex min-h-screen w-full font-['Roboto'] bg-stone-100",
    )


def analytics() -> rx.Component:
    return rx.el.div(
        sidebar(),
        analytics_page(),
        class_name="flex min-h-screen w-full font-['Roboto'] bg-stone-100",
    )


def settings() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            rx.el.h1("Settings", class_name="text-3xl font-bold text-stone-800"),
            rx.el.p("Settings page content will go here.", class_name="mt-4"),
            class_name="flex-1 p-6",
        ),
        class_name="flex min-h-screen w-full font-['Roboto'] bg-stone-100",
    )


app = rxe.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700;900&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, on_load=DashboardState.on_load)
app.add_page(create_post, route="/create-post", on_load=CreatePostState.on_load_posts)
app.add_page(management, route="/management", on_load=ManagementState.on_load_posts)
app.add_page(analytics, route="/analytics", on_load=AnalyticsState.on_load_analytics)
app.add_page(settings, route="/settings")