"""Interfaz gráfica con tkinter."""

import tkinter as tk
from tkinter import ttk, messagebox

from sistema import SistemaSoftwareFJ
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from excepciones import ErrorSoftwareFJ, ErrorDatosInvalidos
from persistencia import registrar_log, leer_ultimos_logs, ruta_archivo_log
from datos_demo import cargar_datos_demo


class AplicacionGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Software FJ - Sistema de Gestión")
        self.geometry("950x620")
        self.configure(bg="#f4f6f9")

        self.sistema = SistemaSoftwareFJ()

        # ejecuta la simulación inicial
        self.eventos_demo = cargar_datos_demo(self.sistema)

        self._construir_interfaz()
        self._refrescar_todo()

    def _construir_interfaz(self):
        # encabezado
        encabezado = tk.Label(self, text="Software FJ - Gestión de Clientes, Servicios y Reservas",
                              font=("Segoe UI", 14, "bold"), bg="#2c3e50", fg="white", pady=10)
        encabezado.pack(fill="x")

        # pestañas
        self.pestañas = ttk.Notebook(self)
        self.pestañas.pack(fill="both", expand=True, padx=10, pady=10)

        self._pestaña_clientes()
        self._pestaña_servicios()
        self._pestaña_reservas()
        self._pestaña_demo()

    # ---------- Clientes ----------
    def _pestaña_clientes(self):
        marco = ttk.Frame(self.pestañas)
        self.pestañas.add(marco, text="Clientes")

        formulario = ttk.LabelFrame(marco, text="Registrar nuevo cliente")
        formulario.pack(fill="x", padx=10, pady=10)

        ttk.Label(formulario, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.ent_nombre = ttk.Entry(formulario, width=30)
        self.ent_nombre.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(formulario, text="Documento:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.ent_documento = ttk.Entry(formulario, width=20)
        self.ent_documento.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(formulario, text="Correo:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.ent_correo = ttk.Entry(formulario, width=30)
        self.ent_correo.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(formulario, text="Teléfono:").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.ent_telefono = ttk.Entry(formulario, width=20)
        self.ent_telefono.grid(row=1, column=3, padx=5, pady=5)

        ttk.Button(formulario, text="Registrar", command=self._accion_registrar_cliente)\
            .grid(row=2, column=0, columnspan=4, pady=10)

        cols = ("id", "nombre", "documento", "correo", "telefono")
        self.tabla_clientes = ttk.Treeview(marco, columns=cols, show="headings", height=12)
        for c in cols:
            self.tabla_clientes.heading(c, text=c.capitalize())
            self.tabla_clientes.column(c, width=150)
        self.tabla_clientes.pack(fill="both", expand=True, padx=10, pady=10)

    def _accion_registrar_cliente(self):
        try:
            cliente = self.sistema.registrar_cliente(
                self.ent_nombre.get(),
                self.ent_documento.get(),
                self.ent_correo.get(),
                self.ent_telefono.get(),
            )
        except ErrorSoftwareFJ as e:
            registrar_log("ERROR", f"Registro cliente desde GUI: {e}")
            messagebox.showerror("Error", str(e))
        except Exception as e:
            registrar_log("ERROR", f"Error inesperado registrando cliente: {e}")
            messagebox.showerror("Error inesperado", str(e))
        else:
            messagebox.showinfo("OK", f"Cliente registrado: {cliente.describir()}")
            for entry in (self.ent_nombre, self.ent_documento, self.ent_correo, self.ent_telefono):
                entry.delete(0, tk.END)
            self._refrescar_clientes()
            self._refrescar_combos()

    # ---------- Servicios ----------
    def _pestaña_servicios(self):
        marco = ttk.Frame(self.pestañas)
        self.pestañas.add(marco, text="Servicios")

        formulario = ttk.LabelFrame(marco, text="Crear nuevo servicio")
        formulario.pack(fill="x", padx=10, pady=10)

        ttk.Label(formulario, text="Tipo:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.cmb_tipo_servicio = ttk.Combobox(formulario, state="readonly",
                                              values=["Sala", "Equipo", "Asesoría"], width=15)
        self.cmb_tipo_servicio.current(0)
        self.cmb_tipo_servicio.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(formulario, text="Nombre:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.ent_serv_nombre = ttk.Entry(formulario, width=25)
        self.ent_serv_nombre.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(formulario, text="Precio base:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.ent_serv_precio = ttk.Entry(formulario, width=15)
        self.ent_serv_precio.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(formulario, text="Extra (capacidad/tipo/área):").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.ent_serv_extra = ttk.Entry(formulario, width=25)
        self.ent_serv_extra.grid(row=1, column=3, padx=5, pady=5)

        ttk.Button(formulario, text="Crear servicio", command=self._accion_crear_servicio)\
            .grid(row=2, column=0, columnspan=4, pady=10)

        cols = ("id", "tipo", "descripcion")
        self.tabla_servicios = ttk.Treeview(marco, columns=cols, show="headings", height=12)
        self.tabla_servicios.heading("id", text="ID")
        self.tabla_servicios.heading("tipo", text="Tipo")
        self.tabla_servicios.heading("descripcion", text="Descripción")
        self.tabla_servicios.column("id", width=60)
        self.tabla_servicios.column("tipo", width=120)
        self.tabla_servicios.column("descripcion", width=600)
        self.tabla_servicios.pack(fill="both", expand=True, padx=10, pady=10)

    def _accion_crear_servicio(self):
        tipo = self.cmb_tipo_servicio.get()
        nombre = self.ent_serv_nombre.get()
        precio_txt = self.ent_serv_precio.get()
        extra = self.ent_serv_extra.get()

        try:
            try:
                precio = float(precio_txt)
            except ValueError as e:
                # encadenamos el error original
                raise ErrorDatosInvalidos("Precio inválido") from e

            if tipo == "Sala":
                try:
                    cap = int(extra)
                except ValueError as e:
                    raise ErrorDatosInvalidos("Capacidad inválida") from e
                servicio = ReservaSala(nombre, precio, cap)
            elif tipo == "Equipo":
                servicio = AlquilerEquipo(nombre, precio, extra)
            elif tipo == "Asesoría":
                servicio = AsesoriaEspecializada(nombre, precio, extra)
            else:
                raise ErrorDatosInvalidos("Tipo de servicio desconocido")

            self.sistema.agregar_servicio(servicio)
        except ErrorSoftwareFJ as e:
            registrar_log("ERROR", f"Crear servicio GUI: {e}")
            messagebox.showerror("Error", str(e))
        except Exception as e:
            registrar_log("ERROR", f"Error inesperado creando servicio: {e}")
            messagebox.showerror("Error inesperado", str(e))
        else:
            messagebox.showinfo("OK", f"Servicio creado: {servicio.describir()}")
            self.ent_serv_nombre.delete(0, tk.END)
            self.ent_serv_precio.delete(0, tk.END)
            self.ent_serv_extra.delete(0, tk.END)
            self._refrescar_servicios()
            self._refrescar_combos()

    # ---------- Reservas ----------
    def _pestaña_reservas(self):
        marco = ttk.Frame(self.pestañas)
        self.pestañas.add(marco, text="Reservas")

        formulario = ttk.LabelFrame(marco, text="Crear y procesar reserva")
        formulario.pack(fill="x", padx=10, pady=10)

        ttk.Label(formulario, text="Cliente:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.cmb_cliente = ttk.Combobox(formulario, state="readonly", width=40)
        self.cmb_cliente.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(formulario, text="Servicio:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.cmb_servicio = ttk.Combobox(formulario, state="readonly", width=40)
        self.cmb_servicio.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(formulario, text="Duración:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.ent_duracion = ttk.Entry(formulario, width=10)
        self.ent_duracion.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(formulario, text="Impuesto %:").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.ent_impuesto = ttk.Entry(formulario, width=10)
        self.ent_impuesto.grid(row=1, column=3, padx=5, pady=5, sticky="w")

        ttk.Label(formulario, text="Descuento %:").grid(row=2, column=2, padx=5, pady=5, sticky="e")
        self.ent_descuento = ttk.Entry(formulario, width=10)
        self.ent_descuento.grid(row=2, column=3, padx=5, pady=5, sticky="w")

        ttk.Button(formulario, text="Crear reserva", command=self._accion_crear_reserva)\
            .grid(row=3, column=0, pady=10)
        ttk.Button(formulario, text="Confirmar selección", command=self._accion_confirmar_reserva)\
            .grid(row=3, column=1, pady=10)
        ttk.Button(formulario, text="Cancelar selección", command=self._accion_cancelar_reserva)\
            .grid(row=3, column=2, pady=10)
        ttk.Button(formulario, text="Procesar selección", command=self._accion_procesar_reserva)\
            .grid(row=3, column=3, pady=10)

        cols = ("id", "cliente", "servicio", "duracion", "estado", "costo")
        self.tabla_reservas = ttk.Treeview(marco, columns=cols, show="headings", height=12)
        for c in cols:
            self.tabla_reservas.heading(c, text=c.capitalize())
            self.tabla_reservas.column(c, width=130)
        self.tabla_reservas.pack(fill="both", expand=True, padx=10, pady=10)

    def _obtener_id_seleccionado(self, tabla, mensaje):
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Atención", mensaje)
            return None
        return int(tabla.item(seleccion[0])["values"][0])

    def _accion_crear_reserva(self):
        try:
            if not self.cmb_cliente.get() or not self.cmb_servicio.get():
                raise ErrorDatosInvalidos("Debe seleccionar cliente y servicio")

            id_cliente = int(self.cmb_cliente.get().split(" - ")[0])
            id_servicio = int(self.cmb_servicio.get().split(" - ")[0])

            try:
                duracion = float(self.ent_duracion.get())
            except ValueError as e:
                raise ErrorDatosInvalidos("Duración inválida") from e

            reserva = self.sistema.crear_reserva(id_cliente, id_servicio, duracion)
        except ErrorSoftwareFJ as e:
            registrar_log("ERROR", f"Crear reserva GUI: {e}")
            messagebox.showerror("Error", str(e))
        except Exception as e:
            registrar_log("ERROR", f"Error inesperado en reserva: {e}")
            messagebox.showerror("Error inesperado", str(e))
        else:
            messagebox.showinfo("OK", f"Reserva creada: {reserva.describir()}")
            self._refrescar_reservas()

    def _accion_confirmar_reserva(self):
        id_r = self._obtener_id_seleccionado(self.tabla_reservas, "Seleccione una reserva")
        if id_r is None:
            return
        try:
            r = self.sistema.buscar_reserva(id_r)
            r.confirmar()
        except ErrorSoftwareFJ as e:
            registrar_log("ERROR", f"Confirmar reserva GUI: {e}")
            messagebox.showerror("Error", str(e))
        else:
            messagebox.showinfo("OK", f"Reserva #{id_r} confirmada")
            self._refrescar_reservas()

    def _accion_cancelar_reserva(self):
        id_r = self._obtener_id_seleccionado(self.tabla_reservas, "Seleccione una reserva")
        if id_r is None:
            return
        try:
            r = self.sistema.buscar_reserva(id_r)
            r.cancelar()
        except ErrorSoftwareFJ as e:
            registrar_log("ERROR", f"Cancelar reserva GUI: {e}")
            messagebox.showerror("Error", str(e))
        else:
            messagebox.showinfo("OK", f"Reserva #{id_r} cancelada")
            self._refrescar_reservas()

    def _accion_procesar_reserva(self):
        id_r = self._obtener_id_seleccionado(self.tabla_reservas, "Seleccione una reserva")
        if id_r is None:
            return
        try:
            r = self.sistema.buscar_reserva(id_r)

            impuesto = self.ent_impuesto.get().strip()
            descuento = self.ent_descuento.get().strip()
            try:
                impuesto = float(impuesto) if impuesto else None
                descuento = float(descuento) if descuento else None
            except ValueError as e:
                raise ErrorDatosInvalidos("Impuesto o descuento inválido") from e

            costo = r.procesar(impuesto=impuesto, descuento=descuento)
        except ErrorSoftwareFJ as e:
            registrar_log("ERROR", f"Procesar reserva GUI: {e}")
            messagebox.showerror("Error", str(e))
        except Exception as e:
            registrar_log("ERROR", f"Error inesperado procesando reserva: {e}")
            messagebox.showerror("Error inesperado", str(e))
        else:
            messagebox.showinfo("OK", f"Reserva procesada. Costo final: ${costo}")
            self._refrescar_reservas()

    # ---------- Demo / Logs ----------
    def _pestaña_demo(self):
        marco = ttk.Frame(self.pestañas)
        self.pestañas.add(marco, text="Simulación y Logs")

        ttk.Label(marco, text="Resultado de las 10+ operaciones de simulación inicial:",
                  font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=10, pady=5)

        self.txt_demo = tk.Text(marco, height=15, wrap="word", bg="#fdfdfd")
        self.txt_demo.pack(fill="both", expand=True, padx=10, pady=5)

        ttk.Label(marco, text=f"Archivo de logs: {ruta_archivo_log()}",
                  font=("Segoe UI", 9, "italic")).pack(anchor="w", padx=10, pady=5)

        ttk.Button(marco, text="Ver últimos logs", command=self._ver_logs).pack(pady=5)

    def _ver_logs(self):
        contenido = leer_ultimos_logs(40)
        if not contenido:
            messagebox.showinfo("Logs", "Aún no hay archivo de logs")
            return
        ventana = tk.Toplevel(self)
        ventana.title("Últimos eventos del log")
        ventana.geometry("700x400")
        txt = tk.Text(ventana, wrap="word")
        txt.pack(fill="both", expand=True)
        txt.insert("1.0", "".join(contenido))
        txt.config(state="disabled")

    # ---------- Refrescos ----------
    def _refrescar_todo(self):
        self._refrescar_clientes()
        self._refrescar_servicios()
        self._refrescar_reservas()
        self._refrescar_combos()
        self._refrescar_demo()

    def _refrescar_clientes(self):
        for fila in self.tabla_clientes.get_children():
            self.tabla_clientes.delete(fila)
        for c in self.sistema.clientes:
            self.tabla_clientes.insert("", "end",
                values=(c.id, c.nombre, c.documento, c.correo, c.telefono))

    def _refrescar_servicios(self):
        for fila in self.tabla_servicios.get_children():
            self.tabla_servicios.delete(fila)
        for s in self.sistema.servicios:
            tipo = type(s).__name__
            self.tabla_servicios.insert("", "end", values=(s.id, tipo, s.describir()))

    def _refrescar_reservas(self):
        for fila in self.tabla_reservas.get_children():
            self.tabla_reservas.delete(fila)
        for r in self.sistema.reservas:
            costo = f"${r.costo_final}" if r.costo_final is not None else "-"
            self.tabla_reservas.insert("", "end",
                values=(r.id, r.cliente.nombre, r.servicio.nombre, r.duracion, r.estado, costo))

    def _refrescar_combos(self):
        self.cmb_cliente["values"] = [f"{c.id} - {c.nombre}" for c in self.sistema.clientes]
        self.cmb_servicio["values"] = [f"{s.id} - {s.nombre}" for s in self.sistema.servicios]

    def _refrescar_demo(self):
        self.txt_demo.delete("1.0", tk.END)
        for i, (estado, msg) in enumerate(self.eventos_demo, start=1):
            self.txt_demo.insert(tk.END, f"{i:>2}. [{estado}] {msg}\n")


def iniciar_aplicacion():
    # función pública para arrancar la GUI desde main.py
    app = AplicacionGUI()
    app.mainloop()

