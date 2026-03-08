import reflex as rx
from PROYECTO_ED_APP.state import ContableState

# ================================
# TABLA PRODUCTOS INVENTARIO (COMPACTA + SCROLL)
# ================================

def tabla_productos_stock():
    return rx.box(
        rx.vstack(
            rx.heading("Productos en inventario", size="4", color="#E2E8F0"),
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Nombre", color="#A0AEC0"),
                        rx.table.column_header_cell("Marca",  color="#A0AEC0"),
                        rx.table.column_header_cell("Modelo", color="#A0AEC0"),
                        rx.table.column_header_cell("Stock",  color="#A0AEC0"),
                    )
                ),
                rx.table.body(
                    rx.foreach(
                        ContableState.productos,
                        lambda p: rx.table.row(
                            rx.table.cell(p["nombre"], color="#E2E8F0"),
                            rx.table.cell(p["marca"],  color="#E2E8F0"),
                            rx.table.cell(p["modelo"], color="#E2E8F0"),
                            rx.table.cell(p["stock"],  color="white"),
                            style={"_hover": {"bg": "#1A202C"}},
                        ),
                    ),
                ),
            ),
        ),
        border="0.1px solid #2a2a2a",
        border_radius="10px",
        padding="1em",
        width="100%",
    )