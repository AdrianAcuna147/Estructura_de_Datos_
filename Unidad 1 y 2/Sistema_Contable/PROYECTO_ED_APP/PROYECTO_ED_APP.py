# Importamos reflex porque es importante
import reflex as rx
#======================
from PROYECTO_ED_APP.pages.index import index
from PROYECTO_ED_APP.state import ContableState

#Aqui arranca la app
#NO BORRAR!!!!!!
# app = rx.App() la app no correra
app = rx.App()
app.add_page(index, on_load=ContableState.on_load)
