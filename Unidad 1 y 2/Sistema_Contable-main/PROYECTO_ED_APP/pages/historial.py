import reflex as rx
from ..state import ContableState # <--- El backend

# ================================
# HISTORIAL
# ================================
def vista_historial() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading("Historial de registros", size="5"),

            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Tipo"),
                        rx.table.column_header_cell("Nombre"),
                        rx.table.column_header_cell("Correo"),
                        rx.table.column_header_cell("Factura"),
                        rx.table.column_header_cell("Producto"),
                        rx.table.column_header_cell("Monto"),
                        rx.table.column_header_cell("Fecha y hora"),
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
                            rx.table.cell(f"${item['monto']}"),
                            rx.table.cell(item["fecha"]),
                        )
                    )
                ),
                width="100%",
            ),
        ),
        padding="1em",
        width="100%",
    )