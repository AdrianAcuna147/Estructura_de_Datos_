import reflex as rx
from PROYECTO_ED_APP.state import ContableState # <--- El backend

# ================================
# HISTORIAL
# ================================
def vista_historial() -> rx.Component:
    return rx.box(
        rx.vstack(
            # Cabecera estilizada
            rx.vstack(
                rx.heading(
                        "Historial de registros",
                        size="9",
                        weight="bold",
                        color="white"
                        ),
                rx.text(
                    "Listado completo de todas las transacciones realizadas",
                    color="#718096",
                    font_size="1.1em"
                    ),
                align="start",
                spacing="1",
                margin_bottom="2em",
            ),

            # Contenedor de la tabla tipo Tarjeta
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
                                color="#E2E8F0"
                                ),
                            rx.table.column_header_cell(
                                "Correo",
                                color="#E2E8F0"
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
                                color="#E2E8F0"
                                ),
                        )
                    ),
                    rx.table.body(
                        rx.foreach(
                            ContableState.historial,
                            lambda item: rx.table.row(
                                rx.table.cell(item["tipo"]),
                                rx.table.cell(item["nombre"]),
                                rx.table.cell(item["correo"]),
                                rx.table.cell(item["numero_factura"]),
                                rx.table.cell(item["producto"]),
                                # Monto con color dinámico (Verde para ingresos, rojo para egresos)
                                rx.table.cell(
                                    f"${item['monto']}",
                                    color=rx.cond(item["tipo"] == "Ingreso", "#48BB78", "#F56565"),
                                    font_weight="bold"
                                ),
                                rx.table.cell(item["fecha"]),
                                style={
                                    "color": "#CBD5E0",
                                    "transition": "all 0.2s",
                                    "_hover": {"bg": "#1A202C"}
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
                padding="1.5em",
                width="100%",
                overflow_x="auto", # Evita que se corte en pantallas pequeñas
            ),
            spacing="4",
            width="100%",
        ),
        padding_y="2em",
        padding_left="300px", # Espacio para el Sidebar
        padding_right="3em",
        bg="#0B0E14",
        min_height="100vh",
        width="100%",
    )