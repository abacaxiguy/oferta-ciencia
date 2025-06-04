# Algoritmo Genético para Alocação de Horários Acadêmicos

Este projeto implementa um **Algoritmo Genético** para resolver o problema de alocação de horários acadêmicos do curso de Ciência da Computação, conforme especificado no `projeto.txt`.

## 📋 Descrição do Problema

O sistema deve criar uma oferta acadêmica otimizada respeitando as seguintes restrições:

### Restrições Obrigatórias:
- ✅ Professor não pode estar em mais de uma disciplina no mesmo horário
- ✅ Sala não pode ser alocada para mais de uma disciplina no mesmo horário  
- ✅ Considerar carga horária e formação do professor
- ✅ Professores dos 4 primeiros períodos podem lecionar qualquer disciplina desses períodos
- ✅ Disciplinas avançadas requerem especialização específica do professor
- ✅ Laboratórios preferencialmente para disciplinas de programação
- ✅ Professor deve ter pelo menos 1 e no máximo 3 disciplinas por semestre
- ✅ Priorizar disciplinas obrigatórias
- ✅ Professores devem ir ao IC todos os dias (restrição Torres)

## 🧬 Algoritmo Genético - Componentes

### 1. **Representação (Cromossomo)**
Cada solução é representada como uma lista de `Alocacao`, onde cada alocação contém:
- Professor responsável
- Disciplina a ser ministrada  
- Sala onde ocorrerá
- Horários (4 slots por disciplina)

### 2. **Função de Fitness**
A função de fitness avalia a qualidade de cada solução considerando:
- **Penalidades** (-100 pontos): Conflitos de horário de professor/sala
- **Penalidades** (-50 pontos): Professor com mais de 3 disciplinas
- **Bonificações** (+10 pontos): Cada disciplina obrigatória alocada
- **Bonificações** (+20 pontos): Professor presente todos os dias
- **Bonificações** (+5 pontos): Uso adequado de laboratórios

### 3. **Operadores Genéticos**

#### **Seleção**: Torneio (tamanho 3)
#### **Crossover**: Ponto único com remoção de duplicatas
#### **Mutação**: Taxa de 10% com três tipos:
- Trocar professor (40% chance)
- Trocar sala (30% chance)  
- Trocar horários (30% chance)

### 4. **Elitismo**
Mantém os 5 melhores indivíduos a cada geração.

## 🚀 Como Executar

### Pré-requisitos
```bash
pip install -r requirements.txt
```

### Execução
```bash
python genetic_algorithm_scheduler.py
```

## 📊 Parâmetros do Algoritmo

- **População**: 30 indivíduos
- **Gerações**: 50 
- **Taxa de Crossover**: 80%
- **Taxa de Mutação**: 10%
- **Elitismo**: Top 5

## 📈 Saída do Sistema

O sistema exibe:

1. **Progresso**: Fitness da melhor solução a cada 10 gerações
2. **Oferta Acadêmica**: Organizada por período com:
   - Disciplina e professor responsável
   - Sala alocada
   - Horários por dia da semana
3. **Estatísticas**:
   - Total de disciplinas alocadas
   - Disciplinas obrigatórias cobertas
   - Distribuição de carga por professor

## 🎯 Dados do Problema

### Professores: 44
Incluindo especialistas como Alan Pedro (Estrutura de Dados), Bruno Pimentel (Algoritmos), etc.

### Disciplinas: 29 obrigatórias
Distribuídas do 1º ao 8º período, incluindo ACEs e disciplinas de programação.

### Salas: 14 disponíveis
- 9 salas de aula tradicionais
- 5 laboratórios para disciplinas práticas

### Horários: 60 slots
- Manhã: M1-M6 (07:30-12:50)
- Tarde: T1-T6 (13:30-18:50)
- 5 dias da semana

## 🔧 Customização

Para ajustar parâmetros do algoritmo, modifique os valores na função `main()`:

```python
melhor_solucao = scheduler.executar_algoritmo(
    tamanho_populacao=30,    # Altere aqui
    num_geracoes=50          # Altere aqui
)
```

## 📝 Estrutura do Código

- `genetic_algorithm_scheduler.py`: Implementação principal
- `requirements.txt`: Dependências do projeto
- `projeto.txt`: Especificação original do problema
- `README.md`: Esta documentação

## ⚡ Características Técnicas

- **Linguagem**: Python 3.7+
- **Paradigma**: Computação Evolucionária 
- **Complexidade**: O(P × G × F) onde P=população, G=gerações, F=fitness
- **Tempo de Execução**: ~30-60 segundos (dependendo do hardware)

## 🎓 Contexto Acadêmico

Este projeto foi desenvolvido no contexto da disciplina de **Computação Evolucionária**, aplicando conceitos de:
- Algoritmos Genéticos
- Otimização Combinatória
- Problemas de Scheduling/Timetabling
- Técnicas de Seleção, Crossover e Mutação

---

**Equipe**: Implementação baseada na especificação para o curso de Ciência da Computação - UFAL 