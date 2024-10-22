import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox, QVBoxLayout, QHBoxLayout, QGridLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from datetime import datetime

# Archivo para almacenar los datos de los artistas
FILE_NAME = 'artistas.json'

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Artistas de K-pop")
        self.setGeometry(100, 100, 900, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ffe6f2;  /* Fondo rosado claro */
            }
            QLabel {
                color: #333333;
            }
            QLineEdit {
                background-color: #ffffff;
                color: #333333;
                border: 2px solid #ff99cc;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton {
                background-color: #ff66b2;
                color: #ffffff;
                border: none;
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #ff85c2;
            }
            QTableWidget {
                background-color: #fff0f5;
                color: #333333;
                gridline-color: #ff99cc;
            }
            QHeaderView::section {
                background-color: #ff99cc;
                color: #ffffff;
            }
        """)

        self.artistas = self.cargar_artistas()
        self.init_ui()

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Título
        self.title_label = QLabel("Gestión de Artistas de K-pop")
        self.title_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)

        # Barra de Búsqueda
        self.search_layout = QHBoxLayout()
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Buscar por ID")
        self.search_button = QPushButton("Buscar")
        self.search_button.clicked.connect(self.buscar_artista)
        self.search_layout.addWidget(self.id_input)
        self.search_layout.addWidget(self.search_button)

        # Formulario
        self.form_layout = QGridLayout()
        self.form_layout.setSpacing(10)

        self.nombre_label = QLabel("Nombre:")
        self.nombre_input = QLineEdit()
        self.form_layout.addWidget(self.nombre_label, 0, 0)
        self.form_layout.addWidget(self.nombre_input, 0, 1)

        self.apellido_label = QLabel("Apellido:")
        self.apellido_input = QLineEdit()
        self.form_layout.addWidget(self.apellido_label, 1, 0)
        self.form_layout.addWidget(self.apellido_input, 1, 1)

        self.cargo_label = QLabel("Cargo:")
        self.cargo_input = QLineEdit()
        self.form_layout.addWidget(self.cargo_label, 2, 0)
        self.form_layout.addWidget(self.cargo_input, 2, 1)

        self.departamento_label = QLabel("Departamento:")
        self.departamento_input = QLineEdit()
        self.form_layout.addWidget(self.departamento_label, 3, 0)
        self.form_layout.addWidget(self.departamento_input, 3, 1)

        self.salario_label = QLabel("Salario:")
        self.salario_input = QLineEdit()
        self.form_layout.addWidget(self.salario_label, 4, 0)
        self.form_layout.addWidget(self.salario_input, 4, 1)

        self.fecha_label = QLabel("Fecha de Contratación:")
        self.fecha_input = QLineEdit()
        self.form_layout.addWidget(self.fecha_label, 5, 0)
        self.form_layout.addWidget(self.fecha_input, 5, 1)

        # Botones
        self.btn_layout = QHBoxLayout()
        self.btn_layout.setSpacing(20)

        self.btn_add = QPushButton("Agregar")
        self.btn_add.clicked.connect(self.agregar_artista)
        self.btn_layout.addWidget(self.btn_add)

        self.btn_update = QPushButton("Actualizar")
        self.btn_update.clicked.connect(self.actualizar_artista)
        self.btn_layout.addWidget(self.btn_update)

        self.btn_delete = QPushButton("Eliminar")
        self.btn_delete.clicked.connect(self.eliminar_artista)
        self.btn_layout.addWidget(self.btn_delete)

        self.btn_clear = QPushButton("Limpiar")
        self.btn_clear.clicked.connect(self.limpiar_campos)
        self.btn_layout.addWidget(self.btn_clear)

        # Tabla
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(["ID", "Nombre", "Apellido", "Cargo", "Departamento", "Salario", "Fecha", "Días Trabajados"])
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(self.table.SelectRows)
        self.table.setEditTriggers(self.table.NoEditTriggers)
        self.table.cellClicked.connect(self.seleccionar_fila)

        # Layout principal
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addLayout(self.search_layout)
        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addLayout(self.btn_layout)
        self.main_layout.addWidget(self.table)

        self.central_widget.setLayout(self.main_layout)

        # Cargar datos en la tabla
        self.visualizar_artistas()

    def cargar_artistas(self):
        try:
            with open(FILE_NAME, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def guardar_artistas(self):
        with open(FILE_NAME, 'w') as f:
            json.dump(self.artistas, f)

    def agregar_artista(self):
        nombre = self.nombre_input.text().strip()
        apellido = self.apellido_input.text().strip()
        cargo = self.cargo_input.text().strip()
        departamento = self.departamento_input.text().strip()
        salario = self.salario_input.text().strip()
        fecha_contratacion = self.fecha_input.text().strip()

        if not all([nombre, apellido, cargo, departamento, salario, fecha_contratacion]):
            QMessageBox.warning(self, "Advertencia", "Por favor, complete todos los campos.")
            return

        id_artista = str(len(self.artistas) + 1)
        artista = {
            'id': id_artista,
            'nombre': nombre,
            'apellido': apellido,
            'cargo': cargo,
            'departamento': departamento,
            'salario': salario,
            'fecha_contratacion': fecha_contratacion
        }

        self.artistas.append(artista)
        self.guardar_artistas()
        self.visualizar_artistas()
        self.limpiar_campos()
        QMessageBox.information(self, "Éxito", "Artista agregado con éxito.")

    def visualizar_artistas(self):
        self.table.setRowCount(0)
        for artista in self.artistas:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(artista['id']))
            self.table.setItem(row_position, 1, QTableWidgetItem(artista['nombre']))
            self.table.setItem(row_position, 2, QTableWidgetItem(artista['apellido']))
            self.table.setItem(row_position, 3, QTableWidgetItem(artista['cargo']))
            self.table.setItem(row_position, 4, QTableWidgetItem(artista['departamento']))
            self.table.setItem(row_position, 5, QTableWidgetItem(artista['salario']))
            self.table.setItem(row_position, 6, QTableWidgetItem(artista['fecha_contratacion']))

            # Calcular los días trabajados
            try:
                fecha = datetime.strptime(artista['fecha_contratacion'], "%d/%m/%Y")
                dias_trabajados = (datetime.now() - fecha).days
                self.table.setItem(row_position, 7, QTableWidgetItem(str(dias_trabajados)))
            except ValueError:
                self.table.setItem(row_position, 7, QTableWidgetItem("Fecha inválida"))

    def seleccionar_fila(self, row, column):
        artista = self.artistas[row]
        self.nombre_input.setText(artista['nombre'])
        self.apellido_input.setText(artista['apellido'])
        self.cargo_input.setText(artista['cargo'])
        self.departamento_input.setText(artista['departamento'])
        self.salario_input.setText(artista['salario'])
        self.fecha_input.setText(artista['fecha_contratacion'])

    def buscar_artista(self):
        """Buscar un artista por ID y cargar sus datos en el formulario."""
        id_artista = self.id_input.text().strip()
        if not id_artista:
            QMessageBox.warning(self, "Advertencia", "Por favor, ingrese un ID para buscar.")
            return

        for artista in self.artistas:
            if artista['id'] == id_artista:
                self.nombre_input.setText(artista['nombre'])
                self.apellido_input.setText(artista['apellido'])
                self.cargo_input.setText(artista['cargo'])
                self.departamento_input.setText(artista['departamento'])
                self.salario_input.setText(artista['salario'])
                self.fecha_input.setText(artista['fecha_contratacion'])
                QMessageBox.information(self, "Éxito", "Artista encontrado.")
                return

        QMessageBox.warning(self, "No encontrado", "Artista no encontrado.")

    def actualizar_artista(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Advertencia", "Seleccione un artista de la tabla para actualizar.")
            return

        row = selected_rows[0].row()
        artista = self.artistas[row]

        artista['nombre'] = self.nombre_input.text().strip()
        artista['apellido'] = self.apellido_input.text().strip()
        artista['cargo'] = self.cargo_input.text().strip()
        artista['departamento'] = self.departamento_input.text().strip()
        artista['salario'] = self.salario_input.text().strip()
        artista['fecha_contratacion'] = self.fecha_input.text().strip()

        self.guardar_artistas()
        self.visualizar_artistas()
        self.limpiar_campos()
        QMessageBox.information(self, "Éxito", "Artista actualizado con éxito.")

    def eliminar_artista(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Advertencia", "Seleccione un artista de la tabla para eliminar.")
            return

        row = selected_rows[0].row()
        self.artistas.pop(row)

        self.guardar_artistas()
        self.visualizar_artistas()
        self.limpiar_campos()
        QMessageBox.information(self, "Éxito", "Artista eliminado con éxito.")

    def limpiar_campos(self):
        self.nombre_input.clear()
        self.apellido_input.clear()
        self.cargo_input.clear()
        self.departamento_input.clear()
        self.salario_input.clear()
        self.fecha_input.clear()
        self.id_input.clear()
        self.table.clearSelection()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())
