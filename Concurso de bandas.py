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
        self._puntajes = {}
        self.set_categoria(categoria)

    def set_categoria(self, categoria):
        if categoria not in BandaEscolar._categorias_validas:
            print(f"Categoria Inválida: {categoria}. Categorías inválidas: {BandaEscolar._categorias_validas}")
            return False
        self._categoria = categoria
        return True

    def registrar_puntajes(self, puntajes):
        for criterio in BandaEscolar._criterios:
            if criterio not in puntajes:
                print(f"Falta criterio: {criterio}")
                return False
            if not (0 <= puntajes[criterio] <= 10):
                print(f" Puntaje inválido en {criterio}: {puntajes[criterio]} (0-10)")
                return False
        self._puntajes = puntajes
        return True

    def total(self):
        return sum(self._puntajes.values()) if self._puntajes else 0

    def promedio(self):
        if not self._puntajes:
            return 0
        return self.total / 5

    def mostrar_info(self):
        info = f"Banda: {self.nombre} | Instituación: {self.institucion} | Categoría: {self._categoria} "
        if self._puntajes:
            info  += f" | Total: {self.total}"
        return info

    def linea_archivo(self):
        if self._puntajes:
            return f"{self.nombre}: {self.institucion}: {self._categoria}: "+":".join(str(self._puntajes.get(c, 0)) for c in BandaEscolar._criterios_evaluacion)
        else:
            return f"{self.nombre}: {self.institucion}: {self._categoria}"
class Concurso:
    def __init__(self, nombre, fecha, archivo = "banda.txt"):
        self.nombre = nombre
        self.fecha = fecha
        self.archivo = archivo
        self.bandas = {}
        self.cargar_bandas()

    def cargar_bandas(self):
        try:
            with open(self.archivo, "r", encoding="udf-8") as f:
                for liena in f:
                    linea = linea.strip()
                    if not linea:
                        continue
                    partes = linea.split(":")
                    if len(partes) < 3:
                        continue
                    nombre = partes[0]
                    institucion = partes[1]
                    categoria = partes[2]
                    banda = BandaEscolar(nombre, institucion, categoria)
                    if len(partes) >= 8:
                        try:
                            puntajes = {
                                "ritmo": int(partes[3]),
                                "uniformidad": int(partes[4]),
                                "coreografia": int(partes[5]),
                                "alineacion": int(partes[6]),
                                "puntualidad": int(partes[7]),
                            }
                            banda.registrar_puntajes(puntajes)
                        except ValueError:
                            print(f"Puntaje inválido en línea:{linea}")
                    self.bandas[nombre] = banda
            print (f"Bandas importandas desde {self.archivo}")
        except FileNotFoundError:
            print(f"No existe el archibo {self.archivo}. Se creará al guardar.")

    def guardar_bandas(self):
        try:
            with open(self.archivo, "w", encoding="utf-8") as f:
                for banda in self.bandas.values():
                    f.write(banda.a_linea_archivo() + "\n")
            print(f"Datos gurdados en {self.archivos}")
        except Exception as e:
            print(f"No se puede guardar el archivo:{e}")

    def inscribir_banda(self, banda: BandaEscolar):
       if banda._categoria is None:
           print("No se puede inscrivir: Categoria inválida.")
           return False
       if banda.nombre in self.bandas:
           print(f"Ya existe una banda con el nombre '{banda.nombre}'.")
           return False
       self.bandas[banda.nombre] = banda
       self.cargar_bandas()
       print(f"Banda {banda.nombre} inscrito correctamente.")
       return True

    def registrar_evaluacion(self, nombre_banda, puntajes):
        if nombre_banda not in self.bandas:
            print(f" No existe la banda {nombre_banda}")
            return False
        si = self.bandas[nombre_banda].registrar_puntajes(puntajes)
        if si:
            self.guardar_bandas()
            print(f"Evaluación registrada para '{nombre_banda}'.")
            return si
        return False

    def listar_bandas(self):
        print(f"Listado de Bandas - {self.nombre} ({self.fecha})")
        if not self.bandas:
            print("No hay ninguna banda registrada.")
            return
        for banda in self.bandas.values():
            print(" -", banda.mostrar_info())

    def ranking(self):
        lista = list(self.bandas.values())
        resultado = []

        while lista:
            mayor = lista [0]
            for banda in lista:
                if banda.total > mayor.total:
                    mayor = banda
            resultado.append(mayor)
            lista.remove(mayor)
        print(f"Ranking Final - {self.nombre} ({self.fecha})")
        if not resultado:
            print("Sin bandas")
            return
        posicion = 1
        for banda in resultado:
            print(f"{posicion}. {banda.nombre} ({banda.intitucion}) - {banda._categoria} -> Total: {banda.total}")
            posicion += 1

