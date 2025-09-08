import tkinter as tk

class Participante:
    def __init__(self, nombre, institucion):
        self.nombre = nombre
        self.institucion = institucion

    def mostrar_info(self):
        return f"{self.nombre} - {self.institucion}"

class BandaEscolar(Participante):
    _categorias_validas = ["Primaria", "Básico", "Diversificado"]
    _criterios_evaluacion = ["Ritmo", "Uniformidad", "Coreografía", "Alineación", "Puntualidad"]

    def __init__(self, nombre, institucion, categoria):
        super().__init__(nombre, institucion)
        self._categoria = None
        self.set_categoria(categoria)
        self._puntajes = {}

    def set_categoria(self, categoria):
        if categoria in BandaEscolar._categorias_validas:
            self._categoria = categoria

    def registrar_puntajes(self, puntajes):
        for criterio in BandaEscolar._criterios_evaluacion:
            if criterio not in puntajes:
                return False, f"Falta critero:{criterio}"
            if not (0 <= puntajes[criterio] <= 10):
                return False, f"Puntaje inválido en {criterio}: {puntajes[criterio]}"
        self._puntajes = puntajes
        return True, "Evaluación  registrado correctamente."

    def total(self):
        return sum(self._puntajes.values()) if self._puntajes else 0

    def promedio(self):
        return self.total() / len(BandaEscolar._criterios_evaluacion) if self._puntajes else 0

    def mostrar_info(self):
        info = f"{self.nombre} - {self.institucion} - Categoría: {self._categoria}"
        if self._puntajes:
            info  += f" | Total: {self.total} | {self.promedio: 1f}"
        return info

class Concurso:
    def __init__(self, nombre, fecha):
        self.nombre = nombre
        self.fecha = fecha
        self.bandas = {}

    def inscribir_banda(self, banda):
       if banda.nombre in self.bandas:
           return False, "Ya existe una banda con ese nombre."
       self.bandas[banda.nombre] = banda
       return True, f"Banda {banda.nombre} inscrita correctamente."

    def registrar_evaluacion(self, nombre_banda, puntajes):
        if nombre_banda not in self.bandas:
            print(f" No existe la banda {nombre_banda}")
            return False
        return self.bandas[nombre_banda].registrar_puntajes(puntajes)

    def listar_bandas(self):
        return [banda.mostrar_info() for banda in self.bandas.values()]

    def ranking(self):
        bandas_ordenadas = sorted(
            self.bandas.values(), key=lambda b: (b.total, b.promedio), reverse=True)
        return bandas_ordenadas [:3]

    def guardar_resultados(self, archivo = "bandas.txt"):
            with open(archivo, "w", encoding="utf-8") as f:
                f.write(f"{self.nombre} - {self.fecha}\n")
                f.write("Bandas Inscritos:\n")
                for banda in self.bandas.values():
                    f.write(f"{banda.mostrar_info()}\n")

                f.write("Ranking:\n")
                for i, banda in enumerate(self.ranking(), start=1):
                    f.write(f"{i}. {banda.nombre} - {banda.total} puntos\n")
            return f"Resultados guardados en {archivo}"

