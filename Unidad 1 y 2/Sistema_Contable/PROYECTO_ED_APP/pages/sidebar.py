import reflex as rx
from ..state import ContableState # <--- El backend

# ================================
# SIDEBAR
# Es la barrita vertical que aparece en el lado izquido
# ================================
def sidebar():

    # Estilo común para todos los botones
    estilo_botones = {
        "width": "200px",
        "height": "45px",
        "bg": "#1A1A21",
        "color": "white",
        "border_radius": "8px",
        "_hover": {
            "background_color": "#30303B"
        }
    }

    return rx.box(
        rx.vstack(
            rx.heading("Menú"),

            #Agrega los botones que se ven en el lado izquierdo
            rx.button("Dashboard", on_click=ContableState.ir_dashboard, **estilo_botones),
            rx.button("Sistema contable", on_click=ContableState.ir_contable, **estilo_botones),
            rx.button("Historial registros", on_click=ContableState.ir_historial, **estilo_botones),
            rx.button("Buscador", on_click=ContableState.ir_buscador, **estilo_botones),
            rx.button("Inventario", on_click=ContableState.ir_inventario, **estilo_botones),

            align="start",
            height="100%",
        ),
        width="220px",
        min_height="100vh",
        padding="1em",
        border_right="1px solid gray",
        bg="#1A1A21",
    )