def pedir_entero(mensaje):
    while True:
        valor = input(mensaje)
        try:
            n = int(valor)
            return n
        except ValueError:
            print("Ingrese un número entero.")

class ConcursoBandaApp:
    def __init__(self):
        self.ventana =tk.Tk()
        self.ventana.title("Concurso de bandas - Quetzaltenango")
        self.ventana.geometry("800x600")

        self.menu()

        tk.label(
            self.ventana,
            text="Sistema de insctripcion y evaluacion de Bandas Escolares\nConcurso 14 de Septiembre - Quetzaltenango",
            font=("Arial", 20, "bold"),
            justify="center"
        ).pack(pady=50)

        self.ventana.mainloop()

    def menu(self):
        barra = tk.Menu(self.ventana)
        opciones = tk.Menu(barra, tearoff=0)
        opciones.add_command(label="Inscribir Banda", command=self.inscribir_banda)
        opciones.add_command(label="Registrar Evaluación", commando=self.registrar_evaluacion)
        opciones.add_command(label="Listar Bandas", command=self.listar_bandas)
        opciones.add_command(label="Ver Ranking", command=self.ver_ranking)
        opciones.add_separator()
        opciones.add_command(label="Ventana de Saludo", command=self.ventana_saludo)
        opciones.add_separator()
        opciones.add_command(label="Salir", command=self.ventana.quit)
        barra.add_cascade(label="Opciones", menu=opciones)
        self.ventana.config(menu=barra)

    def inscribir_banda(self):
        print("Se abrió la ventana: Inscribir Banda")
        tk.Toplevel(self.ventana).title("Inscribir Banda")

    def registrar_evaluacion(self):
        print("Se abrió la ventana: Registrar Evaluacion")
        tk.Toplevel(self.ventana).title("Evaluación")

    def listar_bandas(self):
        print("Se abrió la ventana: Listado de Bandas ")
        tk.Toplevel(self.ventana).title("Listado de Bandas")

    def ver_ranking(self):
        print("Se abri la ventana: Clasificación Final")
        tk.Toplevel(self.ventana).title("Clasificación Final")


def menu():
    concurso = Concurso("Concurso de Bandas - 15 de Septiembre", "15-09-2025")

    while True:
        print("\n----MENÚ DE CONCURSO DE BANDAS----")
        print("1. Inscribir Banda")
        print("2. Registrar Evaluacion")
        print("3. Listar Bandas")
        print("4. Ver ranking final")
        print("5. Guardar en archivo")
        print("6. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nombre = input("Nombre de la bandas: ").strip()
            institucion = input("Institución: ").strip()
            categoria = input("Categoria (Primaria/Básico/Diversificado: ").strip()
            banda = BandaEscolar(nombre, institucion, categoria)
            concurso.inscribir_banda(banda)

        elif opcion == "2":
            nombre = input("Nombre de la banda a evaluar: ").strip()
            puntajes = {}
            print("Ingrese puntajes (o a 10)")
            for criterio in BandaEscolar._criterios_evaluacion:
                puntajes[criterio] = pedir_entero(f"{criterio}: ")
            concurso.registrar_evaluacion(nombre, puntajes)

        elif opcion == "3":
            concurso.listar_bandas()

        elif opcion == "4":
            concurso.ranking()

        elif opcion == "5":
            concurso.guardar_bandas()

        elif opcion == "6":
            print("Saliendo... ¡Gracias por participar!")
            break

        else:
            print("Opción inválida.")

if __name__ == "__main__":
    menu()
