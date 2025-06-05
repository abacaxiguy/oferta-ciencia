import random
import numpy as np
from dataclasses import dataclass
from typing import List, Dict, Set, Tuple
import copy

@dataclass
class Professor:
    nome: str
    areas: List[str]
    max_disciplinas: int = 3

@dataclass
class Disciplina:
    nome: str
    periodo: int
    obrigatoria: bool
    carga_horaria: int = 4  # 4 horas por semana
    laboratorio_necessario: bool = False

@dataclass
class Sala:
    nome: str
    laboratorio: bool = False

@dataclass
class Horario:
    dia: str  # Segunda, Terça, etc.
    turno: str  # M ou T
    slot: int  # 1-6

@dataclass
class Alocacao:
    professor: str
    disciplina: str
    sala: str
    horarios: List[Horario]

class GeneticScheduler:
    def __init__(self):
        self.dias_semana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta']
        self.professores = self._init_professores()
        self.disciplinas = self._init_disciplinas()
        self.salas = self._init_salas()
        self.horarios = self._init_horarios()
            
    def _init_professores(self) -> List[Professor]:
        professores_data = [
            ("ALAN PEDRO DA SILVA", ["ESTRUTURA DE DADOS", "PROGRAMAÇÃO 1"]),
            ("ALEJANDRO CÉSAR FRERY", ["PROBABILIDADE E ESTATÍSTICA", "TEORIA DA COMPUTAÇÃO"]),
            ("ALMIR PEREIRA GUIMARÃES", ["REDES DE COMPUTADORES", "ORGANIZAÇÃO E ARQUITETURA DE COMPUTADORES"]),
            ("ALLA", ["ÁLGEBRA LINEAR", "GEOMETRIA ANALÍTICA", "SISTEMAS OPERACIONAIS"]),
            ("ARTUROHD", ["CÁLCULO DIFERENCIAL E INTEGRAL", "MATEMÁTICA DISCRETA", "PROGRAMAÇÃO 2", "COMPILADORES", "CÁLCULO 1", "CÁLCULO 2", "CÁLCULO 3", "CÁLCULO 4"]),
            ("AYDANO PAMPONET MACHADO", ["LÓGICA PARA COMPUTAÇÃO", "TEORIA DOS GRAFOS"]),
            ("BALDOINO", ["BANCO DE DADOS", "PROGRAMAÇÃO 2"]),
            ("BRUNO PIMENTEL", ["PROGRAMAÇÃO 3", "PROJETO E ANÁLISE DE ALGORITMOS", "MATEMÁTICA DISCRETA", "PROBABILIDADE E ESTATÍSTICA", "CIÊNCIA DE DADOS", "APRENDIZAGEM DE MÁQUINA", "EXPLORAÇÃO E MINERAÇÃO DE DADOS"]),
            ("BRUNO NOGUEIRA", ["COMPUTAÇÃO, SOCIEDADE E ÉTICA", "ORGANIZAÇÃO E ARQUITETURA DE COMPUTADORES", "EMPREENDEDORISMO", "INTRODUÇÃO À ADMINISTRAÇÃO"]),
            ("CID", ["TEORIA DA COMPUTAÇÃO", "LÓGICA PARA COMPUTAÇÃO", "NOÇÕES DE DIREITO"]),
            ("DAVI BIBIANO BRITO", ["ESTRUTURA DE DADOS", "PROGRAMAÇÃO 1"]),
            ("ERICK", ["REDES DE COMPUTADORES", "ORGANIZAÇÃO E ARQUITETURA DE COMPUTADORES", "SISTEMAS DIGITAIS", "CIRCUITOS DIGITAIS", "MICROCONTROLADORES E APLICAÇÕES", "FPGA"]),
            ("EVANDRO", ["MATEMÁTICA DISCRETA", "TEORIA DOS GRAFOS","INTELIGÊNCIA ARTIFICIAL", "REDES NEURAIS E APRENDIZADO PROFUNDO", "COMPUTAÇÃO EVOLUCIONÁRIA"]),
            ("FÁBIO JOSÉ COUTINHO", ["PROGRAMAÇÃO 2", "PROJETO E ANÁLISE DE ALGORITMOS"]),
            ("PARAGUA", ["BANCO DE DADOS", "PROGRAMAÇÃO 3", "COMPILADORES", "BANCO DE DADOS 2", "SISTEMAS EMBARCADOS"]),
            ("GLAUBER RODRIGUES LEITE", ["PROGRAMAÇÃO 1", "ESTRUTURA DE DADOS"]),
            ("ÍCARO", ["CÁLCULO DIFERENCIAL E INTEGRAL", "ÁLGEBRA LINEAR"]),
            ("IG", ["PROBABILIDADE E ESTATÍSTICA", "TEORIA DOS GRAFOS"]),
            ("JOÃO RAPHAEL SOUZA", ["LÓGICA PARA COMPUTAÇÃO", "TEORIA DA COMPUTAÇÃO"]),
            ("JOBSON NASCIMENTO", ["REDES DE COMPUTADORES", "ORGANIZAÇÃO E ARQUITETURA DE COMPUTADORES"]),
            ("LEANDRO DIAS", ["BANCO DE DADOS", "PROGRAMAÇÃO 2"]),
            ("LEANDRO", ["MATEMÁTICA DISCRETA", "CÁLCULO DIFERENCIAL E INTEGRAL"]),
            ("LEONARDO VIANA PEREIRA", ["PROGRAMAÇÃO 3", "PROJETO E ANÁLISE DE ALGORITMOS"]),
            ("LUCAS BENEVIDES VIANA", ["TEORIA DOS GRAFOS", "LÓGICA PARA COMPUTAÇÃO"]),
            ("MARCELO COSTA OLIVEIRA", ["ESTRUTURA DE DADOS", "PROGRAMAÇÃO 1", "COMPUTAÇÃO GRÁFICA", "METODOLOGIA DE PESQUISA E TRABALHO INDIVIDUAL", "VISÃO COMPUTACIONAL", "PROCESSAMENTO DIGITAL DE IMAGENS"]),
            ("MÁRCIO", ["ÁLGEBRA LINEAR", "GEOMETRIA ANALÍTICA", "ESTRUTURA DE DADOS"]),
            ("MARIA CRISTINA TENÓRIO", ["PROGRAMAÇÃO 3", "PROJETO E ANÁLISE DE ALGORITMOS", "BANCO DE DADOS"]),
            ("MÁRIO HOZANO LUCAS", ["CÁLCULO DIFERENCIAL E INTEGRAL", "MATEMÁTICA DISCRETA", "PROGRAMAÇÃO 2"]),
            ("MAURÍCIO BELTRÃO", ["TEORIA DA COMPUTAÇÃO", "LÓGICA PARA COMPUTAÇÃO"]),
            ("OLIVAL", ["PROBABILIDADE E ESTATÍSTICA", "TEORIA DOS GRAFOS"]),
            ("PETRUCIO", ["BANCO DE DADOS", "PROGRAMAÇÃO 2"]),
            ("RAFAEL", ["REDES DE COMPUTADORES", "ORGANIZAÇÃO E ARQUITETURA DE COMPUTADORES", "CONCEITOS DE LINGUAGEM DE PROGRAMAÇÃO", "SISTEMAS DISTRIBUÍDOS", "REDES DE COMPUTADORES 2"]),
            ("RANILSON PAIVA", ["ESTRUTURA DE DADOS", "PROGRAMAÇÃO 1", "PROBABILIDADE E ESTATÍSTICA"]),
            ("RIAN GABRIEL", ["COMPUTAÇÃO, SOCIEDADE E ÉTICA", "PROJETO E ANÁLISE DE ALGORITMOS"]),
            ("ROBERTA", ["LÓGICA PARA COMPUTAÇÃO", "TEORIA DA COMPUTAÇÃO"]),
            ("RODRIGO PAES", ["PROGRAMAÇÃO 3", "PROJETO E ANÁLISE DE ALGORITMOS"]),
            ("RODRIGO JOSÉ SARMENTO", ["ÁLGEBRA LINEAR", "GEOMETRIA ANALÍTICA"]),
            ("THALES", ["CÁLCULO DIFERENCIAL E INTEGRAL", "MATEMÁTICA DISCRETA"]),
            ("THIAGO CORDEIRO", ["PROGRAMAÇÃO 2", "PROJETO E ANÁLISE DE ALGORITMOS"]),
            ("TIAGO ALVES DE ALMEIDA", ["TEORIA DOS GRAFOS", "LÓGICA PARA COMPUTAÇÃO","CÁLCULO DIFERENCIAL E INTEGRAL"]),
            ("TIAGO FIGUEIREDO VIEIRA", ["REDES DE COMPUTADORES", "ORGANIZAÇÃO E ARQUITETURA DE COMPUTADORES"]),
            ("WILLY CARVALHO TIENGO", ["PROBABILIDADE E ESTATÍSTICA", "TEORIA DA COMPUTAÇÃO", "PROJETO E DESENVOLVIMENTO DE SISTEMAS", "TESTE DE SOFTWARE", "SEGURANÇA DE SISTEMAS COMPUTACIONAIS", "GERÊNCIA DE PROJETO"]),
            ("YANG", ["ÁLGEBRA LINEAR", "GEOMETRIA ANALÍTICA"])
        ]
        # Crie e retorne a lista de objetos Professor, conforme a sua implementação
        return [Professor(nome, disciplinas) for nome, disciplinas in professores_data]

    
    def _init_disciplinas(self) -> List[Disciplina]:
        disciplinas_obrigatorias = [
            ("PROGRAMAÇÃO 1", 1, True, True),
            ("LÓGICA PARA COMPUTAÇÃO", 1, True, False),
            ("COMPUTAÇÃO, SOCIEDADE E ÉTICA", 1, True, False),
            ("MATEMÁTICA DISCRETA", 1, True, False),
            ("CÁLCULO DIFERENCIAL E INTEGRAL", 1, True, False),
            ("ESTRUTURA DE DADOS", 2, True, True),
            ("BANCO DE DADOS", 2, True, True),
            ("ORGANIZAÇÃO E ARQUITETURA DE COMPUTADORES", 2, True, False),
            ("GEOMETRIA ANALÍTICA", 2, True, False),
            ("REDES DE COMPUTADORES", 3, True, False),
            ("TEORIA DOS GRAFOS", 3, True, False),
            ("PROBABILIDADE E ESTATÍSTICA", 3, True, False),
            ("ÁLGEBRA LINEAR", 3, True, False),
            ("PROGRAMAÇÃO 2", 4, True, True),
            ("PROGRAMAÇÃO 3", 4, True, True),
            ("PROJETO E ANÁLISE DE ALGORITMOS", 4, True, False),
            ("TEORIA DA COMPUTAÇÃO", 4, True, False),
            ("ACE 1: PROJETO I", 4, True, False),
            ("SISTEMAS OPERACIONAIS", 5, True, False),
            ("COMPILADORES", 5, True, False),
            ("INTELIGÊNCIA ARTIFICIAL", 5, True, False),
            ("COMPUTAÇÃO GRÁFICA", 5, True, False),
            ("ACE 2: CONTINUIDADE DO PROJETO I", 5, True, False),
            ("PROJETO E DESENVOLVIMENTO DE SISTEMAS", 6, True, True),
            ("ACE 3: PROJETO 2", 6, True, False),
            ("METODOLOGIA DE PESQUISA E TRABALHO INDIVIDUAL", 7, True, False),
            ("NOÇÕES DE DIREITO", 7, True, False),
            ("ACE 4: CONTINUIAÇÃO DE PROJETO 2", 7, True, False),
            ("ACE 5: EVENTO", 8, True, False)
        ]
        
        # Eletivas - Disciplinas opcionais (período 0 conforme projeto.txt)
        disciplinas_eletivas = [
            ("INTRODUÇÃO À COMPUTAÇÃO", 0, False, True),
            ("CONCEITOS DE LINGUAGEM DE PROGRAMAÇÃO", 0, False, False),
            ("APRENDIZAGEM DE MÁQUINA", 0, False, True),
            ("SISTEMAS DIGITAIS", 0, False, False),
            ("SISTEMAS DISTRIBUÍDOS", 0, False, False),
            ("REDES NEURAIS E APRENDIZADO PROFUNDO", 0, False, True),
            ("FPGA", 0, False, True),
            ("INTERAÇÃO HOMEM-MÁQUINA", 0, False, True),
            ("PROCESSAMENTO DIGITAL DE IMAGENS", 0, False, True),
            ("COMPUTAÇÃO EVOLUCIONÁRIA", 0, False, True),
            ("SISTEMAS EMBARCADOS", 0, False, True),
            ("GERÊNCIA DE PROJETO", 0, False, False),
            ("VISÃO COMPUTACIONAL", 0, False, True),
            ("CIÊNCIA DE DADOS", 0, False, True),
            ("MICROCONTROLADORES E APLICAÇÕES", 0, False, True),
            ("SEGURANÇA DE SISTEMAS COMPUTACIONAIS", 0, False, False),
            ("CÁLCULO 3", 0, False, False),
            ("TÓPICOS EM CIÊNCIA DA COMPUTAÇÃO 1", 0, False, False),
            ("TÓPICOS EM CIÊNCIA DA COMPUTAÇÃO 2", 0, False, False),
            ("TÓPICOS EM CIÊNCIA DA COMPUTAÇÃO 3", 0, False, False),
            ("TÓPICOS EM MATEMÁTICA PARA COMPUTAÇÃO 1", 0, False, False),
            ("TÓPICOS EM MATEMÁTICA PARA COMPUTAÇÃO 2", 0, False, False),
            ("TÓPICOS EM MATEMÁTICA PARA COMPUTAÇÃO 3", 0, False, False),
            ("TÓPICOS EM FÍSICA PARA COMPUTAÇÃO 1", 0, False, False),
            ("TÓPICOS EM FÍSICA PARA COMPUTAÇÃO 2", 0, False, False),
            ("TÓPICOS EM FÍSICA PARA COMPUTAÇÃO 3", 0, False, False),
            ("NAVEGAÇÃO EM ROBÓTICA MÓVEL", 0, False, True),
            ("PESQUISA OPERACIONAL", 0, False, False),
            ("CÁLCULO 2", 0, False, False),
            ("EMPREENDEDORISMO", 0, False, False),
            ("TESTE DE SOFTWARE", 0, False, True),
            ("BANCO DE DADOS 2", 0, False, True),
            ("FUNDAMENTOS DE IA APLICADOS AO DIAGNÓSTICO MÉDICO", 0, False, True),
            ("PROCESSAMENTO DE LINGUAGEM NATURAL", 0, False, True),
            ("LABORATÓRIO DE PROGRAMAÇÃO", 0, False, True),
            ("INTELIGÊNCIA ARTIFICIAL APLICADA AO DIAGNÓSTICO DE DOENÇAS", 0, False, True),
            ("CÁLCULO 4", 0, False, False),
            ("TÓPICOS EM SOFTWARE BÁSICO", 0, False, True),
            ("LIBRAS", 0, False, False),
            ("GAMIFICAÇÃO", 0, False, True),
            ("EXPLORAÇÃO E MINERAÇÃO DE DADOS", 0, False, True),
            ("TÓPICOS ESPECIAIS EM GESTÃO DE PROJETOS", 0, False, False),
            ("TÓPICOS ESP. EM BANCO DE DADOS: GERAÇÃO DE DADOS SEMIESTRUTURADOS", 0, False, True),
            ("TÓPICOS EM ENGENHARIA DE SOFTWARE - PROJETANDO LINHAS DE PRODUTO DE SOFTWARE", 0, False, True),
            ("CÁLCULO 1", 0, False, False),
            ("INTRODUÇÃO À ADMINISTRAÇÃO", 0, False, False),
            ("LABORATÓRIO DE INTELIGÊNCIA ARTIFICIAL EM ROBÓTICA", 0, False, True),
            ("TÓPICOS ESPECIAIS EM GERÊNCIA E PROCESSAMENTO DE DADOS EM LARGAESCALA", 0, False, True),
            ("REDES DE COMPUTADORES 2", 0, False, False),
            ("REUSO DE SOFTWARE E METODOLOGIAS ÁGEIS", 0, False, True),
            ("INGLÊS INSTRUMENTAL", 0, False, False),
            ("METODOLOGIA E PROCESSOS", 0, False, False),
            ("CIRCUITOS DIGITAIS", 0, False, True),
            ("DESENHO", 0, False, False)
        ]
        
        # Combina disciplinas obrigatórias e eletivas
        todas_disciplinas = disciplinas_obrigatorias + disciplinas_eletivas
        
        return [Disciplina(nome, periodo, obrigatoria, 4, laboratorio) 
                for nome, periodo, obrigatoria, laboratorio in todas_disciplinas]
    
    def _init_salas(self) -> List[Sala]:
        salas_data = [
            ("Auditório CEPETEC", False),
            ("Sala de Aula 02", False),
            ("Sala de Aula 03", False),
            ("Mini-sala 01", False),
            ("Mini-auditório", False),
            ("Laboratório de Robótica", True),
            ("Laboratório de Graduação 01", True),
            ("Laboratório de Graduação 02", True),
            ("Laboratório de Graduação 03", True),
            ("Lab. de Circ. Elétricos e Eletrônicos", True),
            ("Sala de Aula 207", False),
            ("Sala de Aula 206", False),
            ("Sala de Aula 205", False),
            ("Sala de Aula 204", False)
        ]
        
        return [Sala(nome, laboratorio) for nome, laboratorio in salas_data]
    
    def _init_horarios(self) -> List[Horario]:
        horarios = []
        for dia in self.dias_semana:
            for turno in ['M', 'T']:
                for slot in range(1, 7):
                    horarios.append(Horario(dia, turno, slot))
        return horarios
    
    def professor_pode_lecionar(self, professor: Professor, disciplina: Disciplina) -> bool:
        """Verifica se um professor pode lecionar uma disciplina baseado em sua especialização"""
        # Professores podem lecionar disciplinas dos 4 primeiros períodos
        if disciplina.periodo <= 4:
            # Verifica se tem especialização ou se é dos primeiros períodos
            for area in professor.areas:
                if area.upper() in disciplina.nome.upper():
                    return True
            # Se não tem especialização específica, pode lecionar se for dos primeiros períodos
            return disciplina.periodo <= 4
        
        # Para disciplinas avançadas, precisa ter especialização
        for area in professor.areas:
            if area.upper() in disciplina.nome.upper():
                return True
        return False
    
    def criar_cromossomo(self) -> List[Alocacao]:
        """Cria um cromossomo (solução) aleatória com alocação em 8 períodos sem conflitos"""
        cromossomo = []
        disciplinas_alocadas = set()
        horarios_ocupados = set()  # Track occupied time slots
        professores_horarios = {}  # Track professor schedules
        salas_horarios = {}  # Track room schedules
        
        # Ordena priorizando disciplinas obrigatórias e pelo período recomendado
        disciplinas_ordenadas = sorted(self.disciplinas, 
                                    key=lambda d: (not d.obrigatoria, d.periodo))
        
        for disciplina in disciplinas_ordenadas:
            if disciplina.nome in disciplinas_alocadas:
                continue
            
            # Encontra professores aptos para a disciplina
            professores_aptos = [p for p in self.professores 
                                if self.professor_pode_lecionar(p, disciplina)]
            
            if not professores_aptos:
                continue
            
            # Tenta várias combinações de professor, sala e horário sem conflito
            tentativas_maximas = 50
            alocacao_criada = False
            
            for tentativa in range(tentativas_maximas):
                professor = random.choice(professores_aptos)
                
                # Escolhe sala apropriada
                salas_disponiveis = [s for s in self.salas 
                                    if not disciplina.laboratorio_necessario or s.laboratorio]
                if not salas_disponiveis:
                    salas_disponiveis = self.salas
                
                sala = random.choice(salas_disponiveis)
                
                # Tenta alocar horários sem conflito
                horarios_alocados = self._alocar_horarios_sem_conflito(
                    professores_horarios.get(professor.nome, []),
                    salas_horarios.get(sala.nome, [])
                )
                
                if horarios_alocados:
                    # Cria a alocação
                    alocacao = Alocacao(professor.nome, disciplina.nome, sala.nome, horarios_alocados)
                    cromossomo.append(alocacao)
                    disciplinas_alocadas.add(disciplina.nome)
                    
                    # Atualiza os registros de horários ocupados
                    if professor.nome not in professores_horarios:
                        professores_horarios[professor.nome] = []
                    professores_horarios[professor.nome].extend(horarios_alocados)
                    
                    if sala.nome not in salas_horarios:
                        salas_horarios[sala.nome] = []
                    salas_horarios[sala.nome].extend(horarios_alocados)
                    
                    alocacao_criada = True
                    break
            
            # Se não conseguiu alocar após muitas tentativas, pula esta disciplina
            if not alocacao_criada:
                continue
        
        return cromossomo
    
    def _alocar_horarios_disciplina(self) -> List[Horario]:
        """Aloca 4 horas de aula em 2 blocos de 2 horas"""
        horarios = []
        tentativas = 0
        
        while len(horarios) < 4 and tentativas < 100:
            dia = random.choice(self.dias_semana)
            turno = random.choice(['M', 'T'])
            slot_inicial = random.randint(1, 5)  # Para ter 2 slots consecutivos
            
            # Adiciona 2 slots consecutivos
            horario1 = Horario(dia, turno, slot_inicial)
            horario2 = Horario(dia, turno, slot_inicial + 1)
            
            # Verifica se já não foram alocados
            if horario1 not in horarios and horario2 not in horarios:
                horarios.extend([horario1, horario2])
            
            tentativas += 1
            
            # Se já temos 4 horários, termina
            if len(horarios) >= 4:
                break
                
            # Tenta outro dia para os próximos 2 horários
            if len(horarios) == 2:
                dias_restantes = [d for d in self.dias_semana if d != dia]
                if dias_restantes:
                    dia = random.choice(dias_restantes)
        
        return horarios[:4]  # Garante exatamente 4 horários
    
    def _alocar_horarios_sem_conflito(self, horarios_professor: List[Horario], horarios_sala: List[Horario]) -> List[Horario]:
        """Aloca 4 horas de aula em 2 blocos de 2 horas sem conflitos, preferencialmente em dias diferentes"""
        horarios_ocupados = set()
        
        # Converte listas de horários ocupados para conjunto de tuplas
        for h in horarios_professor + horarios_sala:
            horarios_ocupados.add((h.dia, h.turno, h.slot))
        
        # ESTRATÉGIA MELHORADA: Tenta primeiro alocar em dois dias diferentes
        # Primeira tentativa: forçar dois dias diferentes
        for tentativa_dois_dias in range(50):
            dia1 = random.choice(self.dias_semana)
            dias_restantes = [d for d in self.dias_semana if d != dia1]
            if not dias_restantes:
                continue
            dia2 = random.choice(dias_restantes)
            
            # Tenta alocar 2 horas no primeiro dia
            turno1 = random.choice(['M', 'T'])
            slot_inicial1 = random.randint(1, 5)
            
            # Verifica se os slots estão livres no primeiro dia
            slot1_livre = (dia1, turno1, slot_inicial1) not in horarios_ocupados
            slot2_livre = (dia1, turno1, slot_inicial1 + 1) not in horarios_ocupados
            
            if not (slot1_livre and slot2_livre):
                continue
            
            # Tenta alocar 2 horas no segundo dia
            turno2 = random.choice(['M', 'T'])
            slot_inicial2 = random.randint(1, 5)
            
            # Verifica se os slots estão livres no segundo dia
            slot3_livre = (dia2, turno2, slot_inicial2) not in horarios_ocupados
            slot4_livre = (dia2, turno2, slot_inicial2 + 1) not in horarios_ocupados
            
            if slot3_livre and slot4_livre:
                # Sucesso! Dois dias diferentes
                return [
                    Horario(dia1, turno1, slot_inicial1),
                    Horario(dia1, turno1, slot_inicial1 + 1),
                    Horario(dia2, turno2, slot_inicial2),
                    Horario(dia2, turno2, slot_inicial2 + 1)
                ]
        
        # FALLBACK: Se não conseguiu dois dias, tenta método original
        horarios_alocados = []
        tentativas = 0
        max_tentativas = 50
        
        while len(horarios_alocados) < 4 and tentativas < max_tentativas:
            dia = random.choice(self.dias_semana)
            turno = random.choice(['M', 'T'])
            slot_inicial = random.randint(1, 5)
            
            # Verifica se os 2 slots consecutivos estão livres
            slot1_livre = (dia, turno, slot_inicial) not in horarios_ocupados
            slot2_livre = (dia, turno, slot_inicial + 1) not in horarios_ocupados
            
            if slot1_livre and slot2_livre:
                horario1 = Horario(dia, turno, slot_inicial)
                horario2 = Horario(dia, turno, slot_inicial + 1)
                
                # Verifica se estes horários não estão já na lista que estamos construindo
                horarios_existentes = [(h.dia, h.turno, h.slot) for h in horarios_alocados]
                if (dia, turno, slot_inicial) not in horarios_existentes and (dia, turno, slot_inicial + 1) not in horarios_existentes:
                    horarios_alocados.extend([horario1, horario2])
                    # Adiciona aos horários ocupados para evitar sobreposição no mesmo bloco
                    horarios_ocupados.add((dia, turno, slot_inicial))
                    horarios_ocupados.add((dia, turno, slot_inicial + 1))
            
            tentativas += 1
            
            # Se já temos 4 horários, termina
            if len(horarios_alocados) >= 4:
                break
                
            # Se já temos 2 horários, força outro dia para os próximos 2
            if len(horarios_alocados) == 2:
                dias_ja_usados = set(h.dia for h in horarios_alocados)
                dias_livres = [d for d in self.dias_semana if d not in dias_ja_usados]
                if dias_livres:
                    dia = random.choice(dias_livres)
        
        return horarios_alocados[:4] if len(horarios_alocados) == 4 else []
    
    def calcular_fitness(self, cromossomo: List[Alocacao]) -> float:
        """Calcula o fitness de um cromossomo (quanto maior, melhor)"""
        fitness = 1000  # Valor base
        penalidades = 0
        
        # Verifica conflitos de professor
        prof_horarios = {}
        for alocacao in cromossomo:
            if alocacao.professor not in prof_horarios:
                prof_horarios[alocacao.professor] = []
            prof_horarios[alocacao.professor].extend(alocacao.horarios)
        
        # Penaliza conflitos de horário do professor (mais rigoroso)
        for prof, horarios in prof_horarios.items():
            horarios_tuples = [(h.dia, h.turno, h.slot) for h in horarios]
            horarios_set = set(horarios_tuples)
            conflitos_prof = len(horarios_tuples) - len(horarios_set)
            if conflitos_prof > 0:
                penalidades += 1000 * conflitos_prof  # Penalidade extremamente alta para conflitos
        
        # Verifica conflitos de sala (mais rigoroso)
        sala_horarios = {}
        for alocacao in cromossomo:
            if alocacao.sala not in sala_horarios:
                sala_horarios[alocacao.sala] = []
            sala_horarios[alocacao.sala].extend(alocacao.horarios)
        
        # Penaliza conflitos de sala
        for sala, horarios in sala_horarios.items():
            horarios_tuples = [(h.dia, h.turno, h.slot) for h in horarios]
            horarios_set = set(horarios_tuples)
            conflitos_sala = len(horarios_tuples) - len(horarios_set)
            if conflitos_sala > 0:
                penalidades += 1000 * conflitos_sala  # Penalidade extremamente alta para conflitos
        
        # Verifica carga de trabalho dos professores
        disciplinas_por_prof = {}
        for alocacao in cromossomo:
            if alocacao.professor not in disciplinas_por_prof:
                disciplinas_por_prof[alocacao.professor] = 0
            disciplinas_por_prof[alocacao.professor] += 1
        
        # Penaliza professores com muitas ou poucas disciplinas
        for prof, num_disc in disciplinas_por_prof.items():
            if num_disc > 3:
                penalidades += 50 * (num_disc - 3)
            elif num_disc == 0:
                penalidades += 30
        
        # Bonifica disciplinas obrigatórias alocadas
        disciplinas_obrigatorias_alocadas = sum(1 for alocacao in cromossomo 
                                              for disc in self.disciplinas 
                                              if disc.nome == alocacao.disciplina and disc.obrigatoria)
        fitness += disciplinas_obrigatorias_alocadas * 10
        
        # Bonifica uso adequado de laboratórios
        for alocacao in cromossomo:
            disciplina = next((d for d in self.disciplinas if d.nome == alocacao.disciplina), None)
            sala = next((s for s in self.salas if s.nome == alocacao.sala), None)
            if disciplina and sala:
                if disciplina.laboratorio_necessario and sala.laboratorio:
                    fitness += 5
                elif not disciplina.laboratorio_necessario and not sala.laboratorio:
                    fitness += 2
        
        # Verifica se professores vão ao IC todos os dias (restrição Torres)
        for prof, horarios in prof_horarios.items():
            dias_prof = set(h.dia for h in horarios)
            if len(dias_prof) == 5:  # Todos os dias da semana
                fitness += 20
            elif len(dias_prof) >= 3:  # Pelo menos 3 dias
                fitness += 10
        
        # NOVA PENALIDADE: Penaliza disciplinas em apenas um dia (incentiva dispersão)
        for alocacao in cromossomo:
            dias_disciplina = set(h.dia for h in alocacao.horarios)
            if len(dias_disciplina) == 1:
                # Penaliza fortemente disciplinas concentradas em um só dia
                penalidades += 30
            elif len(dias_disciplina) == 2:
                # Bonifica disciplinas bem distribuídas em dois dias
                fitness += 15
        
        return max(0, fitness - penalidades)
    
    def crossover(self, pai1: List[Alocacao], pai2: List[Alocacao]) -> Tuple[List[Alocacao], List[Alocacao]]:
        """Realiza crossover entre dois cromossomos"""
        if len(pai1) == 0 or len(pai2) == 0:
            return pai1.copy(), pai2.copy()
        
        ponto_corte = random.randint(1, min(len(pai1), len(pai2)) - 1)
        
        filho1 = pai1[:ponto_corte] + pai2[ponto_corte:]
        filho2 = pai2[:ponto_corte] + pai1[ponto_corte:]
        
        # Remove duplicações de disciplinas
        filho1 = self._remove_duplicatas(filho1)
        filho2 = self._remove_duplicatas(filho2)
        
        # Valida e corrige conflitos
        filho1 = self._validar_e_corrigir_cromossomo(filho1)
        filho2 = self._validar_e_corrigir_cromossomo(filho2)
        
        return filho1, filho2
    
    def _remove_duplicatas(self, cromossomo: List[Alocacao]) -> List[Alocacao]:
        """Remove alocações duplicadas da mesma disciplina"""
        disciplinas_vistas = set()
        resultado = []
        
        for alocacao in cromossomo:
            if alocacao.disciplina not in disciplinas_vistas:
                resultado.append(alocacao)
                disciplinas_vistas.add(alocacao.disciplina)
        
        return resultado
    
    def mutacao(self, cromossomo: List[Alocacao], taxa_mutacao: float = 0.1) -> List[Alocacao]:
        """Aplica mutação em um cromossomo"""
        cromossomo_mutado = copy.deepcopy(cromossomo)
        
        for i, alocacao in enumerate(cromossomo_mutado):
            if random.random() < taxa_mutacao:
                # Muta o professor
                if random.random() < 0.4:
                    disciplina = next((d for d in self.disciplinas if d.nome == alocacao.disciplina), None)
                    if disciplina:
                        professores_aptos = [p for p in self.professores 
                                           if self.professor_pode_lecionar(p, disciplina)]
                        if professores_aptos:
                            cromossomo_mutado[i].professor = random.choice(professores_aptos).nome
                
                # Muta a sala
                if random.random() < 0.3:
                    disciplina = next((d for d in self.disciplinas if d.nome == alocacao.disciplina), None)
                    if disciplina:
                        salas_disponiveis = [s for s in self.salas 
                                           if not disciplina.laboratorio_necessario or s.laboratorio]
                        if not salas_disponiveis:
                            salas_disponiveis = self.salas
                        cromossomo_mutado[i].sala = random.choice(salas_disponiveis).nome
                
                # Muta os horários
                if random.random() < 0.3:
                    # Coleta horários ocupados por outros
                    outros_horarios_prof = []
                    outros_horarios_sala = []
                    
                    for j, outra_alocacao in enumerate(cromossomo_mutado):
                        if i != j:  # Não incluir a própria alocação
                            if outra_alocacao.professor == alocacao.professor:
                                outros_horarios_prof.extend(outra_alocacao.horarios)
                            if outra_alocacao.sala == alocacao.sala:
                                outros_horarios_sala.extend(outra_alocacao.horarios)
                    
                    novos_horarios = self._alocar_horarios_sem_conflito(outros_horarios_prof, outros_horarios_sala)
                    if novos_horarios:
                        cromossomo_mutado[i].horarios = novos_horarios
        
        return self._validar_e_corrigir_cromossomo(cromossomo_mutado)
    
    def _validar_e_corrigir_cromossomo(self, cromossomo: List[Alocacao]) -> List[Alocacao]:
        """Valida um cromossomo e remove alocações conflitantes rigorosamente"""
        cromossomo_valido = []
        horarios_prof_ocupados = {}
        horarios_sala_ocupados = {}
        horarios_globais_ocupados = set()  # Track all occupied time slots globally
        
        # Ordena por prioridade (disciplinas obrigatórias primeiro)
        disciplinas_dict = {d.nome: d for d in self.disciplinas}
        cromossomo_ordenado = sorted(cromossomo, 
                                   key=lambda a: (not disciplinas_dict.get(a.disciplina, Disciplina("", 0, False)).obrigatoria,
                                                disciplinas_dict.get(a.disciplina, Disciplina("", 0, False)).periodo))
        
        for alocacao in cromossomo_ordenado:
            conflito = False
            
            # Verifica conflitos MÚLTIPLOS
            for horario in alocacao.horarios:
                tupla_horario = (horario.dia, horario.turno, horario.slot)
                
                # Conflito de professor
                if alocacao.professor in horarios_prof_ocupados:
                    if tupla_horario in horarios_prof_ocupados[alocacao.professor]:
                        conflito = True
                        break
                
                # Conflito de sala
                if alocacao.sala in horarios_sala_ocupados:
                    if tupla_horario in horarios_sala_ocupados[alocacao.sala]:
                        conflito = True
                        break
            
            # Se não há conflito, adiciona à solução válida
            if not conflito:
                cromossomo_valido.append(alocacao)
                
                # Registra horários ocupados
                if alocacao.professor not in horarios_prof_ocupados:
                    horarios_prof_ocupados[alocacao.professor] = set()
                if alocacao.sala not in horarios_sala_ocupados:
                    horarios_sala_ocupados[alocacao.sala] = set()
                
                for horario in alocacao.horarios:
                    tupla_horario = (horario.dia, horario.turno, horario.slot)
                    horarios_prof_ocupados[alocacao.professor].add(tupla_horario)
                    horarios_sala_ocupados[alocacao.sala].add(tupla_horario)
                    horarios_globais_ocupados.add(tupla_horario)
        
        return cromossomo_valido
    
    def executar_algoritmo(self, tamanho_populacao: int = 50, num_geracoes: int = 100) -> List[Alocacao]:
        """Executa o algoritmo genético"""
        print("Inicializando algoritmo genético...")
        
        # Cria população inicial
        populacao = []
        for _ in range(tamanho_populacao):
            cromossomo = self.criar_cromossomo()
            populacao.append(cromossomo)
        
        melhor_fitness = 0
        melhor_solucao = None
        
        for geracao in range(num_geracoes):
            # Calcula fitness de toda a população
            fitness_scores = [self.calcular_fitness(cromossomo) for cromossomo in populacao]
            
            # Encontra o melhor da geração
            melhor_idx = np.argmax(fitness_scores)
            if fitness_scores[melhor_idx] > melhor_fitness:
                melhor_fitness = fitness_scores[melhor_idx]
                melhor_solucao = copy.deepcopy(populacao[melhor_idx])
            
            # Seleção por torneio
            nova_populacao = []
            
            # Elitismo - mantém os melhores
            indices_ordenados = np.argsort(fitness_scores)[::-1]
            for i in range(min(5, len(populacao))):  # Top 5
                nova_populacao.append(copy.deepcopy(populacao[indices_ordenados[i]]))
            
            # Gera resto da população
            while len(nova_populacao) < tamanho_populacao:
                # Seleção por torneio
                pai1 = self._selecao_torneio(populacao, fitness_scores)
                pai2 = self._selecao_torneio(populacao, fitness_scores)
                
                # Crossover
                if random.random() < 0.8:  # Taxa de crossover
                    filho1, filho2 = self.crossover(pai1, pai2)
                else:
                    filho1, filho2 = pai1.copy(), pai2.copy()
                
                # Mutação
                filho1 = self.mutacao(filho1)
                filho2 = self.mutacao(filho2)
                
                nova_populacao.extend([filho1, filho2])
            
            # Limita o tamanho da população
            populacao = nova_populacao[:tamanho_populacao]
            
            if geracao % 10 == 0:
                print(f"Geração {geracao}: Melhor fitness = {melhor_fitness}")
        
        print(f"Algoritmo concluído! Melhor fitness: {melhor_fitness}")
        return melhor_solucao
    
    def _selecao_torneio(self, populacao: List[List[Alocacao]], fitness_scores: List[float], tamanho_torneio: int = 3) -> List[Alocacao]:
        """Seleção por torneio"""
        indices_torneio = random.sample(range(len(populacao)), min(tamanho_torneio, len(populacao)))
        melhor_idx = max(indices_torneio, key=lambda i: fitness_scores[i])
        return copy.deepcopy(populacao[melhor_idx])
    
    def imprimir_solucao(self, solucao: List[Alocacao]):
        """Imprime a solução de forma organizada"""
        print("\n" + "="*80)
        print("OFERTA ACADÊMICA - CURSO DE CIÊNCIA DA COMPUTAÇÃO")
        print("="*80)
        
        # Agrupa por período
        disciplinas_por_periodo = {}
        for alocacao in solucao:
            disciplina = next((d for d in self.disciplinas if d.nome == alocacao.disciplina), None)
            if disciplina:
                periodo = disciplina.periodo
                if periodo not in disciplinas_por_periodo:
                    disciplinas_por_periodo[periodo] = []
                disciplinas_por_periodo[periodo].append(alocacao)
        
        for periodo in sorted(disciplinas_por_periodo.keys()):
            print(f"\n{periodo}º PERÍODO:")
            print("-" * 50)
            
            for alocacao in disciplinas_por_periodo[periodo]:
                print(f"\nDisciplina: {alocacao.disciplina}")
                print(f"Professor: {alocacao.professor}")
                print(f"Sala: {alocacao.sala}")
                print("Horários:")
                
                # Agrupa horários por dia
                horarios_por_dia = {}
                for horario in alocacao.horarios:
                    dia = horario.dia
                    if dia not in horarios_por_dia:
                        horarios_por_dia[dia] = []
                    horarios_por_dia[dia].append(f"{horario.turno}{horario.slot}")
                
                for dia, slots in horarios_por_dia.items():
                    print(f"  {dia}: {', '.join(sorted(slots))}")
        
        # Estatísticas
        print(f"\n" + "="*80)
        print("ESTATÍSTICAS E ANÁLISE DA SOLUÇÃO:")
        print("="*80)
        
        print(f"Total de disciplinas alocadas: {len(solucao)}")
        
        # Disciplinas obrigatórias alocadas
        obrigatorias_alocadas = sum(1 for alocacao in solucao 
                                  for disc in self.disciplinas 
                                  if disc.nome == alocacao.disciplina and disc.obrigatoria)
        total_obrigatorias = sum(1 for d in self.disciplinas if d.obrigatoria)
        print(f"Disciplinas obrigatórias alocadas: {obrigatorias_alocadas}/{total_obrigatorias}")
        
        # Verifica conflitos
        conflitos_professor = self._verificar_conflitos_professor(solucao)
        conflitos_sala = self._verificar_conflitos_sala(solucao)
        
        print(f"Conflitos de horário (Professor): {conflitos_professor}")
        print(f"Conflitos de horário (Sala): {conflitos_sala}")
        
        # Uso de laboratórios
        labs_usados = sum(1 for alocacao in solucao 
                         for sala in self.salas 
                         if sala.nome == alocacao.sala and sala.laboratorio)
        print(f"Laboratórios utilizados: {labs_usados} alocações")
        
        # Carga de trabalho dos professores
        disciplinas_por_prof = {}
        for alocacao in solucao:
            prof = alocacao.professor
            if prof not in disciplinas_por_prof:
                disciplinas_por_prof[prof] = 0
            disciplinas_por_prof[prof] += 1
        
        print(f"\nDistribuição de disciplinas por professor:")
        for prof, num_disc in sorted(disciplinas_por_prof.items()):
            print(f"  {prof}: {num_disc} disciplina(s)")
            
        # Professores presentes todos os dias
        prof_horarios = {}
        for alocacao in solucao:
            if alocacao.professor not in prof_horarios:
                prof_horarios[alocacao.professor] = set()
            for horario in alocacao.horarios:
                prof_horarios[alocacao.professor].add(horario.dia)
        
        profs_todos_dias = [prof for prof, dias in prof_horarios.items() if len(dias) == 5]
        print(f"\nProfessores presentes todos os dias da semana: {len(profs_todos_dias)}")
        for prof in profs_todos_dias:
            print(f"  ✓ {prof}")
    
    def _verificar_conflitos_professor(self, solucao: List[Alocacao]) -> int:
        """Conta conflitos de horário de professores"""
        prof_horarios = {}
        for alocacao in solucao:
            if alocacao.professor not in prof_horarios:
                prof_horarios[alocacao.professor] = []
            prof_horarios[alocacao.professor].extend(alocacao.horarios)
        
        conflitos = 0
        for prof, horarios in prof_horarios.items():
            horarios_set = set((h.dia, h.turno, h.slot) for h in horarios)
            if len(horarios_set) != len(horarios):
                conflitos += len(horarios) - len(horarios_set)
        
        return conflitos
    
    def _verificar_conflitos_sala(self, solucao: List[Alocacao]) -> int:
        """Conta conflitos de horário de salas"""
        sala_horarios = {}
        for alocacao in solucao:
            if alocacao.sala not in sala_horarios:
                sala_horarios[alocacao.sala] = []
            sala_horarios[alocacao.sala].extend(alocacao.horarios)
        
        conflitos = 0
        for sala, horarios in sala_horarios.items():
            horarios_set = set((h.dia, h.turno, h.slot) for h in horarios)
            if len(horarios_set) != len(horarios):
                conflitos += len(horarios) - len(horarios_set)
        
        return conflitos

def main():
    """Função principal"""
    print("Iniciando sistema de alocação de horários acadêmicos")
    print("Algoritmo Genético para otimização de grade curricular")
    print("="*60)
    
    scheduler = GeneticScheduler()
    
    # Executa o algoritmo genético
    melhor_solucao = scheduler.executar_algoritmo(
        tamanho_populacao=30,
        num_geracoes=50
    )
    
    if melhor_solucao:
        # Calcula e exibe o fitness final
        fitness_final = scheduler.calcular_fitness(melhor_solucao)
        print(f"\nFitness da melhor solução: {fitness_final}")
        
        # Imprime a solução
        scheduler.imprimir_solucao(melhor_solucao)
    else:
        print("Não foi possível encontrar uma solução válida.")

if __name__ == "__main__":
    main() 
