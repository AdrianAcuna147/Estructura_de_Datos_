#   //////////////////////////#
#  //      FRONT-END       // #
# //////////////////////////  #


import reflex as rx
from ..state import ContableState # <--- El backend

#Todos los archivos de frontend convergen aqui porque este es el archivo main del front end 
#Todos los archivos estan en la carpeta /pages

#    main_folder    |folder| file    |      funcion
from PROYECTO_ED_APP.componentes.dashboard import vista_dashboard
from PROYECTO_ED_APP.componentes.historial import vista_historial
from PROYECTO_ED_APP.componentes.buscador import vista_buscador
from PROYECTO_ED_APP.componentes.contable import vista_contable
from PROYECTO_ED_APP.componentes.inventario import vista_inventario
from PROYECTO_ED_APP.componentes.sidebar import sidebar


# ================================
# PÁGINA PRINCIPAL
# ================================
def index() -> rx.Component:
    # El index en donde todas las funciones del front end son llamadas para poder ser utilizadas
    return rx.hstack(
        sidebar(),
        rx.box(
            rx.cond(
                ContableState.pestana_actual == "dashboard",
                vista_dashboard(),
                rx.cond(
                    ContableState.pestana_actual == "contable",
                    vista_contable(),
                    rx.cond(
                        ContableState.pestana_actual == "historial",
                        vista_historial(),
                        rx.cond(
                            ContableState.pestana_actual == "buscador",
                            vista_buscador(),
                            vista_inventario()
                        )
                    )
                )
            ),
            width="100%",
        ),
        width="100%",
        min_height="100vh",
        align="start", 
    )
