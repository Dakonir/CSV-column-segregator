# -*- coding: utf-8 -*-
import pandas as pd
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename, Toplevel
from tkinter import ttk
import sys 
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow,QPushButton, QFileDialog

input_path = ""  # ścieżka do pliku wejściowego
output_path = "" # ścieżka do pliku wyjściowego
label = ""
separator = ";"
Kolumna_Sortowanie = ""
MapaAgregowania = {}
#Klasa GUI
class myWindow(QMainWindow):
    def __init__(self):
        super(myWindow,self).__init__()
        self.setGeometry(750,400,300,200)
        self.setWindowTitle("Agregacja Pliku CSV")
        self.initUI()
        
    def initUI(self):
        self.labelMenu = QtWidgets.QLabel(self)
        self.labelMenu.setText("Witaj Segregatorze Plików CSV")
        self.labelMenu.adjustSize()
        self.labelMenu.move(65,5)
            
        self.labelButton1 = QtWidgets.QLabel(self)
        self.labelButton1.setText("1. Wybierz plik Excel lub csv")
        self.labelButton1.adjustSize()
        self.labelButton1.move(25,38)
        
        self.labelButton2 = QtWidgets.QLabel(self)
        self.labelButton2.setText("2. Wybierz gdzie zapisać CSV")
        self.labelButton2.adjustSize()
        self.labelButton2.move(25,78)
            
        self.button1 = QPushButton(self)
        self.button1.setText("Wybierz")
        self.button1.adjustSize()
        self.button1.move(185,35)
        self.button1.clicked.connect(self.chooseFunction)
        
        self.button2 = QPushButton(self)
        self.button2.setText("Zapisz jako")
        self.button2.adjustSize()
        self.button2.move(185,75)
        self.button2.clicked.connect(self.saveFunction)
        
        self.button3 = QPushButton(self)
        self.button3.setText("3. Przetwórz i Zapisz")
        self.button3.adjustSize()
        self.button3.move(75,115)
        self.button3.clicked.connect(self.processFunction)
        
    def chooseFunction(self):
        if wybierz_plik() == True:
            self.labelButton1.setText("1.Wybrałes plik CSV")
        elif wybierz_plik == False:
            self.labelButton1.setText("1.Błędny plik")
        self.labelButton1.adjustSize()
        return
    def saveFunction(self):
        self.labelButton2.setText("2.Wybrałes gdzie zapisać plik CSV")
        zapisz_plik()
        self.labelButton2.adjustSize()
        self.button2.adjustSize()
    def processFunction(self):
        if wykonaj_zapis() == True:
            self.button3.setText("3. Plik Przetworzony i Zapisany")
        elif wykonaj_zapis() == False:
            self.button3.setText("3. Wybierz plik i miejsce zapisu")
        self.button3.adjustSize()   
        
#Funkcja na wykrywanie separatora 
def wykryj_separator(plik_wyjsciowy):
    global czytaj_csv
    global kolumn
    separators = [";","\t",":",','," "]
    i = 0
    czytaj_csv = pd.read_csv(
        plik_wyjsciowy,
        sep=separators[0],
        decimal=",",
        on_bad_lines="warn"
                             )
    kolumn = czytaj_csv.columns.values.tolist()
    try:
        kolumn[1]
    except IndexError :
        print("Szukam Separatora")
        checker = False
        i = 0
        while checker == False:
            if i >= len(separators):
                print("Separator nie jest obejmowany przez baze")
                break
            check = kolumn[0].split(separators[i])
            try:
                check[1]
            except IndexError:
                print("Nie ten Separator")
            else:
                czytaj_csv = pd.read_csv(
                      plik_wyjsciowy,
                      decimal=",",
                      sep = separators[i],
                      on_bad_lines="warn"      
                      )
                kolumn = czytaj_csv.columns.values.tolist()
                print(kolumn)
                checker = True
            i = i+1
    else:
        print("ok")
    return kolumn 
def wybierz_plik():
    global input_path
    full_input_path = QFileDialog.getOpenFileName(myWindow(),"XML or CSV File (*.csv *.xls *.xlsx)")
    if full_input_path == ("",""):
        print("canceled")
        return False
    else:
        input_path = full_input_path[0]
    if ".csv" in input_path or ".xls" in input_path:
        print("Plik Poprawny")
        
    else:
        input_path=""
        return False
    if ".xls" in input_path:
        data_time = pd.read_excel(input_path, index_col=None)
        data_time.columns.values.tolist()
        return True
    elif ".csv" in input_path:
        wykryj_separator(input_path)
        return True
def zapisz_plik():
    global output_path
    if input_path != "":
        file_list= input_path.split("/")
        file_list= file_list[-1].split(".")
        filename = file_list[0]
    else:
        filename=""
    full_output_path = QFileDialog.getSaveFileName(myWindow(),'Save File', filename, "Plik CSV (*.csv)")
    output_path = full_output_path[0]
def przetworz_dane(input_path: str, output_path: str):
#Wykrywanie rozszerzenia i odpowiednie przypisanie parametrów pliku
    print(input_path)    
    if ".xls" in input_path or ".xlsx" in input_path:
        data_xls = pd.read_excel(input_path, index_col=None)
        data_xls.to_csv(output_path, encoding='utf-8', index=False, sep=';')
        wykryj_separator(input_path)
    elif ".xls" in input_path or ".xlsx" in input_path or ".csv" in input_path :
        print("Poprawny Format Pliku")
    else:
        print("Niepoprawny Format Pliku")
        top = tk.Toplevel()
        top.title("Błąd")
        label = tk.Label(top, text="Niepoprawny format pliku")
        label.grid(column=0, row=0, padx=20, pady=20)
    summary = czytaj_csv.groupby(Kolumna_Sortowanie).agg(
        ilosc=("ILOŚĆ", "sum")
    ).reset_index()

    summary.to_csv(output_path, index=False, encoding='utf-8-sig', sep=';', decimal=',')
#Sortowanie i Agregacja 
def wykonaj_zapis():
    if input_path and output_path:
        przetworz_dane(input_path, output_path)
        print(kolumn)
        print("Plik Wykonany")
        return True
    else:
        print("Upewnij się, że wybrano plik wejściowy i miejsce zapisu.")
        return False 
# GUI
def window():
    app = QApplication(sys.argv)
    app.setStyleSheet("QLabel{font-size: 9pt;}")
    win = myWindow()
    win.show()
    sys.exit(app.exec_())
window() 
