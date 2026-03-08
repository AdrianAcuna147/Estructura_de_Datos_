import reflex as rx

config = rx.Config(
    app_name="PROYECTO_ED_APP",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)