import reflex as rx
from PROYECTO_ED_APP.state import ContableState

def crear_boton_menu(icono, texto, ruta_destino):
    es_activo = (ContableState.pestana_actual == ruta_destino)
    
    return rx.button(
        rx.hstack(
            rx.icon(tag=icono, size=18), 
            rx.text(texto),
            spacing="3"
        ),
        on_click=getattr(ContableState, f"ir_{ruta_destino}"),
        # Estilo dinámico de iluminación
        background_color=rx.cond(es_activo, "#30303B", "transparent"),
        color=rx.cond(es_activo, "white", "#A0A0A8"),
        width="100%",
        height="45px",
        border_radius="8px",
        justify_content="start",
        padding_left="1em",
        _hover={"background_color": "#30303B", "color": "white"},
    )

def sidebar():
    return rx.box(
        rx.vstack(
            rx.heading("Menú",
                    color="white",
                    size="7",
                    weight="bold",
                    margin_bottom="1.5em"
                    ),
            crear_boton_menu("layout-dashboard", "Dashboard", "dashboard"),
            crear_boton_menu("calculator", "Sistema Contable", "contable"),
            crear_boton_menu("history", "Historial", "historial"),
            crear_boton_menu("search", "Buscador", "buscador"),
            crear_boton_menu("package", "Inventario", "inventario"),
            spacing="2",
            align="start",
            width="100%",
        ),
        width="250px",
        height="100vh",
        position="fixed",
        left="0",
        top="0",
        padding="1.5em",
        bg="#111116",
        border_right="1px solid #222228",
        z_index="100", # Para que siempre esté arriba
    )