#historial.py
import reflex as rx
from PROYECTO_ED_APP.state import ContableState


def color_badge(tipo: str):
    return rx.match(
        tipo,
        ("Cliente",            rx.badge(tipo, color_scheme="green")),
        ("Proveedor",          rx.badge(tipo, color_scheme="red")),
        ("Venta",              rx.badge(tipo, color_scheme="green")),
        ("Recepción",          rx.badge(tipo, color_scheme="orange")),
        ("Producto creado",    rx.badge(tipo, color_scheme="blue")),
        ("Producto editado",   rx.badge(tipo, color_scheme="yellow")),
        ("Producto eliminado", rx.badge(tipo, color_scheme="red")),
        rx.badge(tipo, color_scheme="gray"),
    )


def vista_historial() -> rx.Component:
    return rx.box(
        rx.vstack(
            # CABECERA
            rx.vstack(
                rx.heading(
                    "Historial de movimientos en el sistema",
                    size="9",
                    weight="bold",
                    color="white",
                ),
                rx.text(
                    "Listado completo de todos los movimientos del sistema",
                    color="#718096",
                    font_size="1.1em",
                ),
                align="start",
                spacing="1",
                margin_bottom="2em",
            ),

            # FILTROS
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.vstack(
                            rx.text("Tipo", color="#A0AEC0", size="1", weight="bold"),
                            rx.select(
                                ContableState.tipos_disponibles_historial,
                                value=ContableState.filtro_tipo_historial,
                                on_change=ContableState.set_filtro_tipo_historial,
                                placeholder="Todos",
                                bg="#2D3748",
                                color="white",
                            ),
                            spacing="1", width="150px",
                        ),
                        rx.vstack(
                            rx.text("Usuario", color="#A0AEC0", size="1", weight="bold"),
                            rx.select(
                                ContableState.usuarios_disponibles_historial,
                                value=ContableState.filtro_usuario_historial,
                                on_change=ContableState.set_filtro_usuario_historial,
                                placeholder="Todos",
                                bg="#2D3748",
                                color="white",
                            ),
                            spacing="1", width="150px",
                        ),
                        rx.vstack(
                            rx.text("Desde", color="#A0AEC0", size="1", weight="bold"),
                            rx.input(
                                type="date",
                                value=ContableState.filtro_fecha_inicio,
                                on_change=ContableState.set_filtro_fecha_inicio,
                                bg="#2D3748",
                                color="white",
                            ),
                            spacing="1",
                        ),
                        rx.vstack(
                            rx.text("Hasta", color="#A0AEC0", size="1", weight="bold"),
                            rx.input(
                                type="date",
                                value=ContableState.filtro_fecha_fin,
                                on_change=ContableState.set_filtro_fecha_fin,
                                bg="#2D3748",
                                color="white",
                            ),
                            spacing="1",
                        ),
                        rx.vstack(
                            rx.text("Buscar", color="#A0AEC0", size="1", weight="bold"),
                            rx.input(
                                placeholder="Texto...",
                                value=ContableState.texto_busqueda,
                                on_change=ContableState.set_texto_busqueda,
                                bg="#2D3748",
                                color="white",
                                width="180px",
                            ),
                            spacing="1",
                        ),
                        rx.vstack(
                            rx.button(
                                "Limpiar filtros",
                                on_click=ContableState.limpiar_filtros_historial,
                                variant="ghost",
                                color="#718096",
                                size="1",
                            ),
                            spacing="1",
                        ),
                        spacing="3", align="end", width="100%",
                    ),
                    spacing="2", width="100%",
                ),
                padding="1.5em",
                bg="#141921",
                border="1px solid #2D3748",
                border_radius="15px",
                width="100%",
                margin_bottom="1.5em",
            ),

            # TABLA
            rx.box(
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Tipo",         color="#E2E8F0"),
                            rx.table.column_header_cell("Descripción",  color="#E2E8F0"),
                            rx.table.column_header_cell("Fecha y hora", color="#E2E8F0"),
                            rx.table.column_header_cell("Acciones", color="#E2E8F0"),
                            # Columna Usuario: solo visible para admin
                            rx.cond(
                                ContableState.usuario_rol == "administrador",
                                rx.table.column_header_cell(
                                    rx.hstack(
                                        rx.icon(tag="user", size=13, color="#A0AEC0"),
                                        rx.text("Usuario", color="#E2E8F0"),
                                        spacing="1",
                                        align="center",
                                    )
                                ),
                                rx.fragment(),
                            ),
                        )
                    ),
                    rx.table.body(
                        rx.foreach(
                            ContableState.historial_filtrado_y_paginado,
                            lambda item: rx.table.row(
                                rx.table.cell(
                                    color_badge(item["tipo"]),
                                ),
                                rx.table.cell(
                                    rx.text(
                                        item["descripcion"],
                                        color="#CBD5E0",
                                        size="2",
                                    )
                                ),
                                rx.table.cell(
                                    rx.text(
                                        item["fecha"],
                                        color="#718096",
                                        size="2",
                                    )
                                ),
                                        # Acciones: editar/anular solo para administradores
                                        rx.table.cell(
                                            rx.cond(
                                                ContableState.usuario_rol == "administrador",
                                                rx.cond(
                                                    item.get("id", 0) != 0,
                                                    rx.hstack(
                                                        rx.button(
                                                            "Editar",
                                                            on_click=ContableState.abrir_modal_editar_transaccion(item.get("id", 0)),
                                                            size="2",
                                                            variant="ghost",
                                                            color="#4299E1",
                                                        ),
                                                        rx.button(
                                                            "Anular",
                                                            on_click=ContableState.cancelar_transaccion(item.get("id", 0)),
                                                            size="2",
                                                            variant="ghost",
                                                            color="#E53E3E",
                                                        ),
                                                        spacing="2",
                                                    ),
                                                    rx.text("—", color="#4A5568"),
                                                ),
                                                rx.text("—", color="#4A5568"),
                                            )
                                        ),
                                # Celda Usuario: solo visible para admin
                                rx.cond(
                                    ContableState.usuario_rol == "administrador",
                                    rx.table.cell(
                                        rx.cond(
                                            item["usuario"] != "",
                                            rx.badge(
                                                item["usuario"],
                                                color_scheme="purple",
                                                variant="soft",
                                            ),
                                            rx.text("—", color="#4A5568", size="2"),
                                        )
                                    ),
                                    rx.fragment(),
                                ),
                                style={
                                    "transition": "all 0.2s",
                                    "_hover": {"bg": "#1A202C"},
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
                overflow_x="auto",
            ),

            # PAGINACIÓN
            rx.hstack(
                rx.button(
                    "← Anterior",
                    on_click=lambda: ContableState.set_pagina_actual(ContableState.pagina_actual - 1),
                    is_disabled=ContableState.pagina_actual <= 1,
                    variant="ghost",
                    color="#4299E1",
                ),
                rx.text(
                    ContableState.pagina_actual.to(str) + " / " + ContableState.total_paginas_historial.to(str),
                    color="#A0AEC0",
                    weight="bold",
                ),
                rx.button(
                    "Siguiente →",
                    on_click=lambda: ContableState.set_pagina_actual(ContableState.pagina_actual + 1),
                    is_disabled=ContableState.pagina_actual >= ContableState.total_paginas_historial,
                    variant="ghost",
                    color="#4299E1",
                ),
                rx.spacer(),
                rx.text(
                    f"{ContableState.items_por_pagina} items/página",
                    color="#718096",
                    size="2",
                ),
                spacing="3",
                align="center",
                width="100%",
                margin_top="1.5em",
            ),

            spacing="4",
            width="100%",
        ),
        padding_y="2em",
        padding_left="300px",
        padding_right="3em",
        bg="#0B0E14",
        min_height="100vh",
        width="100%",
    )


# Modal compartido para editar transacciones (se puede incluir en el index.py si deseas hacerlo global)
def modal_editar_transaccion() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Editar Transacción", color="white"),
            rx.vstack(
                rx.vstack(rx.text("Número de factura", color="#A0AEC0"), rx.input(value=ContableState.editar_trans_numero, on_change=ContableState.set_editar_trans_numero, bg="#2D3748", color="white")),
                rx.vstack(rx.text("Monto", color="#A0AEC0"), rx.input(value=ContableState.editar_trans_monto.to(str), on_change=ContableState.set_editar_trans_monto, type="number", bg="#2D3748", color="white")),
                rx.vstack(rx.text("Producto", color="#A0AEC0"), rx.input(value=ContableState.editar_trans_producto, on_change=ContableState.set_editar_trans_producto, bg="#2D3748", color="white")),
                rx.vstack(rx.text("Nombre", color="#A0AEC0"), rx.input(value=ContableState.editar_trans_nombre, on_change=ContableState.set_editar_trans_nombre, bg="#2D3748", color="white")),
                rx.vstack(rx.text("Correo", color="#A0AEC0"), rx.input(value=ContableState.editar_trans_correo, on_change=ContableState.set_editar_trans_correo, bg="#2D3748", color="white")),
                rx.hstack(
                    rx.button("Cancelar", on_click=ContableState.cerrar_modal_editar_transaccion, variant="ghost", color="#718096"),
                    rx.button("Guardar", on_click=ContableState.guardar_edicion_transaccion, bg="#3182CE", color="white"),
                    spacing="3",
                ),
                spacing="3",
            ),
            bg="#1A202C",
            border="1px solid #2D3748",
            border_radius="15px",
            padding="2em",
            max_width="640px",
        ),
        open=ContableState.mostrar_modal_editar_transaccion,
    )