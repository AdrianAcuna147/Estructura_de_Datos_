import reflex as rx 
from PROYECTO_ED_APP.state import ContableState 

# ================================
# COMPONENTE DE TARJETA ESTILIZADA (DARK MODE)
# ================================
def tarjeta_metrica(titulo, valor, icono, color_bg, color_icon):
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.icon(
                    tag=icono,
                    size=24,
                    color=color_icon,
                    ),
                rx.text(
                    titulo,
                    font_size="1em",
                    weight="bold",
                    color="#E2E8F0",
                    ),
                spacing="3",
                align="center",
            ),
            rx.heading(
                valor, 
                size="8", 
                margin_top="0.5em",
                color="white", 
            ),
            align="start",
        ),
        padding="1.8em",
        bg=color_bg, 
        border_radius="20px",
        box_shadow="0 4px 15px rgba(0,0,0,0.3)",
        border=f"1px solid {color_icon}44", 
        _hover={
            "transform": "translateY(-5px)",
            "transition": "all 0.2s ease-in-out",
            "box_shadow": f"0 8px 20px {color_icon}22",
        },
        width="100%",
    )

# ================================
# DASHBOARD CORREGIDO
# ================================
def vista_dashboard() -> rx.Component:
    return rx.box( 
        rx.vstack(
            # Contenedor con Margen Izquierdo para no chocar con el Sidebar
            rx.box(
                rx.vstack(
                    # Cabecera
                    rx.hstack(
                        rx.vstack(
                            rx.heading("Bienvenido",
                                        size="9",
                                        weight="bold",
                                        color="white",
                                        ),
                            rx.heading("Panel de Control",
                                        size="7",
                                        weight="bold",
                                        color="white",
                                        ),
                            rx.text(
                                "Resumen en tiempo real de tu contabilidad",
                                color="#718096",
                                font_size="1.1em",
                                ),
                            align="start",
                            spacing="1",
                        ),
                        rx.spacer(),
                        width="100%",
                    ),
                    
                    rx.divider(margin_y="1em", opacity="0.1"),

                    # Grids de Finanzas
                    rx.grid(
                        tarjeta_metrica("Ingresos", "$" + ContableState.total_ingresos.to(str), "trending-up", "#1C2D24", "#48BB78"), 
                        tarjeta_metrica("Egresos", "$" + ContableState.total_egresos.to(str), "trending-down", "#2D1C1C", "#F56565"), 
                        tarjeta_metrica("Saldo", "$" + ContableState.saldo_total.to(str), "wallet", "#1C252D", "#4299E1"), 
                        columns="3",
                        spacing="6",
                        width="100%",
                    ),

                    # Grids de Registros
                    rx.grid(
                        tarjeta_metrica("Clientes", ContableState.total_clientes.to(str), "users", "#251C2D", "#9F7AEA"), 
                        tarjeta_metrica("Proveedores", ContableState.total_proveedores.to(str), "truck", "#2D241C", "#ED8936"), 
                        tarjeta_metrica("Inventario", ContableState.total_productos.to(str), "package", "#1C2D2D", "#38B2AC"), 
                        columns="3",
                        spacing="6",
                        width="100%",
                        margin_top="2em",
                    ),

                    # Gráfico
                    rx.box(
                        rx.vstack(
                            rx.heading(
                                "Flujo Mensual",
                                size="5",
                                color="#E2E8F0",
                                ),
                            rx.recharts.bar_chart(
                                rx.recharts.cartesian_grid(
                                    stroke_dasharray="3 3",
                                    vertical=False,
                                    stroke="#2D3748"
                                    ),
                                rx.recharts.x_axis(
                                    data_key="mes",
                                    stroke="#718096",
                                    ),
                                rx.recharts.y_axis(
                                    stroke="#718096",
                                    ),
                                rx.recharts.tooltip(
                                    content_style={
                                        "background_color": "#1A202C",
                                        "border_color": "#2D3748",
                                        "color": "white"
                                        }
                                ),
                                rx.recharts.bar(
                                    data_key="ingresos",
                                    fill="#48BB78",
                                    radius=[4, 4, 0, 0],
                                    ),
                                rx.recharts.bar(
                                    data_key="egresos",
                                    fill="#F56565",
                                    radius=[4, 4, 0, 0],
                                    ),
                                data=ContableState.grafica_financiera,
                                width="100%",
                                height=300,
                            ),
                        ),
                        padding="2em",
                        bg="#141921", 
                        border="1px solid #2D3748",
                        border_radius="20px",
                        width="100%",
                        margin_top="2em",
                    ),
                    width="100%",
                ),
                # --- AQUÍ ESTÁ EL AJUSTE VISUAL ---
                padding_left="320px", # Espacio suficiente para que el Menú no lo tape
                padding_right="40px",
                padding_top="40px",
                padding_bottom="40px",
                width="100%",
            ),
            width="100%",
        ),
        bg="#0B0E14", 
        min_height="100vh",
        width="100%",
    )