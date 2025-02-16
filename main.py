import sys
import pandas as pd
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QWidget, QLabel, QTableWidget, QTableWidgetItem, QTabWidget, QLineEdit, QHBoxLayout, QComboBox
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
        self.schedule_tab.setLayout(layout)
    
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