class ConcursoBanda:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Concurso de bandas")
        self.ventana.geometry("800x500")

        self.concurso = Concurso("Concurso de bandas - 15 de Septiembre", "2025-09-14")

        boton_inscribir_banda = tk.Button(self.ventana, text="Inscribir Banda", command=self.inscribir_banda)
        boton_inscribir_banda.pack(pady=5)

        boton_registrar_evaluacion = tk.Button(self.ventana, text="Registrar Evaluacion", command=self.registrar_evaluacion)
        boton_registrar_evaluacion.pack(pady=5)

        boton_listar_bandas = tk.Button(self.ventana, text="Listar Bandas", command=self.listar_bandas)
        boton_listar_bandas.pack(pady=5)

        boton_ver_ranking = tk.Button(self.ventana, text="Ver Ranking", command=self.ver_ranking)
        boton_ver_ranking.pack(pady=5)

        boton_salir = tk.Button(self.ventana, text="Salir", command=self.ventana.quit)
        boton_salir.pack(pady=5)

    def inscribir_banda(self):
        ventana_form = tk.Toplevel(self.ventana)
        ventana_form.title("Inscribir Banda")
        ventana_form.geometry("600x500")


        tk.Label(ventana_form, text="Nombre de la Banda:").pack(pady=5)
        entry_nombre=tk.Entry(ventana_form)
        entry_nombre.pack(pady=5)

        tk.Label(ventana_form, text="Institución:").pack(pady=5)
        entry_institucion = tk.Entry(ventana_form)
        entry_institucion.pack(pady=5)

        tk.Label(ventana_form, text="Categoria (Primaria/Básico/Diversificado: ").pack(pady=5)
        entry_categoria = tk.Entry(ventana_form)
        entry_categoria.pack(pady=5)

        def guardar():
            nombre = entry_nombre.get().strip()
            institucion = entry_institucion.get().strip()
            categoria = entry_categoria.get().strip()

            if not nombre or not institucion or not categoria:
                tk.Label(ventana_form, text="Todos los campos son obligatorios:").pack(pady=5)
                return

            try:
                banda = BandaEscolar(nombre, institucion, categoria)
                ok, mensaje = self.concurso.inscribir_banda(banda)
                tk.Label(ventana_form, text=mensaje).pack(pady=5)
                if ok:
                    ventana_form.destroy()
            except ValueError as e:
                tk.Label(ventana_form, text=str(e)).pack(pady=5)

        tk.Button(ventana_form, text="Guardar", command=guardar).pack(pady=5)

    def registrar_evaluacion(self):
        ventana_evalua = tk.Toplevel(self.ventana)
        ventana_evalua.title("Registrar Evaluacion")
        ventana_evalua.geometry("600x500")

        nombres_bandas= list(self.concurso.bandas.keys())
        if not nombres_bandas:
            tk.Label(ventana_evalua, text="No hay bandas registradas para evaluar ").pack(pady=5)
            return

        tk.Label(ventana_evalua, text="Seleccione la banda a Evaluar:").pack(pady=5)
        seleccion = tk.StringVar()
        seleccion.set(nombres_bandas[0])
        tk.OptionMenu(ventana_evalua, seleccion, *nombres_bandas).pack(pady=5)

        entradas = {}
        for criterio in BandaEscolar._criterios_evaluacion:
            tk.Label(ventana_evalua, text=f"{criterio} (0-10):").pack(pady=5)
            entry = tk.Entry(ventana_evalua)
            entry.pack(pady=5)
            entradas[criterio] = entry

        def guardar_evalua():
            nombre_banda = seleccion.get()
            puntajes = {}
            try:
                for criterio, entry in entradas.items():
                    valor = int(entry.get())
                    if valor <0 or valor >10:
                        tk.Label(ventana_evalua, text=f"{criterio} fuera de rango").pack()
                        return
                    puntajes[criterio] = valor
            except ValueError:
                tk.Label(ventana_evalua, text="Los puntajes deben ser números (0-10)").pack()
                return

            ok, correcto, mensaje = self.concurso.registrar_evaluacion(nombre_banda, puntajes)
            tk.Label(ventana_evalua, text=mensaje).pack()

            if ok:
                ventana_evalua.destroy()
        tk.Button(ventana_evalua, text="Guardar Evaluación", command=guardar_evalua).pack(pady=5)

    def listar_bandas(self):
        ventana_lista = tk.Toplevel(self.ventana)
        ventana_lista.title("Listado de Bandas")
        ventana_lista.geometry("600x500")

        bandas = self.concurso.listar_bandas()
        if not bandas:
            tk.Label(ventana_lista, text="No hay bandas registradas:").pack(pady=5)
        else:
            for info in bandas:
                tk.Label(ventana_lista, text=info).pack(pady=5)

    def ver_ranking(self):
        ventana_ranking = tk.Toplevel(self.ventana)
        ventana_ranking.title("Clasificación Final")
        ventana_ranking.geometry("600x500")

        ranking = self.concurso.ranking()
        if not ranking:
            tk.Label(ventana_ranking, text="No hay evaluaciones registraadas").pack(pady=5)
        else:
            for i, banda in enumerate(ranking, start=1):
                tk.Label(ventana_ranking, text=f"{i}. {banda.nombre} ({banda.institucion} - {banda.total} puntos").pack(pady=5)

def guardar_archivo(self):
    mensaje = self.concurso.guardar_resultados()
    ventana_msg = tk.Toplevel(self.ventana)
    ventana_msg.title("Guardar Archivo")
    tk.Label(ventana_msg, text=mensaje).pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = ConcursoBanda(root)
    root.mainloop()