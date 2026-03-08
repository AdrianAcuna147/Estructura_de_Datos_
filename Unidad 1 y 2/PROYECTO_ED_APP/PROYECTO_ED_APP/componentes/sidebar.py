# sidebar.py
import reflex as rx
from PROYECTO_ED_APP.state import ContableState

# Crea los botones y su estilo de la barra de la izquierda
def crear_boton_menu(icono, texto, ruta_destino):
    # Se inicializa el botón para saber si está activo
    es_activo = (ContableState.pestana_actual == ruta_destino)
    
    return rx.button(
        rx.hstack(
            rx.icon(tag=icono, size=18),
            rx.text(texto),
            spacing="3"
        ),
        # Redirige a la pestaña adecuada usando la función dinámica ir_
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

# Barra lateral de la izquierda de la aplicación
def sidebar():
    return rx.box(
        rx.vstack(
            # --- LOGO / TÍTULO ---
            rx.heading("Menú",
                    color="white",
                    size="7",
                    weight="bold",
                    margin_bottom="1.5em"
                    ),
            
            # --- BOTONES DE NAVEGACIÓN ---
            crear_boton_menu("layout-dashboard", "Dashboard", "dashboard"),
            crear_boton_menu("calculator", "Sistema Contable", "contable"),
            crear_boton_menu("history", "Historial", "historial"),
            crear_boton_menu("search", "Buscador", "buscador"),
            crear_boton_menu("package", "Inventario", "inventario"),
            
            # NUEVO: Botón de Cuenta Personal (accesible para todos)
            crear_boton_menu("user-round-cog", "Mi Cuenta", "cuenta"),
            
            # --- SECCIÓN ADMINISTRADOR (Condicional) ---
            rx.cond(
                ContableState.usuario_rol == "administrador",
                rx.vstack(
                    rx.divider(border_color="#222228", margin_y="1em"),
                    crear_boton_menu("users", "Usuarios", "usuarios"),
                    width="100%"
                )
            ),

            # Empuja el perfil hacia abajo
            rx.spacer(),

            # --- PANEL DE USUARIO Y LOGOUT ---
            rx.hstack(
                rx.vstack(
                    rx.text(ContableState.usuario_nombre, color="#E2E8F0", size="2", weight="bold"),
                    rx.badge(
                        ContableState.usuario_rol,
                        color_scheme=rx.cond(ContableState.usuario_rol == "administrador", "purple", "blue"),
                        variant="soft",
                        size="1"
                    ),
                    spacing="0",
                    align="start",
                ),
                rx.button(
                    rx.icon(tag="log-out", size=18),
                    on_click=ContableState.logout,
                    variant="ghost",
                    color="#F56565",
                    size="2",
                    _hover={"bg": "#2D1515"},
                ),
                width="100%",
                justify_content="space-between",
                padding="0.8em",
                bg="#1A1A21",
                border_radius="8px",
                border="1px solid #2D3748",
            ),
            
            spacing="2",
            align="start",
            width="100%",
            height="100%",
        ),
        width="250px",
        height="100vh",
        position="fixed",
        left="0",
        top="0",
        padding="1.5em",
        bg="#111116",
        border_right="1px solid #222228",
        z_index="100", 
    )