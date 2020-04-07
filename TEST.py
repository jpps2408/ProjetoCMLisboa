Fields_Display={"CIRCUIT":"CIRCUITO",
                             "SHIFT":"PERCURSO",
                             "START_TIME":"H_INICIO",
                             "END_TIME":"H_FIM",
                             "CIRCUIT_TOLERANCE":"PARAMETRO_CIRCUITO",
                             "VISITED_TOLERANCE":"PARAMETRO_VISITADOS",
                             "ABSOLUTE_VISITED_STOPS":"NR_VISITADOS",
                             "RELATIVE_VISITED_STOPS":"%_VISITADOS",
                             "ABSOLUTE_IGNORED_STOPS":"NR_IGNORADOS",
                             "RELATIVE_IGNORED_STOPS":"%_IGNORADOS",
                             "GARAGE_TIME":"TEMP_GARAGEM",
                             "GARAGE_DIST":"DIST_GARAGEM",
                             "UNLOADING_TIME":"TEMP_DESCARGA",
                             "UNLOADING_DIST":"DIST_DESCARGA",
                             "CIRCUIT_TIME":"TEMP_RECOLHA",
                             "CIRCUIT_DIST":"DIST_RECOLHA",
                             "CONNECTION_TIME":"TEMP_LIGACAO",
                             "CONNECTION_DIST":"DIST_LIGACAO",
                             "OTHERS_TIME":"TEMP_OUTROS",
                             "OTHERS_DIST":"DIST_OUTROS"}

Fields_Numbers={"CIRCUIT":None,
                    "SHIFT":None,
                    "START_TIME":None,
                    "END_TIME":None,
                    "CIRCUIT_TOLERANCE":None,
                    "VISITED_TOLERANCE":None,
                    "ABSOLUTE_VISITED_STOPS":None,
                    "RELATIVE_VISITED_STOPS":None,
                    "ABSOLUTE_IGNORED_STOPS":None,
                    "RELATIVE_IGNORED_STOPS":None,
                    "GARAGE_TIME":None,
                    "GARAGE_DIST":None,
                    "UNLOADING_TIME":None,
                    "UNLOADING_DIST":None,
                    "CIRCUIT_TIME":None,
                    "CIRCUIT_DIST":None,
                    "CONNECTION_TIME":None,
                    "CONNECTION_DIST":None,
                    "OTHERS_TIME":None,
                    "OTHERS_DIST":None}

order =["CIRCUIT","SHIFT","START_TIME","END_TIME","CIRCUIT_TOLERANCE","VISITED_TOLERANCE",
        "ABSOLUTE_VISITED_STOPS", "RELATIVE_VISITED_STOPS","ABSOLUTE_IGNORED_STOPS",
        "RELATIVE_IGNORED_STOPS","GARAGE_TIME","GARAGE_DIST","UNLOADING_TIME",
        "UNLOADING_DIST","CIRCUIT_TIME","CIRCUIT_DIST","CONNECTION_TIME",
        "CONNECTION_DIST","OTHERS_TIME","OTHERS_DIST"]

Columns = [Fields_Display[key] for key in order]
Row = [Fields_Numbers[key] for key in order]


series = pd.DataFrame([Row], columns=Columns)