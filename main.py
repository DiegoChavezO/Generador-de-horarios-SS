import sys
import pandas as pd
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QTabWidget, QLineEdit, QComboBox,QSpinBox, QVBoxLayout, QWidget, QLabel, QTableWidget, QTableWidgetItem, QLineEdit, QHBoxLayout, QCalendarWidget, QDateEdit
from PyQt6.QtCore import QDate

import data_transform
import generar_horarios_tt

class ScheduleApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Generador de Horarios de Trabajos Terminales")
        self.setGeometry(100, 100, 1000, 600)

        self.tt_days_df = pd.DataFrame(columns=["Inicio", "Fin", "8-10", "10-12", "12-2", "2-4", "4-6", "6-8", "Total TT"])
        self.generated_schedule_df = None

        self.initUI()
    
    def initUI(self):
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        self.upload_tab = QWidget()
        self.schedule_tab = QWidget()
        self.tt_tab = QWidget()
        self.tt_days_tab = QWidget()
        self.generated_schedule_tab = QWidget()

        self.tabs.addTab(self.upload_tab, "Carga de Datos")
        self.tabs.addTab(self.schedule_tab, "Horarios Profesores")
        self.tabs.addTab(self.tt_tab, "Trabajos Terminales")
        self.tabs.addTab(self.tt_days_tab, "Configuración TT")
        self.tabs.addTab(self.generated_schedule_tab, "Horarios Generados")
        
        self.initUploadTab()
        self.initScheduleTab()
        self.initTTTab()
        self.initTTDaysTab()
        self.initGeneratedScheduleTab()
    
    def initUploadTab(self):
        layout = QVBoxLayout()
        
        self.label = QLabel("Carga los archivos de datos:")
        layout.addWidget(self.label)
        
        self.load_professors_button = QPushButton("Cargar Horarios de Profesores")
        self.load_professors_button.clicked.connect(self.load_professor_schedule)
        layout.addWidget(self.load_professors_button)
        
        self.load_tt_button = QPushButton("Cargar Trabajos Terminales")
        self.load_tt_button.clicked.connect(self.load_tt_data)
        layout.addWidget(self.load_tt_button)
        
        self.generate_schedule_button = QPushButton("Generar Horarios")
        self.generate_schedule_button.clicked.connect(self.generate_tt_schedule) #funcionalidad core para asignacion
        layout.addWidget(self.generate_schedule_button)
        
        self.upload_tab.setLayout(layout)
    
    def initScheduleTab(self):
        layout = QVBoxLayout()
        
        self.professors_table = QTableWidget()
        layout.addWidget(self.professors_table)
        
        # Formulario para agregar profesor
        form_layout = QHBoxLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nombre del Profesor")
        form_layout.addWidget(self.name_input)
        
        self.schedule_combo = QComboBox()
        self.schedule_combo.addItems(["7-2", "9-3", "2-9", "3-10", "SIN HORARIO"])
        form_layout.addWidget(self.schedule_combo)
        
        self.add_professor_button = QPushButton("Añadir Profesor")
        self.add_professor_button.clicked.connect(self.add_professor)
        form_layout.addWidget(self.add_professor_button)
        
        self.delete_professor_button = QPushButton("Eliminar Profesor")
        self.delete_professor_button.clicked.connect(self.delete_professor)
        form_layout.addWidget(self.delete_professor_button)
        layout.addLayout(form_layout)
        # Botón para aplicar la clasificación horaria
        self.apply_schedule_button = QPushButton("Aplicar Clasificación Horaria")
        self.apply_schedule_button.clicked.connect(self.apply_classification_to_schedule)
        layout.addWidget(self.apply_schedule_button)
        
        
        self.schedule_tab.setLayout(layout)

    def initTTTab(self):
        layout = QVBoxLayout()
        
        self.tt_table = QTableWidget()
        layout.addWidget(self.tt_table)
        
        form_layout = QHBoxLayout()
        self.tt_input = QLineEdit()
        self.tt_input.setPlaceholderText("TT")
        form_layout.addWidget(self.tt_input)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nombre del Trabajo Terminal")
        form_layout.addWidget(self.name_input)
        
        self.director1_input = QLineEdit()
        self.director1_input.setPlaceholderText("Director 1")
        form_layout.addWidget(self.director1_input)
        
        self.director2_input = QLineEdit()
        self.director2_input.setPlaceholderText("Director 2")
        form_layout.addWidget(self.director2_input)
        
        self.sinodal1_input = QLineEdit()
        self.sinodal1_input.setPlaceholderText("Sinodal 1")
        form_layout.addWidget(self.sinodal1_input)
        
        self.sinodal2_input = QLineEdit()
        self.sinodal2_input.setPlaceholderText("Sinodal 2")
        form_layout.addWidget(self.sinodal2_input)
        
        self.sinodal3_input = QLineEdit()
        self.sinodal3_input.setPlaceholderText("Sinodal 3")
        form_layout.addWidget(self.sinodal3_input)
        
        self.add_tt_button = QPushButton("Añadir TT")
        self.add_tt_button.clicked.connect(self.add_tt)
        form_layout.addWidget(self.add_tt_button)
        
        self.delete_tt_button = QPushButton("Eliminar TT")
        self.delete_tt_button.clicked.connect(self.delete_tt)
        form_layout.addWidget(self.delete_tt_button)
        
        layout.addLayout(form_layout)
        self.tt_tab.setLayout(layout)   
    def load_professor_schedule(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo de horarios de profesores", "", "Archivos CSV o Excel (*.csv *.xlsx *.xls)")
        if file_path:
            if file_path.endswith(".csv"):
                self.professors_df = pd.read_csv(file_path, encoding='UTF-8')
            else:
                self.professors_df = pd.read_excel(file_path, encoding='UTF-8')
            
            self.professors_df = data_transform.transform_professor_schedule(self.professors_df)
            self.label.setText("Horarios de profesores cargados y transformados correctamente.")
            self.display_professor_schedule()
    
    def load_tt_data(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo de trabajos terminales", "", "Excel Files (*.xlsx *.xls)")
        if file_path:
            self.tt_df = pd.read_excel(file_path)
            self.label.setText("Trabajos terminales cargados correctamente.")
    
    def generate_schedule(self):
        if hasattr(self, 'professors_df') and hasattr(self, 'tt_df'):
            self.label.setText("Generando horarios...")
            
            result_df = pd.DataFrame({
                'ID TT': ["2025-A001"],
                'Director 1': ["RUBÉN PEREDO VALDERRAMA"],
                'D1': [True],
                'Director 2': ["#N/A"],
                'Sinodal 1': ["ELIZABETH MORENO GALVÁN"],
                'D3': [True],
                'Horario': ["8:00 a 10:00"],
                'Día': ["Martes 26 de noviembre"],
            })
            
            self.display_results(result_df)
        else:
            self.label.setText("Debes cargar ambos archivos primero.")
    
    def add_professor(self):
        new_name = self.name_input.text().strip().upper()
        new_schedule = self.schedule_combo.currentText()
        if new_name:
            new_row = pd.DataFrame([[new_name, None, None, None, None, None, new_schedule]],
                                   columns=self.professors_df.columns)
            self.professors_df = pd.concat([self.professors_df, new_row], ignore_index=True)
            self.display_professor_schedule()
            self.name_input.clear()
    
    def delete_professor(self):
        selected_row = self.professors_table.currentRow()
        if selected_row >= 0:
            self.professors_df.drop(index=selected_row, inplace=True)
            self.professors_df.reset_index(drop=True, inplace=True)
            self.display_professor_schedule()
    
    def display_professor_schedule(self):
        self.professors_table.setRowCount(self.professors_df.shape[0])
        self.professors_table.setColumnCount(self.professors_df.shape[1])
        self.professors_table.setHorizontalHeaderLabels(self.professors_df.columns)
        
        for row in range(self.professors_df.shape[0]):
            for col in range(self.professors_df.shape[1]):
                self.professors_table.setItem(row, col, QTableWidgetItem(str(self.professors_df.iat[row, col])))
    #agregado despuess
    def apply_classification_to_schedule(self):
        self.professors_df = data_transform.apply_classification_to_schedule(self.professors_df)
        self.display_professor_schedule()
    
    def display_professor_schedule(self):
        self.professors_table.setRowCount(self.professors_df.shape[0])
        self.professors_table.setColumnCount(self.professors_df.shape[1])
        self.professors_table.setHorizontalHeaderLabels(self.professors_df.columns)
        
        for row in range(self.professors_df.shape[0]):
            for col in range(self.professors_df.shape[1]):
                self.professors_table.setItem(row, col, QTableWidgetItem(str(self.professors_df.iat[row, col])))

#agregamos pestaña para horarios de TT tipo funcionaidad
    def load_tt_data(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo de trabajos terminales", "", "Excel Files (*.xlsx *.xls)")
        if file_path:
            self.tt_df = pd.read_excel(file_path)
            self.label.setText("Trabajos terminales cargados correctamente.")
            self.display_tt_schedule()
    
    def add_tt(self):
        new_tt = [
            self.tt_input.text(),
            self.name_input.text(),
            self.director1_input.text(),
            self.director2_input.text(),
            self.sinodal1_input.text(),
            self.sinodal2_input.text(),
            self.sinodal3_input.text()
        ]
        
        new_row = pd.DataFrame([new_tt], columns=["TT", "Nombre", "DIRECTOR 1", "DIRECTOR 2", "SINODAL 1", "SINODAL 2", "SINODAL 3"])
        self.tt_df = pd.concat([self.tt_df, new_row], ignore_index=True)
        self.display_tt_schedule()
        
        for input_field in [self.tt_input, self.name_input, self.director1_input, self.director2_input, self.sinodal1_input, self.sinodal2_input, self.sinodal3_input]:
            input_field.clear()
    
    def delete_tt(self):
        selected_row = self.tt_table.currentRow()
        if selected_row >= 0:
            self.tt_df.drop(index=selected_row, inplace=True)
            self.tt_df.reset_index(drop=True, inplace=True)
            self.display_tt_schedule()
    
    def display_tt_schedule(self):
        self.tt_table.setRowCount(self.tt_df.shape[0])
        self.tt_table.setColumnCount(self.tt_df.shape[1])
        self.tt_table.setHorizontalHeaderLabels(self.tt_df.columns)
        
        for row in range(self.tt_df.shape[0]):
            for col in range(self.tt_df.shape[1]):
                self.tt_table.setItem(row, col, QTableWidgetItem(str(self.tt_df.iat[row, col])))
    
    def initTTDaysTab(self):
        layout = QVBoxLayout()
        
        self.tt_days_table = QTableWidget()
        self.tt_days_table.setColumnCount(9)
        self.tt_days_table.setHorizontalHeaderLabels(["Inicio", "Fin", "8-10", "10-12", "12-2", "2-4", "4-6", "6-8", "Total TT"])
        layout.addWidget(self.tt_days_table)
        
        form_layout = QHBoxLayout()
        
        self.start_date_input = QDateEdit()
        self.start_date_input.setCalendarPopup(True)
        self.start_date_input.setDate(QDate.currentDate())
        form_layout.addWidget(self.start_date_input)
        
        self.end_date_input = QDateEdit()
        self.end_date_input.setCalendarPopup(True)
        self.end_date_input.setDate(QDate.currentDate().addDays(14))
        form_layout.addWidget(self.end_date_input)
        
        self.slots_inputs = []
        for _ in range(6):
            spinbox = QSpinBox()
            spinbox.setRange(0, 10)
            spinbox.setValue(10)
            form_layout.addWidget(spinbox)
            self.slots_inputs.append(spinbox)
        
        self.add_tt_day_button = QPushButton("Añadir Rango de Fechas")
        self.add_tt_day_button.clicked.connect(self.add_tt_day)
        form_layout.addWidget(self.add_tt_day_button)
        
        self.delete_tt_day_button = QPushButton("Eliminar Rango de Fechas")
        self.delete_tt_day_button.clicked.connect(self.delete_tt_day)
        form_layout.addWidget(self.delete_tt_day_button)
        
        layout.addLayout(form_layout)
        self.tt_days_tab.setLayout(layout)
    
    def add_tt_day(self):
        start_date = self.start_date_input.date().toString("dd MMM yyyy")
        end_date = self.end_date_input.date().toString("dd MMM yyyy")
        slots = [spinbox.value() for spinbox in self.slots_inputs]
        total_tt = sum(slots)
        
        new_row = pd.DataFrame([[start_date, end_date] + slots + [total_tt]], columns=["Inicio", "Fin", "8-10", "10-12", "12-2", "2-4", "4-6", "6-8", "Total TT"])
        self.tt_days_df = pd.concat([self.tt_days_df, new_row], ignore_index=True)
        self.display_tt_days()
        
    def delete_tt_day(self):
        selected_row = self.tt_days_table.currentRow()
        if selected_row >= 0:
            self.tt_days_df.drop(index=selected_row, inplace=True)
            self.tt_days_df.reset_index(drop=True, inplace=True)
            self.display_tt_days()
    
    def display_tt_days(self):
        self.tt_days_table.setRowCount(self.tt_days_df.shape[0])
        self.tt_days_table.setColumnCount(self.tt_days_df.shape[1])
        self.tt_days_table.setHorizontalHeaderLabels(self.tt_days_df.columns)
        
        for row in range(self.tt_days_df.shape[0]):
            for col in range(self.tt_days_df.shape[1]):
                self.tt_days_table.setItem(row, col, QTableWidgetItem(str(self.tt_days_df.iat[row, col])))

#logica core
    def initGeneratedScheduleTab(self):
        layout = QVBoxLayout()
        self.generated_schedule_table = QTableWidget()
        layout.addWidget(self.generated_schedule_table)
        self.generated_schedule_tab.setLayout(layout)
    
    def generate_tt_schedule(self):
        if hasattr(self, 'professors_df') and hasattr(self, 'tt_df') and not self.tt_days_df.empty:
            self.generated_schedule_df = generar_horarios_tt.generate_tt_schedule(self.professors_df, self.tt_df, self.tt_days_df)
            self.display_generated_schedule()
        else:
            self.label.setText("Faltan datos para generar el horario.")
    
    def display_generated_schedule(self):
        if self.generated_schedule_df is not None:
            self.generated_schedule_table.setRowCount(self.generated_schedule_df.shape[0])
            self.generated_schedule_table.setColumnCount(self.generated_schedule_df.shape[1])
            self.generated_schedule_table.setHorizontalHeaderLabels(self.generated_schedule_df.columns)
            
            for row in range(self.generated_schedule_df.shape[0]):
                for col in range(self.generated_schedule_df.shape[1]):
                    self.generated_schedule_table.setItem(row, col, QTableWidgetItem(str(self.generated_schedule_df.iat[row, col])))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScheduleApp()
    window.show()
    sys.exit(app.exec())

'''import sys
import pandas as pd
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QWidget, QLabel, QTableWidget, QTableWidgetItem, QTabWidget
import data_transform

class ScheduleApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Generador de Horarios de Trabajos Terminales")
        self.setGeometry(100, 100, 1000, 600)
        
        self.initUI()
    
    def initUI(self):
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        self.upload_tab = QWidget()
        self.schedule_tab = QWidget()
        
        self.tabs.addTab(self.upload_tab, "Carga de Datos")
        self.tabs.addTab(self.schedule_tab, "Horarios Profesores")
        
        self.initUploadTab()
        self.initScheduleTab()
    
    def initUploadTab(self):
        layout = QVBoxLayout()
        
        self.label = QLabel("Carga los archivos de datos:")
        layout.addWidget(self.label)
        
        self.load_professors_button = QPushButton("Cargar Horarios de Profesores")
        self.load_professors_button.clicked.connect(self.load_professor_schedule)
        layout.addWidget(self.load_professors_button)
        
        self.load_tt_button = QPushButton("Cargar Trabajos Terminales")
        self.load_tt_button.clicked.connect(self.load_tt_data)
        layout.addWidget(self.load_tt_button)
        
        self.generate_schedule_button = QPushButton("Generar Horarios")
        self.generate_schedule_button.clicked.connect(self.generate_schedule)
        layout.addWidget(self.generate_schedule_button)
        
        self.upload_tab.setLayout(layout)
    
    def initScheduleTab(self):
        layout = QVBoxLayout()
        
        self.professors_table = QTableWidget()
        layout.addWidget(self.professors_table)
        
        self.schedule_tab.setLayout(layout)
    
    def load_professor_schedule(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo de horarios de profesores", "", "Archivos CSV o Excel (*.csv *.xlsx *.xls)")
        if file_path:
            if file_path.endswith(".csv"):
                self.professors_df = pd.read_csv(file_path, encoding="utf-8")
            else:
                self.professors_df = pd.read_excel(file_path, encoding="utf-8", errors='replace')
            
            self.professors_df = data_transform.transform_professor_schedule(self.professors_df)
            self.label.setText("Horarios de profesores cargados y transformados correctamente.")
            self.display_professor_schedule()
    
    def load_tt_data(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo de trabajos terminales", "", "Excel Files (*.xlsx *.xls)")
        if file_path:
            self.tt_df = pd.read_excel(file_path)
            self.label.setText("Trabajos terminales cargados correctamente.")
    
    def generate_schedule(self):
        if hasattr(self, 'professors_df') and hasattr(self, 'tt_df'):
            self.label.setText("Generando horarios...")
            
            # Aquí se implementaría la lógica de asignación de horarios considerando restricciones
            result_df = pd.DataFrame({
                'ID TT': ["2025-A001"],
                'Director 1': ["RUBÉN PEREDO VALDERRAMA"],
                'D1': [True],
                'Director 2': ["#N/A"],
                'Sinodal 1': ["ELIZABETH MORENO GALVÁN"],
                'D3': [True],
                'Horario': ["8:00 a 10:00"],
                'Día': ["Martes 26 de noviembre"],
            })
            
            self.display_results(result_df)
        else:
            self.label.setText("Debes cargar ambos archivos primero.")
    
    def display_professor_schedule(self):
        self.professors_table.setRowCount(self.professors_df.shape[0])
        self.professors_table.setColumnCount(self.professors_df.shape[1])
        self.professors_table.setHorizontalHeaderLabels(self.professors_df.columns)
        
        for row in range(self.professors_df.shape[0]):
            for col in range(self.professors_df.shape[1]):
                self.professors_table.setItem(row, col, QTableWidgetItem(str(self.professors_df.iat[row, col])))

    def display_results(self, df):
        self.professors_table.setRowCount(df.shape[0])
        self.professors_table.setColumnCount(df.shape[1])
        self.professors_table.setHorizontalHeaderLabels(df.columns)
        
        for row in range(df.shape[0]):
            for col in range(df.shape[1]):
                self.professors_table.setItem(row, col, QTableWidgetItem(str(df.iat[row, col])))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScheduleApp()
    window.show()
    sys.exit(app.exec())
'''