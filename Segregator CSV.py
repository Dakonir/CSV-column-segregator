# -*- coding: utf-8 -*-
import pandas as pd
import sys 
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow,QPushButton, QFileDialog,QVBoxLayout

input_path = ""  # ścieżka do pliku wejściowego
output_path = "" # ścieżka do pliku wyjściowego
label = ""
kolumn = []
separator = ";"
kolumna_sortowanie = ""
mapaAgregowania = {"1":"first"}
gui_width = 350
gui_height = 300

labelMenuText = "Witaj w Segregatorze Plików CSV"
labelButton1Text = "1.Wybierz plik Excel lub csv"
LabelButton2Text = "2.Wybierz gdzie zapisać CSV"
button3Text = "4.Przetwórz i Zapisz"

#Klasa GUI
class myWindow(QMainWindow):
    def __init__(self):
        super(myWindow,self).__init__()
        self.setGeometry(750,400,gui_width,gui_height)
        self.setWindowTitle("Agregacja Pliku CSV")
        self.initUI()
        
    def initUI(self):
        self.labelMenu = QtWidgets.QLabel(self)
        self.labelMenu.setText(labelMenuText)
        self.labelMenu.adjustSize()
        self.labelMenu.move(65,5)
            
        self.labelButton1 = QtWidgets.QLabel(self)
        self.labelButton1.setText(labelButton1Text)
        self.labelButton1.adjustSize()
        self.labelButton1.move(25,38)
        
        self.labelButton2 = QtWidgets.QLabel(self)
        self.labelButton2.setText(LabelButton2Text)
        self.labelButton2.adjustSize()
        self.labelButton2.move(25,78)
            
        self.button1 = QPushButton(self)
        self.button1.setText("Wybierz Plik")
        self.button1.adjustSize()
        self.button1.move(185,35)
        self.button1.clicked.connect(self.chooseFunction)
        
        self.button2 = QPushButton(self)
        self.button2.setText("Zapisz jako")
        self.button2.adjustSize()
        self.button2.move(185,75)
        self.button2.clicked.connect(self.saveFunction)
        
        self.button3 = QPushButton(self)
        self.button3.setText(button3Text)
        self.button3.move(75,195)
        self.button3.adjustSize()
        self.button3.clicked.connect(self.aggregateFunction)
        
        self.labelWybierzSeparator = QtWidgets.QLabel(self)
        self.labelWybierzSeparator.setText("3.Kolumna według której odbędzię sie segregacja")
        self.labelWybierzSeparator.adjustSize()
        self.labelWybierzSeparator.move(25,110)
        
        self.wybierzSeperator = QtWidgets.QComboBox(self)
        self.wybierzSeperator.adjustSize()
        self.wybierzSeperator.move(40,137)
        
        self.button4 = QPushButton(self)
        self.button4.setText("Wybierz i dostosuje agregacje")
        self.button4.adjustSize()
        self.button4.move(135,135)
        self.button4.clicked.connect(self.processFunction)
        if len(kolumn) ==0:
            self.button4.hide()
            self.wybierzSeperator.hide()
            self.labelWybierzSeparator.hide()            
        
    def chooseFunction(self):
        correctFileExtension = wybierz_plik()
        if correctFileExtension == True:
            self.labelButton1.setText("1.Poprawnie Wybrano plik csv/xls")
            self.wybierzSeperator.addItems(kolumn)
            self.button4.show()
            self.wybierzSeperator.show()
            self.labelWybierzSeparator.show()
        elif correctFileExtension == False:
            self.labelButton1.setText("1.Rozszerzenie Pliku nieprawidłowe")
        self.labelButton1.adjustSize()
        return
    def saveFunction(self):
        correctSavePath = zapisz_plik()
        if correctSavePath == True:
            self.labelButton2.setText("2.Wybrałes gdzie zapisać plik CSV")
        elif correctSavePath == False:
            self.labelButton2.setText("2.Nie wybrałes gdzie zapisać plik CSV")
        self.labelButton2.adjustSize()
        self.button2.adjustSize()  
    def aggregateFunction(self):
        self.button3.setText("In progress")
        global kolumna_sortowanie
        if len(kolumn) != 0:
            kolumna_sortowanie = kolumn[self.wybierzSeperator.currentIndex()]
        wykonaj_zapis()
    def processFunction(self):
        global kolumna_sortowanie
        if len(kolumn) != 0:
            kolumna_sortowanie = kolumn[self.wybierzSeperator.currentIndex()]
    
class aggregationWindow(QMainWindow):
    def __init__(self):
        super(aggregationWindow,self).__init__()
        self.setGeometry(750,400,300,200)
        self.setWindowTitle("Agreguj plik")
        self.initUIAggregation()
    def initUIAggregation(self):
        self.labelMenu = QtWidgets.QLabel(self)
        self.labelMenu.setText("Witaj Segregatorze Plików CSV")
        self.labelMenu.adjustSize()
        self.labelMenu.move(70,5)
        
        self.labelWybierzSeparator = QtWidgets.QLabel(self)
        self.labelWybierzSeparator.setText("Wybierz kolumnę według której odbędzię sie segregacja")
        self.labelWybierzSeparator.adjustSize()
        self.labelWybierzSeparator.move(5,58)
        
        self.wybierzSeperator = QtWidgets.QComboBox(self)
        self.wybierzSeperator.addItems(kolumn)
        self.wybierzSeperator.adjustSize()
        self.wybierzSeperator.move(75,78)
        
        self.button1 = QPushButton(self)
        self.button1.setText("Wybierz")
        self.button1.adjustSize()
        self.button1.move(120,115)
        self.button1.clicked.connect(self.processFunction)
        
    def processFunction(self):
        global kolumna_sortowanie
        if len(kolumn) != 0:
            kolumna_sortowanie = kolumn[self.wybierzSeperator.currentIndex()]
        print(kolumna_sortowanie)
        self.close()
        
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
    global kolumn
    full_input_path = QFileDialog.getOpenFileName(myWindow(),"Wybierz Plik csv lub xls","","XML or CSV File (*.csv *.xls *.xlsx)")
    if full_input_path == ("",""):
        print("canceled")
        return False
    else:
        input_path = full_input_path[0]
    if ".csv" in input_path or ".xls" in input_path:
        print("Plik Poprawny")
    if ".xls" in input_path or ".xlxs" in input_path:
        data_time = pd.read_excel(input_path, index_col=None)
        kolumn = data_time.columns.values.tolist()
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
    if full_output_path == ("",""):
        return False
    else:
        output_path = full_output_path[0]
        return True
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
    summary = czytaj_csv.groupby(kolumna_sortowanie).agg(
        mapaAgregowania
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
# włączenie gui
def window():
    app = QApplication(sys.argv)
    app.setStyleSheet("QLabel{font-size: 9pt;}")
    win = myWindow()
    win.show()
    sys.exit(app.exec_())
if __name__ == "__main__":
    window() 
