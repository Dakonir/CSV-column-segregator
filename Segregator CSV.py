# -*- coding: utf-8 -*-
import pandas as pd
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename, Toplevel
from tkinter import ttk

input_path = ""  # ścieżka do pliku wejściowego
output_path = "" # ścieżka do pliku wyjściowego
label = ""
separator = ";"
Kolumna_Sortowanie = "EAN"

#Funkcja na wykrywanie separatora 
def wykryj_separator(plik_wyjsciowy):
    global czytaj_csv
    global kolumn
    separators = [",",";","\t",":"," "]
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
    input_path = askopenfilename(
        filetypes=[("Excel or CSV files", "*.xls *.xlsx *.csv"),("Excel files", "*.xls *.xlsx"),("CSV files", "*.csv"), ("All files", "*.*")]
    )
    print(input_path)
    if ".csv" in input_path or ".xls" in input_path:
        print("Plik Poprawny")
        
    else:
        input_path=""
        print("Niepoprawny Format Pliku")
        top = tk.Toplevel()
        top.title("Błąd")
        label = tk.Label(top, text="Niepoprawny format pliku")
        label.grid(column=0, row=0, padx=20, pady=20)
    if ".xls" in input_path:
        data_time = pd.read_excel(input_path, index_col=None)
        data_time.columns.values.tolist()
    elif ".csv" in input_path:
        wykryj_separator(input_path)
def zapisz_plik():
    global output_path
    if input_path != "":
        file_list= input_path.split("/")
        file_list= file_list[-1].split(".")
        filename = file_list[0]
        print(input_path)
    else:
        filename=""
    output_path = asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        initialfile = filename 
    )

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
        ilosc=("ilosc", "sum")
    ).reset_index()

    summary.to_csv(output_path, index=False, encoding='utf-8-sig', sep=';', decimal=',')
#Sortowanie i Agregacja 
def wykonaj_zapis():
    if input_path and output_path:
        przetworz_dane(input_path, output_path)
        print(kolumn)
        print("Plik Wykonany")
    else:
        print("Upewnij się, że wybrano plik wejściowy i miejsce zapisu.")
        top = tk.Toplevel()
        top.title("Błąd")
        label = tk.Label(top, text="Upewnij się, że wybrano plik wejściowy i miejsce zapisu.")
        label.grid(column=0, row=0, padx=20, pady=20)
        
# GUI
root = tk.Tk()
root.title("Przetwarzanie danych Excel do CSV")
frm = ttk.Frame(root, padding=20)
frm.grid()
# Przycisk funkcji wybierz plik
ttk.Label(frm, text="1. Wybierz plik Excel").grid(column=0, row=0, padx=10, pady=10)
ttk.Button(frm, text="Wybierz", command=wybierz_plik).grid(column=1, row=0)
#Przycisk funkcji zapisz plik
ttk.Label(frm, text="2. Wybierz gdzie zapisać CSV").grid(column=0, row=1, padx=10, pady=10)
ttk.Button(frm, text="Zapisz jako...", command=zapisz_plik).grid(column=1, row=1)
#Przycisk funkcji wykonaj zapis
ttk.Button(frm, text="3. Przetwórz i Zapisz", command=wykonaj_zapis).grid(column=0, row=2, pady=20)
ttk.Button(frm, text="Wyjdź", command=root.destroy).grid(column=1, row=2)

root.mainloop()