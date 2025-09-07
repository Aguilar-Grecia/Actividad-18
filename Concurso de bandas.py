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
            r = self._puntajes.get("ritmo", 0)
            u = self._puntajes.get("uniformidad", 0)
            c = self._puntajes.get("coreografia", 0)
            a = self._puntajes.get("alineacion", 0)
            p = self._puntajes.get("puntualidad", 0)
            return f"{self.nombre}: {self.institucion}: {self._categoria}:{r}:{u}:{c}:{a}:{p}"
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
            with open(self.archivo, "r", encodig="udf-8") as f:
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
                            rimtmo = int(partes[3])
                            uniformidad = int(partes[4])
                            coreografia = int(partes[5])
                            alineacion = int(partes[6])
                            puntualidad = int(partes[7])
                            puntajes = (
                                "ritmo": ritmo,
                                "uniformidad": uniformidad,
                                "coreografia": coreografia,
                                "alineacion": alineacion,
                                "puntualidad": puntualidad,
                            )
                            banda.registrar_puntaje(puntajes)
                        except ValueError:



    def inscribir_banda(self, banda: BandaEscolar):
        if banda.nombre in self.bandas:
            print(f"Ya existe una banda con el nombre {banda.nombre}")
            return False
        self.bandas[banda.nombre] = banda
        return True

    def registrar_evaluacion(self, nombre_banda, puntaje):
        if nombre_banda not in self.bandas:
            print(f" No existe la banda {nombre_banda}")
            return False
        return self.bandas[nombre_banda].registrar_puntajes(puntaje)

    def listar_bandas(self):
        print(f"Listado de Bandas - {self.nombre} ({self.fecha})")
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

        print(f" Ranking Final")
        posicion = 1
        for banda in resultado:
            print(f"{posicion}. {banda.nombre} ({banda.intitucion}) - {banda._categoria} -> Total: {banda.total}")
            posicion += 1

