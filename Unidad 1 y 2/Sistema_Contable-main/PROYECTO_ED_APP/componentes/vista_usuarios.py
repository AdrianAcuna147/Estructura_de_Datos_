import reflex as rx
from PROYECTO_ED_APP.state import ContableState
from PROYECTO_ED_APP.componentes.sidebar import sidebar


def vista_usuarios() -> rx.Component:
    return rx.box(
        sidebar(),
        rx.box(
            rx.tabs.root(
                rx.tabs.list(
                    rx.tabs.trigger("Lista de Usuarios", value="lista", cursor="pointer"),
                    rx.cond(
                        ContableState.usuario_rol == "administrador",
                        rx.tabs.trigger("Nuevo Usuario", value="nuevo", cursor="pointer"),
                    ),
                    margin_bottom="1.5em",
                ),

                # ── TAB: LISTA ─────────────────────────────────────
                rx.tabs.content(
                    rx.vstack(
                        rx.hstack(
                            rx.vstack(
                                rx.heading("Gestión de Usuarios", size="7", weight="bold", color="#FFFFFF"),
                                rx.text("Administra cuentas de empleados y administradores", color="#718096", size="2"),
                                align="start", spacing="1",
                            ),
                            width="100%", align="center", margin_bottom="1.5em",
                        ),
                        rx.cond(
                            ContableState.usuarios_lista.length() == 0,
                            rx.center(
                                rx.vstack(
                                    rx.icon(tag="users", size=48, color="#4A5568"),
                                    rx.text("No hay usuarios registrados", color="#718096", size="4", weight="medium"),
                                    rx.text("Ve a la pestaña 'Nuevo Usuario' para crear uno", color="#4A5568", size="2"),
                                    spacing="3", align="center",
                                ),
                                padding="4em",
                                bg="#141921",
                                border="1px solid #2D3748",
                                border_radius="20px",
                                width="100%",
                            ),
                            rx.box(
                                rx.table.root(
                                    rx.table.header(
                                        rx.table.row(
                                            rx.table.column_header_cell("Nombre",    color="#A0AEC0", size="1"),
                                            rx.table.column_header_cell("Apellidos", color="#A0AEC0", size="1"),
                                            rx.table.column_header_cell("Correo",    color="#A0AEC0", size="1"),
                                            rx.table.column_header_cell("Rol",       color="#A0AEC0", size="1"),
                                            rx.table.column_header_cell("Estado",    color="#A0AEC0", size="1"),
                                            rx.table.column_header_cell("Acción",    color="#A0AEC0", size="1"),
                                        )
                                    ),
                                    rx.table.body(
                                        rx.foreach(
                                            ContableState.usuarios_lista,
                                            lambda u: rx.table.row(
                                                rx.table.cell(rx.text(u["nombre"],    color="#E2E8F0", weight="bold", size="2")),
                                                rx.table.cell(rx.text(u["apellidos"], color="#CBD5E0", size="2")),
                                                rx.table.cell(rx.text(u["correo"],    color="#A0AEC0", size="2")),
                                                rx.table.cell(
                                                    rx.match(
                                                        u["rol"],
                                                        ("administrador", rx.badge("Administrador", color_scheme="purple")),
                                                        ("empleado",      rx.badge("Empleado",      color_scheme="blue")),
                                                        rx.badge(u["rol"], color_scheme="gray"),
                                                    )
                                                ),
                                                rx.table.cell(
                                                    rx.cond(
                                                        u["activo"],
                                                        rx.badge("Activo",   color_scheme="green"),
                                                        rx.badge("Inactivo", color_scheme="red"),
                                                    )
                                                ),
                                                rx.table.cell(
                                                    rx.cond(
                                                        ContableState.usuario_rol == "administrador",
                                                        rx.button(
                                                            rx.cond(u["activo"], rx.icon(tag="user-x", size=14),  rx.icon(tag="user-check", size=14)),
                                                            rx.cond(u["activo"], rx.text("Desactivar", size="1"), rx.text("Activar", size="1")),
                                                            on_click=ContableState.desactivar_usuario(u["id"]),
                                                            size="1", variant="ghost", cursor="pointer",
                                                            color=rx.cond(u["activo"], "#F56565", "#48BB78"),
                                                            _hover={"bg": "#2D3748"},
                                                        ),
                                                    )
                                                ),
                                                style={"_hover": {"bg": "#1A202C"}},
                                            )
                                        )
                                    ),
                                    variant="ghost", size="3", width="100%",
                                ),
                                bg="#141921",
                                border="1px solid #2D3748",
                                border_radius="20px",
                                padding="1.5em",
                                width="100%",
                                overflow_x="auto",
                            ),
                        ),
                        spacing="4", width="100%",
                    ),
                    value="lista",
                ),

                # ── TAB: NUEVO USUARIO ──────────────────────────────
                rx.tabs.content(
                    rx.vstack(
                        rx.hstack(
                            rx.icon(tag="user-plus", size=20, color="#4299E1"),
                            rx.heading("Registrar Nuevo Usuario", size="7", weight="bold", color="#FFFFFF"),
                            spacing="2", align="center", margin_bottom="1.5em",
                        ),
                        rx.box(
                            rx.vstack(
                                rx.hstack(
                                    rx.vstack(
                                        rx.text("Nombre", color="#718096", size="1"),
                                        rx.input(
                                            placeholder="Nombre",
                                            value=ContableState.reg_nombre,
                                            on_change=ContableState.set_reg_nombre,
                                            bg="#2D3748", color="#FFFFFF", border="none", width="100%",
                                        ),
                                        width="100%", spacing="1",
                                    ),
                                    rx.vstack(
                                        rx.text("Apellidos", color="#718096", size="1"),
                                        rx.input(
                                            placeholder="Apellidos",
                                            value=ContableState.reg_apellidos,
                                            on_change=ContableState.set_reg_apellidos,
                                            bg="#2D3748", color="#FFFFFF", border="none", width="100%",
                                        ),
                                        width="100%", spacing="1",
                                    ),
                                    spacing="3", width="100%",
                                ),
                                rx.vstack(
                                    rx.text("Correo", color="#718096", size="1"),
                                    rx.input(
                                        placeholder="correo@dominio.com",
                                        value=ContableState.reg_correo,
                                        on_change=ContableState.set_reg_correo,
                                        bg="#2D3748", color="#FFFFFF", border="none", width="100%",
                                    ),
                                    width="100%", spacing="1",
                                ),
                                rx.vstack(
                                    rx.text("Contraseña", color="#718096", size="1"),
                                    rx.input(
                                        placeholder="Mínimo 6 caracteres",
                                        type="password",
                                        value=ContableState.reg_password,
                                        on_change=ContableState.set_reg_password,
                                        bg="#2D3748", color="#FFFFFF", border="none", width="100%",
                                    ),
                                    width="100%", spacing="1",
                                ),
                                rx.vstack(
                                    rx.text("Rol", color="#718096", size="1"),
                                    rx.select(
                                        ["empleado", "administrador"],
                                        value=ContableState.reg_rol,
                                        on_change=ContableState.set_reg_rol,
                                        bg="#2D3748", color="#FFFFFF", border="none", width="100%",
                                    ),
                                    width="100%", spacing="1",
                                ),
                                rx.cond(
                                    ContableState.reg_error != "",
                                    rx.hstack(
                                        rx.icon(tag="circle-alert", size=13, color="#F56565"),
                                        rx.text(ContableState.reg_error, color="#F56565", size="2"),
                                        spacing="1", padding="0.75em",
                                        bg="#2D1515", border_radius="8px", width="100%",
                                    ),
                                ),
                                rx.cond(
                                    ContableState.reg_exito != "",
                                    rx.hstack(
                                        rx.icon(tag="circle-check", size=13, color="#48BB78"),
                                        rx.text(ContableState.reg_exito, color="#48BB78", size="2"),
                                        spacing="1", padding="0.75em",
                                        bg="#152D1F", border_radius="8px", width="100%",
                                    ),
                                ),
                                rx.button(
                                    rx.icon(tag="user-plus", size=15),
                                    "Registrar Usuario",
                                    on_click=ContableState.registrar_usuario,
                                    bg="#3182CE", color="#FFFFFF", cursor="pointer",
                                    size="3", width="100%",
                                    _hover={"bg": "#2B6CB0"},
                                ),
                                spacing="4", width="100%",
                            ),
                            bg="#141921",
                            border="1px solid #2D3748",
                            border_radius="20px",
                            padding="2em",
                            width="100%",
                            max_width="520px",
                        ),
                        spacing="4", width="100%",
                    ),
                    value="nuevo",
                ),

                default_value="lista",
                width="100%",
                on_mount=ContableState.cargar_usuarios,
            ),
            padding_y="2em",
            padding_left="300px",
            padding_right="3em",
        ),
        width="100%",
        min_height="100vh",
        bg="#0B0E14",
    )