# schedule_data.py
# This file contains the data for the timetable.
# You should modify this data according to your needs.

# Define the time slots, their labels, and whether they are narrow intervals.
# (slot_id, label_line1, label_line2, is_interval)
TIMESLOT_DEFINITIONS = [
    ("M1", "M1", "7:30-8:20", False),
    ("M2", "M2", "8:20-9:10", False),
    ("IntM1", "IntM1", "9:10-9:20", True),
    ("M3", "M3", "9:20-10:10", False),
    ("M4", "M4", "10:10-11:00", False),
    ("IntM2", "IntM2", "11:00-11:10", True),
    ("M5", "M5", "11:10-12:00", False),
    ("M6", "M6", "12:00-12:50", False),
    ("T1", "T1", "13:30-14:20", False),
    ("T2", "T2", "14:20-15:10", False),
    ("IntT1", "IntT1", "15:10-15:20", True),
    ("T3", "T3", "15:20-16:10", False),
    ("T4", "T4", "16:10-17:00", False),
    ("IntT2", "IntT2", "17:00-17:10", True),
    ("T5", "T5", "17:10-18:00", False),
    ("T6", "T6", "18:00-18:50", False),
    ("IntN1", "IntN1", "18:50-19:00", True),
    ("N1", "N1", "19:00-19:50", False),
    ("N2", "N2", "19:50-20:40", False),
    ("IntN2", "IntN2", "20:40-20:50", True),
    ("N3", "N3", "20:50-21:40", False),
    ("N4", "N4", "21:40-22:30", False),
]

DAYS_OF_WEEK = ["Seg", "Ter", "Qua", "Qui", "Sex"]

