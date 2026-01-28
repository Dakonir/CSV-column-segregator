# -*- coding: utf-8 -*-
import pandas as pd
import sys 
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow,QPushButton, QFileDialog,QVBoxLayout

input_path = ""  # ścieżka do pliku wejściowego
output_path = "" # ścieżka do pliku wyjściowego
kolumn = []
kolumnaBezSeparatora = []
kolumna_sortowanie = ""
mapaAgregowania = {}
listaAgregacji = ["Pomiń","sum","first","mean","max","min"]
guiWidth = 350
guiHeight = 300
labelMenuText = "Witaj w Segregatorze Plików CSV"
labelButton1Text = "1.Wybierz plik Excel lub csv"
LabelButton2Text = "2.Wybierz gdzie zapisać CSV"
button3Text = "4.Przetwórz i Zapisz"

#Klasa GUI
class myWindow(QMainWindow):
    def __init__(self):
        super(myWindow,self).__init__()
        self.setGeometry(750,400,guiWidth,guiHeight)
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
            self.button3.hide()            
        
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
        print(kolumna_sortowanie)
        print(mapaAgregowania)
        wykonaj_zapis()
    def processFunction(self):
        global kolumna_sortowanie
        global kolumnaBezSeparatora
        if len(kolumn) != 0:
            kolumna_sortowanie = kolumn[self.wybierzSeperator.currentIndex()]
            kolumnaBezSeparatora = deepCopy(kolumn)
            kolumnaBezSeparatora.pop(self.wybierzSeperator.currentIndex())
            print(kolumnaBezSeparatora)
            print(kolumn)
            self.dialog = aggregationWindow()
            self.dialog.show()
        self.button3.show()
    
