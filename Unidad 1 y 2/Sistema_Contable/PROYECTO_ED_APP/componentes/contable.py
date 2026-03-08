import reflex as rx
from PROYECTO_ED_APP.state import ContableState 
from PROYECTO_ED_APP.componentes.tabla_productos_y_stock import tabla_productos_stock
from PROYECTO_ED_APP.componentes.sidebar import sidebar # Asegúrate de importar tu sidebar

def vista_contable() -> rx.Component:
    return rx.box(
        # 1. LLAMADA AL SIDEBAR (Fijo a la izquierda)
        sidebar(),

        # 2. CONTENEDOR PRINCIPAL CON MARGEN PARA EL SIDEBAR
        rx.box(
            rx.center(
                rx.hstack(
                    # COLUMNA IZQUIERDA
                    rx.vstack(
                        rx.heading(
                            "Sistema Contable",
                            size="9",
                            weight="bold",
                            margin_bottom="0.5em",
                            color="#FFFFFF"
                        ),
                        
                        # TARJETA: SALDO INICIAL
                        rx.box(
                            rx.vstack(
                                rx.hstack(
                                    rx.icon(
                                        tag="wallet",
                                        size=18,
                                        color="#A0AEC0"
                                        ),
                                    rx.text(
                                        "Saldo Inicial",
                                        weight="bold",
                                        color="#E2E8F0"
                                        ),
                                    spacing="2",
                                ),
                                rx.input(
                                    placeholder="0",
                                    type="number",
                                    value=ContableState.saldo_inicial, 
                                    on_change=ContableState.set_saldo_inicial,
                                    width="100%",
                                    variant="surface",
                                    bg="#2D3748",
                                    color="#FFFFFF",
                                    border="none",
                                    style={"_hover": {"bg": "#1A202C"}},
                                ),
                                align="start",
                                width="100%",
                            ),
                            padding="1.5em",
                            bg="#1A202C",
                            border_radius="xl",
                            border="1px solid #2D3748",
                            width="100%",
                        ),

                        # TARJETA: DETALLES DE FACTURA
                        rx.box(
                            rx.vstack(
                                rx.hstack(
                                    rx.icon(tag="file-text", size=18, color="#A0AEC0"),
                                    rx.text("Detalles de Factura", weight="bold", color="#E2E8F0"),
                                    spacing="2"
                                ),
                                rx.input(
                                    placeholder="Número de factura",
                                    value=ContableState.numero_factura,
                                    on_change=ContableState.set_numero_factura,
                                    width="100%",
                                    bg="#2D3748",
                                    color="#FFFFFF",
                                    border="none",
                                    style={"_hover": {"bg": "#1A202C"}},
                                ),
                                rx.input(
                                    placeholder="Nombre del producto",
                                    value=ContableState.nombre_producto,
                                    on_change=ContableState.set_nombre_producto,
                                    width="100%",
                                    bg="#2D3748",
                                    color="#FFFFFF",
                                    border="none",
                                    style={"_hover": {"bg": "#1A202C"}},
                                ),
                                rx.input(
                                    placeholder="Monto",
                                    type="number",
                                    value=ContableState.monto_factura,
                                    on_change=ContableState.set_monto_factura,
                                    width="100%",
                                    bg="#2D3748",
                                    color="#FFFFFF",
                                    border="none",
                                    style={"_hover": {"bg": "#1A202C"}},
                                ),
                                
                                # --- ERROR GENERAL ---
                                rx.cond(
                                    ContableState.error_general,
                                    rx.text(
                                        ContableState.error_general,
                                        color="#F56565",
                                        size="2",
                                        weight="bold",
                                    )
                                ),

                                rx.hstack(
                                    rx.button(
                                        "Agregar cliente",
                                        on_click=ContableState.abrir_modal_cliente,
                                        color_scheme="green",
                                        bg="#38A169",
                                        width="50%",
                                        _hover={
                                                "transform": "translateY(-5px)",
                                                "transition": "all 0.2s ease-in-out",
                                                "box_shadow": "0 8px 20px #38A16922"
                                                },
                                    ),
                                    rx.button(
                                        "Agregar proveedor",
                                        on_click=ContableState.abrir_modal_proveedor,
                                        color_scheme="red",
                                        bg="#E53E3E",
                                        width="50%",
                                        _hover={
                                            "transform": "translateY(-5px)",
                                            "transition": "all 0.2s ease-in-out",
                                            "box_shadow": "0 8px 20px #E53E3E22"
                                            },
                                    ),
                                    width="100%",
                                    padding_top="0.5em",
                                ),
                                spacing="3",
                                width="100%",
                            ),
                            padding="1.5em",
                            bg="#1A202C",
                            border_radius="xl",
                            border="1px solid #2D3748",
                            width="100%",
                        ),

                        # RESUMEN TOTALES
                        rx.grid(
                            rx.vstack(
                                rx.text(
                                        "Ingresos",
                                        size="2",
                                        color="#A0AEC0"
                                        ),
                                rx.text(
                                    f"${ContableState.total_ingresos}",
                                    color="#48BB78",
                                    weight="bold",
                                    size="4"
                                    ),
                                align_items="center",
                            ),
                            rx.vstack(
                                rx.text(
                                        "Egresos",
                                        size="2",
                                        color="#A0AEC0"
                                        ),
                                rx.text(
                                    f"${ContableState.total_egresos}",
                                    color="#F56565",
                                    weight="bold",
                                    size="4"
                                    ),
                                align_items="center",
                            ),
                            rx.vstack(
                                rx.text(
                                    "Saldo Total",
                                    size="2",
                                    color="#A0AEC0",
                                    ),
                                rx.text(
                                    f"${ContableState.saldo_total}",
                                    color="#FFFFFF",
                                    weight="bold",
                                    size="4",
                                    ),
                                align_items="center",
                            ),
                            columns="3",
                            width="100%",
                            padding="1.5em",
                            bg="#1A202C",
                            border_radius="xl",
                            border="1px solid #2D3748",
                        ),
                        width="420px",
                        spacing="5",
                        align_items="stretch",
                    ),

                    # COLUMNA DERECHA: TABLA
                    rx.box(
                        rx.vstack(
                            rx.hstack(
                                rx.icon(
                                    tag="package",
                                    size=22,
                                    color="#A0AEC0"
                                    ),
                                rx.heading(
                                    "Inventario y Stock",
                                    size="5",
                                    color="#E2E8F0"
                                    ),
                                spacing="3",
                            ),
                            rx.divider(
                                color_scheme="gray",
                                opacity="0.2",
                                ),
                            rx.box(
                                tabla_productos_stock(),
                                width="100%",
                                overflow_x="auto"
                            ),
                            width="100%",
                            spacing="4",
                        ),
                        padding="2em",
                        bg="#1A202C",
                        border_radius="20px",
                        border="1px solid #2D3748",
                        width="480px",
                        height="fit-content",
                        margin_top="11.5em",
                    ),
                    spacing="9",
                    align_items="start",
                    justify="center",
                    width="100%", 
                    max_width="1100px",
                ),
            ),
            padding_left="250px", # MARGEN PARA QUE EL SIDEBAR NO TAPE EL CONTENIDO
            width="100%",
        ),

        # MODAL OSCURO CON ERRORES (Fixed)
        rx.cond(
            ContableState.mostrar_modal,
            rx.center(
                rx.box(
                    rx.vstack(
                        rx.heading(
                            rx.cond(
                                ContableState.tipo_modal == "cliente",
                                "Datos del Cliente",
                                "Datos del Proveedor"
                                ),
                            size="5",
                            color="#FFFFFF",
                        ),
                        rx.cond(
                            ContableState.tipo_modal == "cliente",
                            rx.vstack(
                                rx.input(
                                    placeholder="Nombre",
                                    on_change=ContableState.set_nombre_cliente,
                                    width="100%",
                                    bg="#2D3748",
                                    color="#FFFFFF",
                                    border="none",
                                    ),
                                rx.cond(
                                    ContableState.error_nombre,
                                    rx.text(
                                            ContableState.error_nombre,
                                            color="#F56565",
                                            size="1",
                                            ),
                                            ),
                                rx.input(
                                    placeholder="Correo",
                                    on_change=ContableState.set_correo_cliente,
                                    width="100%",
                                    bg="#2D3748",
                                    color="#FFFFFF",
                                    border="none"
                                    ),
                                rx.cond(
                                    ContableState.error_correo,
                                    rx.text(
                                        ContableState.error_correo,
                                        color="#F56565",
                                        size="1"
                                        ),
                                        ),
                                spacing="3", width="100%"
                            ),
                            rx.vstack(
                                rx.input(
                                    placeholder="Nombre",
                                    on_change=ContableState.set_nombre_proovedor,
                                    width="100%",
                                    bg="#2D3748",
                                    color="#FFFFFF",
                                    border="none",
                                    ),
                                rx.cond(
                                    ContableState.error_nombre,
                                    rx.text(ContableState.error_nombre,
                                            color="#F56565",
                                            size="1",
                                            ),
                                            ),
                                rx.input(
                                    placeholder="Correo",
                                    on_change=ContableState.set_correo_proovedor,
                                    width="100%",
                                    bg="#2D3748",
                                    color="#FFFFFF",
                                    border="none",
                                    ),
                                rx.cond(
                                    ContableState.error_correo,
                                    rx.text(
                                        ContableState.error_correo,
                                        color="#F56565",
                                        size="1",
                                        ),
                                        ),
                                spacing="3",
                                width="100%"
                            )
                        ),
                        rx.hstack(
                            rx.button(
                                "Cancelar",
                                on_click=ContableState.cerrar_modal,
                                variant="ghost",
                                color_scheme="gray"
                                ),
                            rx.button(
                                "Confirmar",
                                on_click=ContableState.confirmar_modal,
                                color_scheme="blue",
                                bg="#3182CE"
                                ),
                            width="100%",
                            justify_content="end",
                            margin_top="1em",
                        ),
                    ),
                    padding="2.5em",
                    bg="#1A202C",
                    border_radius="2xl",
                    border="1px solid #4A5568",
                    width="380px",
                ),
                position="fixed",
                top="0",
                left="0",
                width="100%",
                height="100%",
                bg="rgba(0,0,0,0.8)",
                z_index="1000",
            )
        ),
        width="100%",
        min_height="100vh",
        bg="#0B0E14",
        padding="2em",
        padding_left="100px",
        padding_right="2em",
    )