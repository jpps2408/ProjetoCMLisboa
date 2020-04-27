from DictionaryInstantiator import *
from ostools import *
from DirectoryExlorer import *
from ShiftDirClass import ShiftDir
from db_creator import db_creator
from ostools import *
class AncientStructural(object):


    def __init__(self,masterdirectory,*args,**kwargs):
        self.masterdirectory = os.path.abspath(masterdirectory)
        self.pardir = os.path.join(masterdirectory,os.pardir)
        self.setHandlerPaths()


    def setHandlerPaths(self):
        MASTERJSONDIR = {
        ########Layer 0 #########
        "namestandard": "MainDirectory",
        "alias": os.path.basename(self.masterdirectory),
        "filesystem": {"ancilliarydata.json":"infotrips.json"},
        "children" :
         ########BEGIN Layer 1 #########
        [
                {"namestandard": "InfoCircuitos",
                "alias": "InfoCircuitos",
                "filesystem": None,
                "children" : None},

                {"namestandard": "InfoTripsFiles",
                "alias": "InfoTripsFiles",
                "filesystem": {"Estats_Circuitos.csv":"Estats_Circuitos.csv"},
                "children" : None},

                {"namestandard": "Kmls",
                "alias": "PERCURSOS",
                "filesystem": None,
                "children" : None},

               {"namestandard": "Circuits",
                "alias": "CIRCUITS",
                "filesystem": None,
                "children" : None}]
        }
        
        HandlerPathsobject = DictionaryExplorer(self.pardir)
        self.HandlerPaths = HandlerPathsobject.recursive_dictglobalexplorer(MASTERJSONDIR)


    def get_AllCircuits(self):
        path = self.HandlerPaths['MainDirectory']['Circuits']['path']
        return [os.path.join(path,round) for round in os.listdir(path)]


    def get_AllKmls(self):
        path = self.HandlerPaths['MainDirectory']['Kmls']['path']
        return [os.path.join(path,round) for round in os.listdir(path)]


    def get_AllDatabaseFiles(self):
        path = self.HandlerPaths['MainDirectory']['InfoCircuitos']['path']
        return [os.path.join(path,round) for round in os.listdir(path)]


    @timer
    def retrieve_AllKmls(self):
        #create a dictionary to hold ShiftDir Objects
        shiftdir_dict ={}
        paths = self.get_AllKmls()
        for origfile in paths:
            shiftpart,_ = os.path.splitext(os.path.basename(origfile))
            splitstringlist = shiftpart.split("_")
            circuitpath= os.path.join(self.HandlerPaths['MainDirectory']['Circuits']['path'],splitstringlist[0])
            if not circuitpath in shiftdir_dict.keys():
                circuithandler = CircuitDir(circuitpath)
                shiftdir_dict[circuitpath] = circuithandler
            circuitdir_inst = shiftdir_dict[circuitpath]
            shiftpardir = circuitdir_inst.circuitpathdicts["CircuitName"]["CircuitVoyages"]["DoNe"]["path"]
            if len(splitstringlist)>5:
                shiftfull = "_".join(splitstringlist[0:5])
            else:
                shiftfull = shiftpart
            shiftpath = os.path.join(shiftpardir,shiftfull)
            if not shiftpath in shiftdir_dict.keys():
                shifthandler = ShiftDir(shiftpath,circuithandler)
                shiftdir_dict[shiftpath] = shifthandler
            shiftdir_inst = shiftdir_dict[shiftpath] 
            movedfile = os.path.join(shiftdir_inst.shiftpaths["ShiftName"]["KML"]["path"],shiftpart + _)
            try:
                os.rename(origfile,movedfile)
            except:
                print("The file {} already exists".format(os.path.basename(movedfile)))
                pass


    @timer 
    def run_dbcamara(self):
        databasefiles = getfilesinpath(self.HandlerPaths['MainDirectory']['InfoCircuitos']['path'],".csv")
        dict_csv_dbobject ={}
        for csvfile in databasefiles:
            dict_csv_dbobject[csvfile] = db_creator(csvfile,1000)
        self.dbobject = dict_csv_dbobject[csvfile]
        self.dict_csv_dbobject = dict_csv_dbobject

    
    @timer
    def place_inFilled(self,shift):
        src = shift.shiftpaths['ShiftName']['path']
        dst = shift.circuitobject.circuitpathdicts['CircuitName']["CircuitVoyages"]['Filled']['path']
        copyandremove_directory(src,dst)  

    @timer
    def finalize_shift(self,shift,db):
        row = pd.read_csv(shift.shiftpaths["ShiftName"]["ReportAnalysis"]["filepathdicts"]["Appendable.csv"],sep=';')
        Columns = [shift.Fields_Display[key] for key in shift.order]

        datetime_inicio = string2datetime(row['H_INICIO'].values[0])
        datetime_fim = string2datetime(row['H_FIM'].values[0])
        elapsedtime_ini_fim=datetime_fim-datetime_inicio

        fields=["Circuito","DIA","ANO","HORA","DATA","PESO","FT"]
        query = "SELECT "+','.join(fields)+" FROM a WHERE Circuito=? AND DIA=? AND MES=? AND ANO=?"
        querytuple = (row['CIRCUITO'].values[0],datetime_fim.day,datetime_fim.month,datetime_fim.year)
        row_tuples = db.query_db(query,querytuple)

        apd = pd.DataFrame(list(row_tuples),columns = ["Circuito","DIA","ANO","HORA","DATA","PESO","FT"])
        row[shift.Fields_Display["TOTAL_WEIGHT"]] = apd["PESO"].sum()
        row[shift.Fields_Display["NR_TRIPS"]] = apd["FT"].max()
        row = row[Columns]
        row[Columns].to_csv(shift.shiftpaths["ShiftName"]["ReportAnalysis"]["filepathdicts"]["Appendable.csv"],sep=';')
        shift.circuitobject.write_to_reports(row)


    @timer
    def aggregate_summaries(self):
        circuit_list = self.get_AllCircuits()
        circuit_folder = circuit_list[0]
        all_circuits_csv = self.HandlerPaths["MainDirectory"]["InfoTripsFiles"]["filepathdicts"]["Estats_Circuitos.csv"]
        self.create_single_summary(all_circuits_csv,circuit_folder)
        
        for circuit_folder in circuit_list[1:]:
            self.add_single_summary(all_circuits_csv,circuit_folder)
    

    @signal
    def create_single_summary(self,all_circuits_csv,circuit_folder):
        circuit = CircuitDir(circuit_folder)
        circuit.write_summaries()
        single_circuit_csv = circuit.circuitpathdicts['CircuitName']["Reports"]["filepathdicts"]["Resumos.csv"]
        single_circuit_pd = pd.read_csv(single_circuit_csv,sep=";",index_col=0)
        single_circuit_pd.to_csv(all_circuits_csv,sep=";",mode='wb', header=True)
    

    @signal
    def add_single_summary(self,all_circuits_csv,circuit_folder):
        circuit = CircuitDir(circuit_folder)
        circuit.write_summaries()
        single_circuit_csv = circuit.circuitpathdicts['CircuitName']["Reports"]["filepathdicts"]["Resumos.csv"]
        single_circuit_pd = pd.read_csv(single_circuit_csv,sep=";",index_col=0)
        single_circuit_pd.to_csv(all_circuits_csv,mode='ab', header=False,sep=";")