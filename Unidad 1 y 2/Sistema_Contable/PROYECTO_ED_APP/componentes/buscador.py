import reflex as rx
from PROYECTO_ED_APP.state import ContableState # <--- El backend


# ================================
# BUSCADOR
# ================================
def vista_buscador() -> rx.Component:
    return rx.box(
        rx.vstack(
            # Título estilizado
            rx.vstack(
                rx.heading(
                    "Buscar registros",
                    size="9",
                    weight="bold",
                    color="white",
                    ),
                rx.text(
                    "Consulta el historial detallado de tus movimientos",
                    color="#718096",
                    font_size="1.1em",
                    ),
                align="start",
                spacing="1",
                margin_bottom="1.5em",
            ),

            # Campo de entrada (Input) estilizado
            rx.input(
                rx.input.slot(
                    rx.icon(
                        tag="search",
                        color="#718096",
                        ),
                        ),
                placeholder="Buscar por nombre, factura o fecha...",
                value=ContableState.texto_busqueda,
                on_change=ContableState.set_texto_busqueda,
                width="100%",
                size="3",
                variant="surface",
                color_scheme="gray",
                style={
                    "background_color": "#141921",
                    "border": "1px solid #2D3748",
                    "color": "white",
                    "border_radius": "12px",
                },
            ),

            rx.divider(margin_y="2em", opacity="0.1"),

            rx.cond(
                ContableState.historial_filtrado.length() == 0,

                rx.center(
                    rx.vstack(
                        rx.icon(
                            tag="search-off",
                            size=50,
                            color="#F56565",
                            opacity=0.5,
                            ),
                        rx.text(
                            "Movimiento no encontrado",
                            color="#F56565",
                            font_weight="bold",
                            font_size="1.2em",
                        ),
                        spacing="3",
                        padding="4em",
                    ),
                    width="100%",
                ),

                # Tabla con diseño Dark Mode mejorado
                rx.box(
                    rx.table.root(
                        rx.table.header(
                            rx.table.row(
                                rx.table.column_header_cell(
                                    "Tipo",
                                    color="#E2E8F0"
                                    ),
                                rx.table.column_header_cell(
                                    "Nombre",
                                    color="#E2E8F0",
                                    ),
                                rx.table.column_header_cell(
                                    "Correo",
                                    color="#E2E8F0",
                                    ),
                                rx.table.column_header_cell(
                                    "Factura",
                                    color="#E2E8F0"
                                    ),
                                rx.table.column_header_cell(
                                    "Producto",
                                    color="#E2E8F0"
                                    ),
                                rx.table.column_header_cell(
                                    "Monto",
                                    color="#E2E8F0"
                                    ),
                                rx.table.column_header_cell(
                                "Fecha y hora",
                                color="#E2E8F0",
                                ),
                            ),
                        ),
                        rx.table.body(
                            rx.foreach(
                                ContableState.historial_filtrado,
                                lambda item: rx.table.row(
                                    rx.table.cell(item["tipo"]),
                                    rx.table.cell(item["nombre"]),
                                    rx.table.cell(item["correo"]),
                                    rx.table.cell(item["numero_factura"]),
                                    rx.table.cell(item["producto"]),
                                    rx.table.cell(
                                        f"${item['monto']}", 
                                        color=rx.cond(item["tipo"] == "Ingreso", "#48BB78", "#F56565"),
                                        font_weight="bold"
                                    ),
                                    rx.table.cell(item["fecha"]),
                                    style={
                                        "color": "#CBD5E0",
                                        "_hover": {"bg": "#1A202C", "transition": "0.2s"}
                                    },
                                )
                            )
                        ),
                        variant="ghost",
                        size="3",
                        width="100%",
                    ),
                    bg="#141921",
                    border="1px solid #2D3748",
                    border_radius="20px",
                    padding="1em",
                    width="100%",
                    overflow_x="auto", # Para evitar que la tabla rompa el diseño en pantallas pequeñas
                ),
            ),
            spacing="4",
            width="100%",
        ),
        padding_y="2em",
        padding_left="300px", # Margen respetado para el Sidebar
        padding_right="3em",
        bg="#0B0E14", # Fondo negro profundo consistente
        min_height="100vh",
        width="100%",
    )