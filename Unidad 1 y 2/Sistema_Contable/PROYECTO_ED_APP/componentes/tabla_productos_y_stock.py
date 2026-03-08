import reflex as rx
from PROYECTO_ED_APP.state import ContableState # <--- El backend

# ================================
# TABLA PRODUCTOS INVENTARIO (COMPACTA + SCROLL)
# ================================


def tabla_productos_stock():
    return rx.box(
        rx.vstack(
            rx.heading("Productos en inventario", size="4"),

            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Producto"),
                        rx.table.column_header_cell("Stock"),
                    )
                ),

                rx.table.body(
                    rx.foreach(
                        ContableState.productos,
                        lambda p: rx.table.row(
                            rx.table.cell(p["nombre"]),
                            rx.table.cell(p["stock"]),
                            
                        ),
                    ),
                    style={"_hover": {"bg": "#1A202C"}},
                ),
            ),
        ),
        height="250px",
        overflow="auto",
        border="0.1px solid #2a2a2a",
        border_radius="10px",
        padding="1em",
        width="350px",
    )