# Main data structure for all periods and electives
# Each course has an 'id' (unique string), 'name', 'teacher',
# and 'slots' which is a list of tuples: (day_string, start_slot_id, end_slot_id)
# Example: ("Seg", "M1", "M2") means Monday from M1 up to and including M2.
COURSE_DATA = {
    "1": {
        "page_title": "CC: 1º Período",
        "location_info": "Instituto de Computação IC/UFAL, Cidade Universitária, Maceió",
        "courses": [
            {
                "id": "1_CALC",
                "name": "CÁLCULO DIFERENCIAL E INTEGRAL A",
                "teacher": "CIBELE",
                "slots": [
                    ("Ter", "M2", "M3"),
                    ("Ter", "M5", "M6"),
                    ("Qui", "M2", "M3"),
                    ("Qui", "M5", "M6"),
                ],
            },
            {
                "id": "1_LOG",
                "name": "LÓGICA PARA COMPUTAÇÃO",
                "teacher": "FABIO PARAGUAÇU",
                "slots": [("Seg", "T3", "T4"), ("Qua", "T3", "T4")],
            },
            {
                "id": "1_CSE",
                "name": "COMPUTAÇÃO SOCIEDADE E ÉTICA",
                "teacher": "PETRÚCIO BARROS",
                "slots": [("Seg", "T5", "T6"), ("Qua", "T5", "T6")],
            },
            {
                "id": "1_MD",
                "name": "MATEMÁTICA DISCRETA",
                "teacher": "LUCAS AMORIM",
                "slots": [("Ter", "N1", "N2"), ("Qui", "N1", "N2")],
            },
            {
                "id": "1_PROG1",
                "name": "PROGRAMAÇÃO 1",
                "teacher": "RODRIGO PAES",
                "slots": [("Sex", "T3", "T4"), ("Sex", "T5", "T6")],
            },
        ],
    },
    "2": {
        "page_title": "CC: 2º Período",
        "location_info": "Instituto de Computação IC/UFAL, Cidade Universitária, Maceió",
        "courses": [
            {
                "id": "2_DB",
                "name": "BANCO DE DADOS",
                "teacher": "CRISTINA TENÓRIO",
                "slots": [("Seg", "M5", "M6"), ("Qua", "M5", "M6")],
            },
            {
                "id": "2_GA",
                "name": "GEOMETRIA ANALÍTICA",
                "teacher": "LIBEL FONSECA",
                "slots": [("Seg", "T3", "T4"), ("Qua", "T3", "T4")],
            },
            {
                "id": "2_OAC",
                "name": "ORG E ARQ. DE COMPUTADORES",
                "teacher": "LUCAS AMORIM",
                "slots": [("Ter", "M3", "M4"), ("Qui", "M3", "M4")],
            },
            {
                "id": "2_ED",
                "name": "ESTRUTURA DE DADOS",
                "teacher": "MARIO HOZANO",
                "slots": [("Ter", "M5", "M6"), ("Qui", "M5", "M6")],
            },
        ],
    },
    "3": {
        "page_title": "CC: 3º Período",
        "location_info": "Instituto de Computação - IC/UFAL, Cidade Universitária, Maceió",
        "courses": [
            {
                "id": "3_AL",
                "name": "ÁLGEBRA LINEAR",
                "teacher": "GLAUBER RODRIGUES LEITE",
                "slots": [("Seg", "M1", "M2"), ("Qua", "M1", "M2")],
            },
            {
                "id": "3_PE",
                "name": "PROBABILIDADE E ESTATÍSTICA",
                "teacher": "PETRÚCIO BARROS",
                "slots": [("Seg", "M5", "M6"), ("Qua", "M5", "M6")],
            },
            {
                "id": "3_TG",
                "name": "TEORIA DOS GRAFOS",
                "teacher": "RIAN G. S. PINHEIRO",
                "slots": [("Ter", "T1", "T2"), ("Qui", "M5", "M6")],
            },  # Qui M5-M6 as per PDF image for 3rd period
            {
                "id": "3_RC1",
                "name": "REDES DE COMPUTADORES 1",
                "teacher": "ALMIR P GUIMARAES",
                "slots": [("Ter", "T3", "T4"), ("Qua", "T3", "T4")],
            },  # Note: PDF for 3rd period shows Qua T3-T4 for Redes, but that conflicts with PE. Assuming typo and placing on different day/time or you adjust
        ],
    },
    "4": {
        "page_title": "CC: 4º Período",
        "location_info": "Instituto de Computação IC/UFAL, Cidade Universitária, Maceió",
        "courses": [
            {
                "id": "4_TC",
                "name": "TEORIA DA COMPUTAÇÃO",
                "teacher": "FABIO PARAGUAÇU",
                "slots": [("Seg", "T1", "T2"), ("Ter", "T1", "T2")],
            },
            {
                "id": "4_PAA",
                "name": "PROJETO E ANÁLISE DE ALGORITMOS",
                "teacher": "RIAN G. S. PINHEIRO",
                "slots": [("Seg", "T5", "T6"), ("Qui", "T5", "T6")],
            },
            {
                "id": "4_PROG3",
                "name": "PROGRAMAÇÃO 3",
                "teacher": "RANILSON PAIVA",
                "slots": [("Ter", "T3", "T4"), ("Qui", "T3", "T4")],
            },
            {
                "id": "4_PS",
                "name": "PROJETO DE SOFTWARE",
                "teacher": "BALDOINO NETO",
                "slots": [("Qua", "T3", "T4"), ("Qua", "T5", "T6")],
            },
        ],
    },
    "5": {
        "page_title": "CC: 5º Período",
        "location_info": "Instituto de Computação - IC/UFAL, Cidade Universitária, Maceió",
        "courses": [
            {
                "id": "5_SO",
                "name": "SISTEMAS OPERACIONAIS",
                "teacher": "ANDRE AQUINO",
                "slots": [("Seg", "T1", "T2"), ("Qua", "T1", "T2")],
            },
            {
                "id": "5_COMP",
                "name": "COMPILADORES",
                "teacher": "ARTURO DOMINGUEZ",
                "slots": [("Seg", "T3", "T4"), ("Qua", "T3", "T4")],
            },
            {
                "id": "5_IA",
                "name": "INTELIGÊNCIA ARTIFICIAL",
                "teacher": "EVANDRO DE B COSTA",
                "slots": [("Ter", "T1", "T2"), ("Qui", "T1", "T2")],
            },
            {
                "id": "5_CG",
                "name": "COMPUTAÇÃO GRÁFICA",
                "teacher": "MARCELO OLIVEIRA",
                "slots": [("Ter", "T3", "T4"), ("Qui", "T3", "T4")],
            },
        ],
    },
    "6": {
        "page_title": "CC: 6º Período",
        "location_info": "Instituto de Computação - IC/UFAL, Cidade Universitária, Maceió",
        "courses": [
            {
                "id": "6_PDS",
                "name": "PROJETO E DESENVOLVIMENTO DE SISTEMAS",
                "teacher": "CT/IIBSP/RDBP/WCT",  # Multiple teachers or group
                "slots": [
                    ("Seg", "M3", "M4"),
                    ("Seg", "M5", "M6"),
                    ("Qua", "M3", "M4"),
                    ("Qua", "M5", "M6"),
                    ("Qui", "M5", "M6"),
                    ("Qui", "M3", "M4"),
                ],
            }  # This course occupies many slots
        ],
    },
    "7": {
        "page_title": "CC: 7º Período",
        "location_info": "Instituto de Computação - IC/UFAL, Cidade Universitária, Maceió",
        "courses": [
            {
                "id": "7_MET",
                "name": "MET. DA PESQ. E DO TRABALHO",
                "teacher": "MARCELO OLIVEIRA",
                "slots": [("Ter", "M1", "M2"), ("Qui", "M1", "M2")],
            },
            {
                "id": "7_DIR",
                "name": "NOÇÕES DE DIREITO",
                "teacher": "CID CAVALCANTI DE ALBUQUERQUE",
                "slots": [("Ter", "M3", "M4"), ("Qui", "M3", "M4")],
            },
        ],
    },
    "8": {  # 8th Period is empty in the example PDF
        "page_title": "CC: 8º Período",
        "location_info": "Instituto de Computação IC/UFAL, Cidade Universitária, Maceió",
        "courses": [
            # Add courses here if any
        ],
    },
    "Eletivas": {
        "page_title_prefix": "CC: Eletivas",
        "location_info": "Instituto de Computação IC/UFAL, Cidade Universitária, Maceió",
        "courses": [
            {
                "id": "ELET001",
                "name": "TÓPICOS EM BANCO DE DADOS AVANÇADO",
                "teacher": "PROF. ELET A",
                "slots": [("Seg", "M1", "M2")],
            },
            {
                "id": "ELET002",
                "name": "DESENV. ÁGIL DE SOFTWARE",
                "teacher": "PROF. ELET B",
                "slots": [("Seg", "M1", "M2")],
            },  # Conflict with ELET001
            {
                "id": "ELET003",
                "name": "VISÃO COMPUTACIONAL",
                "teacher": "PROF. ELET C",
                "slots": [("Seg", "M3", "M4")],
            },
            {
                "id": "ELET004",
                "name": "APRENDIZADO DE MÁQUINA APLICADO",
                "teacher": "PROF. ELET D",
                "slots": [("Ter", "T1", "T2")],
            },
            {
                "id": "ELET005",
                "name": "SEGURANÇA DE APLICAÇÕES WEB",
                "teacher": "PROF. ELET E",
                "slots": [("Qua", "N1", "N2")],
            },
            {
                "id": "ELET006",
                "name": "COMPUTAÇÃO EM NUVEM",
                "teacher": "PROF. ELET F",
                "slots": [("Qui", "M5", "M6")],
            },
            {
                "id": "ELET007",
                "name": "JOGOS DIGITAIS: DESIGN E DESENV.",
                "teacher": "PROF. ELET G",
                "slots": [("Sex", "T3", "T4")],
            },
            {
                "id": "ELET008",
                "name": "REDES MÓVEIS E SEM FIO",
                "teacher": "PROF. ELET H",
                "slots": [("Seg", "M3", "M4")],
            },  # Conflict with ELET003
            {
                "id": "ELET009",
                "name": "PROCESSAMENTO DE LINGUAGEM NATURAL",
                "teacher": "PROF. ELET I",
                "slots": [("Ter", "M1", "M2")],
            },
            {
                "id": "ELET010",
                "name": "BIOINFORMÁTICA",
                "teacher": "PROF. ELET J",
                "slots": [("Qua", "T5", "T6")],
            },
            {
                "id": "ELET011",
                "name": "INTERAÇÃO HUMANO-COMPUTADOR",
                "teacher": "PROF. ELET K",
                "slots": [("Sex", "M1", "M2")],
            },
            {
                "id": "ELET012",
                "name": "SISTEMAS EMBARCADOS",
                "teacher": "PROF. ELET L",
                "slots": [("Sex", "M1", "M2")],
            },  # Conflict ELET011
        ],
    },
}
