import reflex as rx
from PROYECTO_ED_APP.state import ContableState


def vista_login() -> rx.Component:
    return rx.center(
        rx.vstack(
            # LOGO / TÍTULO
            rx.vstack(
                rx.hstack(
                    rx.icon(tag="building-2", size=36, color="#4299E1"),
                    rx.vstack(
                        rx.heading("StakFlow", size="7", weight="bold", color="#FFFFFF"),
                        rx.text("Gestion de Contabilidad", color="#718096", size="2"),
                        spacing="0",
                        align="start",
                    ),
                    spacing="3",
                    align="center",
                ),
                align="center",
                margin_bottom="2em",
            ),

            # CARD DE LOGIN
            rx.box(
                rx.vstack(
                    rx.vstack(
                        rx.icon(tag="lock", size=24, color="#4299E1"),
                        rx.heading("Iniciar Sesión", size="5", color="#FFFFFF", weight="bold"),
                        rx.text("Ingresa tus credenciales para continuar", color="#718096", size="2"),
                        align="center",
                        spacing="1",
                        margin_bottom="1.5em",
                    ),

                    # CAMPO NOMBRE
                    rx.vstack(
                        rx.hstack(
                            rx.icon(tag="user", size=14, color="#A0AEC0"),
                            rx.text("Nombre de usuario", color="#A0AEC0", size="2"),
                            spacing="1",
                        ),
                        rx.input(
                            placeholder="Tu nombre",
                            value=ContableState.login_nombre,
                            on_change=ContableState.set_login_nombre,
                            width="100%",
                            bg="#2D3748",
                            color="#FFFFFF",
                            border=rx.cond(
                                ContableState.login_error != "",
                                "1px solid #F56565", "1px solid #4A5568"
                            ),
                            _focus={"border": "1px solid #4299E1", "outline": "none"},
                            _placeholder={"color": "#4A5568"},
                            size="3",
                        ),
                        width="100%",
                        spacing="1",
                    ),

                    # CAMPO CONTRASEÑA con botón ojo
                    rx.vstack(
                        rx.hstack(
                            rx.icon(tag="key-round", size=14, color="#A0AEC0"),
                            rx.text("Contraseña", color="#A0AEC0", size="2"),
                            spacing="1",
                        ),
                        rx.box(
                            rx.input(
                                placeholder="Tu contraseña",
                                type=rx.cond(ContableState.login_mostrar_password, "text", "password"),
                                value=ContableState.login_password,
                                on_change=ContableState.set_login_password,
                                width="100%",
                                bg="#2D3748",
                                color="#FFFFFF",
                                border=rx.cond(
                                    ContableState.login_error != "",
                                    "1px solid #F56565", "1px solid #4A5568"
                                ),
                                _focus={"border": "1px solid #4299E1", "outline": "none"},
                                _placeholder={"color": "#4A5568"},
                                size="3",
                                padding_right="3em",  # espacio para el botón
                            ),
                            # Botón ojo superpuesto a la derecha
                            rx.button(
                                rx.cond(
                                    ContableState.login_mostrar_password,
                                    rx.icon(tag="eye-off", size=16, color="#718096"),
                                    rx.icon(tag="eye", size=16, color="#718096"),
                                ),
                                on_click=ContableState.toggle_login_password,
                                variant="ghost",
                                position="absolute",
                                right="0.5em",
                                top="50%",
                                transform="translateY(-50%)",
                                padding="0.2em",
                                height="auto",
                                min_width="auto",
                                bg="transparent",
                                _hover={"bg": "transparent", "color": "#FFFFFF"},
                                z_index="1",
                            ),
                            position="relative",
                            width="100%",
                        ),
                        width="100%",
                        spacing="1",
                    ),

                    # ERROR
                    rx.cond(
                        ContableState.login_error != "",
                        rx.hstack(
                            rx.icon(tag="circle-alert", size=14, color="#F56565"),
                            rx.text(ContableState.login_error, color="#F56565", size="2"),
                            spacing="1",
                            padding="0.5em 1em",
                            bg="#2D1515",
                            border="1px solid #F56565",
                            border_radius="lg",
                            width="100%",
                        ),
                    ),

                    # BOTÓN LOGIN
                    rx.button(
                        rx.icon(tag="log-in", size=16),
                        "Ingresar",
                        on_click=ContableState.login,
                        width="100%",
                        size="3",
                        bg="#3182CE",
                        color="#FFFFFF",
                        _hover={
                            "bg": "#2B6CB0",
                            "transform": "translateY(-2px)",
                            "transition": "all 0.2s ease",
                            "box_shadow": "0 8px 20px #3182CE44",
                        },
                        margin_top="0.5em",
                    ),

                    # ENLACE RECUPERACIÓN DE CONTRASEÑA
                    rx.button(
                        "¿Olvidaste tu contraseña?",
                        on_click=ContableState.abrir_modal_recuperacion,
                        variant="ghost",
                        color="#4299E1",
                        size="1",
                        width="100%",
                        _hover={"color": "#63B3ED"},
                    ),

                    spaces="4",
                    width="100%",
                ),
                padding="2.5em",
                bg="#1A202C",
                border_radius="2xl",
                border="1px solid #2D3748",
                width="400px",
                box_shadow="0 25px 50px rgba(0,0,0,0.5)",
            ),

            rx.text(
                "© 2026 Sistema ED — Todos los derechos reservados",
                color="#4A5568",
                size="1",
                margin_top="1em",
            ),
            spacing="0",
            align="center",
        ),
        width="100%",
        min_height="100vh",
        bg="#0B0E14",
    )


