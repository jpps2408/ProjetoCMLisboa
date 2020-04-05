


INI_SERIAL_list_copy.reverse()
aux_classification.reverse()
i=0
while INI_SERIAL_list_copy[i] != 2460:
    aux_classification[i] = "final"
    i+=1
INI_SERIAL_list_copy.reverse()
aux_classification.reverse()



TIMESTAMP_SERIAL_LIST = [datetime.datetime(2020, 1, 7, 22, 46, 6), datetime.datetime(2020, 1, 7, 23, 10, 13), 
                         datetime.datetime(2020, 1, 7, 23, 26, 26), datetime.datetime(2020, 1, 7, 23, 27, 25),
                        datetime.datetime(2020, 1, 7, 23, 27, 45), datetime.datetime(2020, 1, 8, 0, 18, 32), 
                        datetime.datetime(2020, 1, 8, 0, 24, 4), datetime.datetime(2020, 1, 8, 0, 36, 52),
                       datetime.datetime(2020, 1, 8, 0, 39, 7), datetime.datetime(2020, 1, 8, 0, 39, 12), 
                       datetime.datetime(2020, 1, 8, 0, 39, 13), datetime.datetime(2020, 1, 8, 0, 49, 30), 
                       datetime.datetime(2020, 1, 8, 0, 49, 35), datetime.datetime(2020, 1, 8, 0, 49, 40), 
                       datetime.datetime(2020, 1, 8, 0, 58, 5), datetime.datetime(2020, 1, 8, 1, 24, 39), 
                       datetime.datetime(2020, 1, 8, 1, 49, 3), datetime.datetime(2020, 1, 8, 1, 59, 5), 
                       datetime.datetime(2020, 1, 8, 2, 22, 17), datetime.datetime(2020, 1, 8, 3, 24, 22), 
                       datetime.datetime(2020, 1, 8, 3, 38, 5), datetime.datetime(2020, 1, 8, 3, 39, 4), 
                       datetime.datetime(2020, 1, 8, 3, 46, 19), datetime.datetime(2020, 1, 8, 3, 53, 14), 
                       datetime.datetime(2020, 1, 8, 4, 0), datetime.datetime(2020, 1, 8, 4, 0, 20), 
                       datetime.datetime(2020, 1, 8, 4, 7, 59)]


FIN_SERIAL_list = [160, 292, 304, 306, 712, 760, 855, 878, 880, 881, 963, 964, 
                   965, 1028, 1234, 1433, 1495, 1701, 2195, 2333, 2339, 2406,
                  2459, 2471, 2473, 2528, 2570]

INI_SERIAL_list = [0, 161, 293, 305, 307, 713, 761, 856, 879, 881, 882, 964, 
                   965, 966, 1029, 1235, 1434, 1496, 1702, 2196, 2334, 2340, 
                   2407, 2460, 2472, 2474, 2529]

INI_SERIAL_list_copy = INI_SERIAL_list




ZONE_list = [u'garagem', u'ligacao', u'recolha', u'ligacao', u'recolha', u'ligacao', u'recolha', u'ligacao',
            u'recolha', u'ligacao', u'recolha', u'ligacao', u'recolha', u'ligacao', u'recolha', u'ligacao', u'descarga', u'ligacao', u'recolha', u'ligacao',
            u'garagem', u'ligacao', u'descarga', u'ligacao', u'descarga', u'ligacao', u'garagem']

zone_classification = {
                    'GARAGE':'garagem',
                    'CIRCUIT':'recolha',
                    'UNLOADING':'descarga',
                    'CONNECTION':'ligacao',
                    'CODE_FIELD_NAME':'ZONA'}

zone_abbreviation = {
                    zone_classification['GARAGE']:"G",
                    zone_classification['CIRCUIT']:"C",
                    zone_classification['UNLOADING']:"D",
                    zone_classification['CONNECTION']:"L",
                    'begin':'B',
                    'end':'E'}


CLASSIFICATION_LIST = []

track_list = []

def get_track_codes():
    b = zone_abbreviation['begin']
    g = zone_abbreviation[zone_classification['GARAGE']]
    p = zone_abbreviation[zone_classification['CIRCUIT']]
    d = zone_abbreviation[zone_classification['UNLOADING']]
    l = zone_abbreviation[zone_classification['CONNECTION']]
    e = zone_abbreviation['end']

    forward_check_dict = {
                    ((b,p),p): (p,p),
                    ((p,p),d): (d,d),
                    ((d,d),p): (d,p),
                    ((d,e),p): (d,p),
                    }
    backward_check_dict = {
                    ((b,p),p,1): ((p,p),1),
                    ((b,p),p,1): ((p,p),1),
                    ((b,p),p): (p,p),
                    ((p,p),d): (d,d),
                    ((d,d),p): (d,p),
                    ((d,e),p): (d,p),
                    }






track_dict = {((zone_abbreviation['source'],zone_abbreviation[zone_classification['GARAGE']]), 
    
    }




small_track_dict = {
                    (("P","C"),"P"): ("P","C"),
                    (("P","C"),"C"): ("C","T"),
                    (("C","T"),"P"): ("C","P"),
                    }


def get_newtrack(track,place):
    if (track,place) in get_newtrackdict.keys():
        return (get_newtrackdict[(track,place)],1)
    else:
        return (track,1)

track = ("S","P")
for zone in ZONE_list:
    zone_classification['GARAGE']

