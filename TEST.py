
import pandas as pd
import sqlite3
import os
chunksize = 1000
testdotcsv = r"C:\Users\JoaoPedro\Documents\BIGDirectory\InfoCircuitos\Fretes_Out2019_Jan2020.csv"
fields = ['FRTG_ID', 'ESCG_ID', '>_1_frete', 'ESCO_ID', 'RSDG_ID_PREVISTO',
       'RSDG_ID_REAL', 'ZL/JF', 'ORS_ID', 'LDES_ID', 'TOPV_ID',
       'ENT_ID_TRANSPORTE', 'UNI_ID', 'RSprev', 'RSreal', 'GrpReal',
       'Origem', 'Destino', 'Transporte',
       'Ft', 'Data', 'Dia_da_semana', 'Turno', 'Ano', 'Mes', 'Dia',
       'Hora',  'Peso', 'Uni', 'CRC_ID', 'Circuito', 'Tipo_CRC',
       'VIAT_ID', 'Viatura', 'Matricula', 'Capac',        
        'Frete_Rejeitado']
csv_name,_ = os.path.splitext(testdotcsv)
dbfile =  csv_name + ".db"
conn = sqlite3.connect(dbfile)

tablecursor = conn.cursor()
for chunk in pd.read_csv(testdotcsv, chunksize=chunksize,sep=";",encoding='cp860'):
    chunk.columns = chunk.columns.str.replace(' ', '_') #replacing spaces with underscores for column names
    chunk.to_sql(name="a", con=conn,if_exists="append")


conn = sqlite3.connect(testdotdb)
tablecursor = conn.cursor()
t = ("I0104",20)

tablecursor = conn.cursor()


fields = "Circuito,FRTG_ID,ESCG_ID,DIA,MES,ANO,HORA,DATA,PESO,FT"





tablecursor = conn.cursor()
tablecursor.execute( "SELECT SUM(Peso) FROM a WHERE Circuito='I0103' AND DIA='15' AND ANO='2020'" )
data = tablecursor.fetchall()
len(data)
print(data)


tablecursor = conn.cursor()
tablecursor.execute( "SELECT MAX(Ft) FROM a WHERE Circuito='I0103' AND DIA='15' AND ANO='2020'" )
data = tablecursor.fetchall()
len(data)
print(data)






pd.DataFrame((("a","a"),("b","b")))



csvfile = r"C:\Users\JoaoPedro\Documents\BIGDirectory\CIRCUITS\I0103\aliasCircuitVoyages\Processados\I0103_V2538_05_01_2020\ReportAnalysis\Appendable.csv"
stats = pd.read_csv(csvfile,sep=';',index_col=0)
import datetime

shiftfile = r"C:\Users\JoaoPedro\Documents\BIGDirectory\CIRCUITS\I0103\aliasCircuitVoyages\aliasDoNe\I0103_V2538_15_01_2020\ReportAnalysis\Appendable.csv"
shiftpd = pd.read_csv(shiftfile,sep=';',index_col=0)
shiftpd.columns
shiftpd['H_INICIO']
shiftpd['H_FIM']
circuito_string = shiftpd['CIRCUITO'].values[0]
datetime_inicio = string2datetime(shiftpd['H_INICIO'].values[0])
datetime_fim = string2datetime(shiftpd['H_FIM'].values[0])
string2datetime(shiftpd['H_FIM'].values[0])-string2datetime(shiftpd['H_INICIO'].values[0])
a=string2datetime(shiftpd['H_FIM'].values[0])-string2datetime(shiftpd['H_INICIO'].values[0])

fields=["Circuito","FRTG_ID","ESCG_ID","DIA","ANO","HORA","DATA","PESO","FT"]

tablecursor.execute( "SELECT "+','.join(fields)+" FROM a WHERE Circuito=? AND DIA=? AND ANO=?",(circuito_string,datetime_fim.day,datetime_fim.year))
data = tablecursor.fetchall()
len(data)
print(data)

data_row = data[1]
data_row[6]
minute = int(data_row[6].split(":")[1])
hour = int(data_row[6].split(":")[0])
day = int(data_row[3])
month = int(data_row[4])
year = int(data_row[5])
HORAS=datetime.datetime(year,month,day,hour,minute)

elapsedtimebetweenunlaodingandending = string2datetime(shiftpd['H_FIM'].values[0]) - HORAS





meanfields=[ 'CARREGADO (kg)','TEMPO_TOTAL (h)', 'DIST_TOTAL (km)', 'NR_VISITADOS', '%_VISITADOS',
       'NR_IGNORADOS', '%_IGNORADOS', 'TEMP_GARAGEM (h)',
       'DIST_GARAGEM (km)', 'VELOCIDADE_GARAGEM (km/h)',
       'TEMP_DESCARGA (h)', 'DIST_DESCARGA (km)',
       'VELOCIDADE_DESCARGA (km/h)', 'TEMP_RECOLHA (h)',
       'DIST_RECOLHA (km)', 'VELOCIDADE_RECOLHA (km/h)', 'TEMP_LIGACAO (h)',
       'DIST_LIGACAO (km)', 'VELOCIDADE_LIGACAO (km/h)', 'TEMP_OUTROS (h)',
       'DIST_OUTROS (km)']



#class MyPrompt(Cmd):
#    prompt = 'pb> '
#    espaco = "\t\t\t\t\t\t\t"
#    intro = espaco+"\n\n Bem Vindo! Introduza ? para ver os comandos disponiveis \n\n"

#    def preloop(self):
#        self.do_insertPath() 

#    def do_exit(self, inp):
#        print("Bye")
#        return True

#    def help_exit(self):
#        print('exit the application. Shorthand: x q Ctrl-D.') 
    



#    def do_insertPath(self):
#        path = input("Introduza o caminho: \n")
#        self.AS = AncientStructural(path)

#    def help_insertPath(self):
#        print('Insert the path for the starter')




#    def do_replaceAllKmls(self):
#        self.AS.replace_AllKmls()

#    def help_replaceAllKmls(self):
#        print('Redireccionar ficheiros dos percursos .kml')





#    def do_showAllCircuits(self,inp):
#        self.circuit_list = self.AS.get_AllCircuits()
#        for circuit in self.circuit_list:
#            print(os.path.basename(circuit))

#    def help_showAllCircuit(self):
#        print('Insert the path for the starter folder and shows all the created circuits')


#    def do_processSingleCircuit(self,inp):
#        self.do_showAllCircuits(self,inp)
#        circuit_folder = r"C:\Users\JoaoPedro\Documents\BIGDirectory\CIRCUITS\I0103"
#        circuit = CD.CircuitDir(circuit_folder)
 
#    def default(self, inp):
#        if inp == 'x' or inp == 'q':
#            return self.do_exit(inp)
 
 
#    do_EOF = do_exit
#    help_EOF = help_exit
 