def modal_recuperacion_contrasena() -> rx.Component:
    """Modal para recuperación de contraseña (3 pasos: correo -> código+password -> confirmación)."""
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Recuperar Contraseña", color="white"),
            rx.cond(
                # Paso 1: Solicitar correo
                ContableState.recuperacion_paso == 1,
                rx.vstack(
                    rx.vstack(
                        rx.icon(tag="mail", size=24, color="#4299E1"),
                        rx.text("Ingresa tu correo", color="#E2E8F0", size="2", weight="bold"),
                        rx.text("Usaremos este correo para enviar el código", color="#718096", size="1"),
                        spacing="1",
                        align="center",
                    ),
                    rx.input(
                        placeholder="tu@correo.com",
                        value=ContableState.recuperacion_correo,
                        on_change=ContableState.set_recuperacion_correo,
                        bg="#2D3748",
                        color="white",
                        width="100%",
                        border=rx.cond(ContableState.recuperacion_error != "", "1px solid #F56565", "none"),
                    ),
                    rx.cond(
                        ContableState.recuperacion_error != "",
                        rx.hstack(
                            rx.icon(tag="circle-alert", size=12, color="#F56565"),
                            rx.text(ContableState.recuperacion_error, color="#F56565", size="1"),
                            spacing="1", width="100%",
                        ),
                    ),
                    rx.hstack(
                        rx.button("Cancelar", on_click=ContableState.cerrar_modal_recuperacion, variant="ghost", color="#718096"),
                        rx.button("Enviar Código", on_click=ContableState.solicitar_recuperacion_contrasena, bg="#3182CE", color="white"),
                        spacing="3", width="100%", justify="end",
                    ),
                    spacing="3",
                ),
                rx.cond(
                    # Paso 2: Ingresar código + contraseña
                    ContableState.recuperacion_paso == 2,
                    rx.vstack(
                        rx.vstack(
                            rx.icon(tag="key-round", size=24, color="#4299E1"),
                            rx.text("Verifica tu identidad", color="#E2E8F0", size="2", weight="bold"),
                            rx.text("Ingresa el código (mostrado en la pantalla) y tu nueva contraseña", color="#718096", size="1"),
                            spacing="1",
                            align="center",
                        ),
                        rx.vstack(
                            rx.text("Código de recuperación", color="#A0AEC0", size="1", weight="bold"),
                            rx.input(
                                placeholder="000000",
                                value=ContableState.recuperacion_codigo,
                                on_change=ContableState.set_recuperacion_codigo,
                                bg="#2D3748",
                                color="white",
                                width="100%",
                            ),
                            spacing="1",
                        ),
                        rx.vstack(
                            rx.text("Nueva contraseña", color="#A0AEC0", size="1", weight="bold"),
                            rx.input(
                                placeholder="Mínimo 6 caracteres",
                                type="password",
                                value=ContableState.recuperacion_password_nueva,
                                on_change=ContableState.set_recuperacion_password_nueva,
                                bg="#2D3748",
                                color="white",
                                width="100%",
                            ),
                            spacing="1",
                        ),
                        rx.cond(
                            ContableState.recuperacion_error != "",
                            rx.hstack(
                                rx.icon(tag="circle-alert", size=12, color="#F56565"),
                                rx.text(ContableState.recuperacion_error, color="#F56565", size="1"),
                                spacing="1", width="100%",
                            ),
                        ),
                        rx.hstack(
                            rx.button("Atrás", on_click=lambda: ContableState.set_pagina_actual(1), variant="ghost", color="#718096"),
                            rx.button("Cambiar Contraseña", on_click=ContableState.validar_y_cambiar_contrasena_recuperacion, bg="#3182CE", color="white"),
                            spacing="3", width="100%", justify="end",
                        ),
                        spacing="3",
                    ),
                    # Paso 3: Confirmación
                    rx.vstack(
                        rx.hstack(
                            rx.icon(tag="check-circle-2", size=32, color="#48BB78"),
                            rx.text("¡Éxito!", color="#48BB78", size="3", weight="bold"),
                            spacing="2",
                            align="center",
                        ),
                        rx.text(ContableState.recuperacion_exito, color="#CBD5E0", size="2", text_align="center"),
                        rx.hstack(
                            rx.button("Cerrar", on_click=ContableState.cerrar_modal_recuperacion, bg="#48BB78", color="white", width="100%"),
                            width="100%",
                        ),
                        spacing="3",
                        align="center",
                    ),
                ),
            ),
            bg="#1A202C",
            border="1px solid #2D3748",
            border_radius="15px",
            padding="2em",
            max_width="500px",
        ),
        open=ContableState.mostrar_modal_recuperacion,
    )