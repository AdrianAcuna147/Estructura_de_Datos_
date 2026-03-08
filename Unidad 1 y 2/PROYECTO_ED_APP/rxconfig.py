import reflex as rx
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

config = rx.Config(
    app_name="PROYECTO_ED_APP",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
    # Usar SQLite por defecto (más simple para desarrollo)
    # Si quieres Supabase, define DATABASE_URL en .env
    db_url=os.getenv("DATABASE_URL", "sqlite:///stakflow.db"),
)