class aggregationWindow(QMainWindow):
    def __init__(self):
        super(aggregationWindow,self).__init__()
        self.setGeometry(750,400,guiWidth,guiHeight)
        self.setWindowTitle("Agreguj plik")
        self.initUIAggregation()
    def initUIAggregation(self):
        self.labelMenu = QtWidgets.QLabel(self)
        self.labelMenu.setText("Witaj w Agregatorze Plików CSV")
        self.labelMenu.adjustSize()
        self.labelMenu.move(65,5)
        
        self.labelWybierzSeparator = QtWidgets.QLabel(self)
        self.labelWybierzSeparator.setText("Wybierz kolumnę według której odbędzię sie segregacja")
        self.labelWybierzSeparator.adjustSize()
        self.labelWybierzSeparator.move(25,38)
        
        self.wybierzAgregator1 = QtWidgets.QComboBox(self)
        self.wybierzAgregator1.addItems(kolumnaBezSeparatora)
        self.wybierzAgregator1.adjustSize()
        self.wybierzAgregator1.move(75,68)
        
        self.wybierzAgregacje1 = QtWidgets.QComboBox(self)
        self.wybierzAgregacje1.addItems(listaAgregacji)
        self.wybierzAgregacje1.adjustSize()
        self.wybierzAgregacje1.move(150,68)
        
        self.wybierzAgregator2 = QtWidgets.QComboBox(self)
        self.wybierzAgregator2.addItems(kolumnaBezSeparatora)
        self.wybierzAgregator2.adjustSize()
        self.wybierzAgregator2.move(75,98)
        
        self.wybierzAgregacje2 = QtWidgets.QComboBox(self)
        self.wybierzAgregacje2.addItems(listaAgregacji)
        self.wybierzAgregacje2.adjustSize()
        self.wybierzAgregacje2.move(150,98)
        
        self.wybierzAgregator3 = QtWidgets.QComboBox(self)
        self.wybierzAgregator3.addItems(kolumnaBezSeparatora)
        self.wybierzAgregator3.adjustSize()
        self.wybierzAgregator3.move(75,128)
        
        self.wybierzAgregacje3 = QtWidgets.QComboBox(self)
        self.wybierzAgregacje3.addItems(listaAgregacji)
        self.wybierzAgregacje3.adjustSize()
        self.wybierzAgregacje3.move(150,128)
        
        self.wybierzAgregator4 = QtWidgets.QComboBox(self)
        self.wybierzAgregator4.addItems(kolumnaBezSeparatora)
        self.wybierzAgregator4.adjustSize()
        self.wybierzAgregator4.move(75,158)
        
        self.wybierzAgregacje4 = QtWidgets.QComboBox(self)
        self.wybierzAgregacje4.addItems(listaAgregacji)
        self.wybierzAgregacje4.adjustSize()
        self.wybierzAgregacje4.move(150,158)
        
        self.wybierzAgregator5 = QtWidgets.QComboBox(self)
        self.wybierzAgregator5.addItems(kolumnaBezSeparatora)
        self.wybierzAgregator5.adjustSize()
        self.wybierzAgregator5.move(75,188)
        
        self.wybierzAgregacje5 = QtWidgets.QComboBox(self)
        self.wybierzAgregacje5.addItems(listaAgregacji)
        self.wybierzAgregacje5.adjustSize()
        self.wybierzAgregacje5.move(150,188)
        
        self.button1 = QPushButton(self)
        self.button1.setText("Wybierz")
        self.button1.adjustSize()
        self.button1.move(120,215)
        self.button1.clicked.connect(self.processFunction)
    
    def processFunction(self):
        global kolumna_sortowanie
        i = 0
        agregator1 = kolumnaBezSeparatora[self.wybierzAgregator1.currentIndex()]
        aggregacja1 = listaAgregacji[self.wybierzAgregacje1.currentIndex()]
        agregator2 = kolumnaBezSeparatora[self.wybierzAgregator2.currentIndex()]
        aggregacja2 = listaAgregacji[self.wybierzAgregacje2.currentIndex()]
        agregator3 = kolumnaBezSeparatora[self.wybierzAgregator3.currentIndex()]
        aggregacja3 = listaAgregacji[self.wybierzAgregacje3.currentIndex()]
        agregator4 = kolumnaBezSeparatora[self.wybierzAgregator4.currentIndex()]
        aggregacja4 = listaAgregacji[self.wybierzAgregacje4.currentIndex()]
        agregator5 = kolumnaBezSeparatora[self.wybierzAgregator5.currentIndex()]
        aggregacja5 = listaAgregacji[self.wybierzAgregacje5.currentIndex()]
        agregatory = [agregator1,agregator2,agregator3,agregator4,agregator5]
        agregacje = [aggregacja1,aggregacja2,aggregacja3,aggregacja4,aggregacja5]
        while i < len(agregatory):
            stworzenieMapyAgregacji(agregatory[i],agregacje[i])
            i = i + 1
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
        print(kolumn)
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
        print(kolumn)
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
    print(mapaAgregowania)
    print(kolumna_sortowanie)
    summary = czytaj_csv.groupby(kolumna_sortowanie).agg(
        mapaAgregowania
    ).reset_index()

    summary.to_csv(output_path, index=False, encoding='utf-8-sig', sep=';', decimal=',')
#funkcja łącząca  
def wykonaj_zapis():
    if input_path != "" and output_path != "":
        przetworz_dane(input_path, output_path)
        print(kolumn)
        print("Plik Wykonany")
        return True
    else:
        print("Upewnij się, że wybrano plik wejściowy i miejsce zapisu.")
        return False 
def stworzenieMapyAgregacji(wybranaKolumna,funkcjaAggregacji):
    global mapaAgregowania
    if funkcjaAggregacji == listaAgregacji[0] :
        return
    elif funkcjaAggregacji == "mean":
        czytaj_csv[wybranaKolumna] = czytaj_csv[wybranaKolumna].astype(str).str.replace(',', '.').str.replace(r'[^0-9\.-]', '', regex=True)
        czytaj_csv[wybranaKolumna] = pd.to_numeric(czytaj_csv[wybranaKolumna], errors="coerce")
        mapaAgregowania.update({wybranaKolumna:funkcjaAggregacji})
    else:
        mapaAgregowania.update({wybranaKolumna:funkcjaAggregacji})
def deepCopy(L):
    ret = []
    if isinstance(L, list):
        for i in L:
            ret.append(deepCopy(i))
    elif isinstance(L,(int, float, type(None),str,bool)):
        ret = L
    else:
        raise ValueError("Niespodziewany typ dla funkcji deepCopy ")
    return ret
# włączenie gui
def window():
    app = QApplication(sys.argv)
    app.setStyleSheet("QLabel{font-size: 9pt;}")
    win = myWindow()
    win.show()
    sys.exit(app.exec_())
if __name__ == "__main__":
    window() 
