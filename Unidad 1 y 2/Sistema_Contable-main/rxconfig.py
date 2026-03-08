import reflex as rx

config = rx.Config(
    app_name="PROYECTO_ED_APP",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
    db_url="postgresql://postgres.huzlrdruzspfdbclgzhk:proyecto_123@aws-1-us-east-1.pooler.supabase.com:6543/postgres",
)