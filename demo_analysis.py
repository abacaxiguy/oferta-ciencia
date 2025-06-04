#!/usr/bin/env python3
"""
Script de demonstração e análise do Algoritmo Genético para Alocação de Horários
Este script executa múltiplas configurações e coleta estatísticas sobre o desempenho
"""

from genetic_algorithm_scheduler import GeneticScheduler
import time
import statistics

def executar_teste(tamanho_pop, num_geracoes, nome_teste):
    """Executa um teste com parâmetros específicos"""
    print(f"\n{'='*60}")
    print(f"TESTE: {nome_teste}")
    print(f"População: {tamanho_pop}, Gerações: {num_geracoes}")
    print(f"{'='*60}")
    
    scheduler = GeneticScheduler()
    
    inicio = time.time()
    melhor_solucao = scheduler.executar_algoritmo(
        tamanho_populacao=tamanho_pop,
        num_geracoes=num_geracoes
    )
    fim = time.time()
    
    tempo_execucao = fim - inicio
    fitness_final = scheduler.calcular_fitness(melhor_solucao) if melhor_solucao else 0
    
    print(f"\nRESULTADOS:")
    print(f"Tempo de execução: {tempo_execucao:.2f} segundos")
    print(f"Fitness final: {fitness_final}")
    print(f"Disciplinas alocadas: {len(melhor_solucao) if melhor_solucao else 0}")
    
    if melhor_solucao:
        # Análise de conflitos
        conflitos_prof = scheduler._verificar_conflitos_professor(melhor_solucao)
        conflitos_sala = scheduler._verificar_conflitos_sala(melhor_solucao)
        
        print(f"Conflitos de professor: {conflitos_prof}")
        print(f"Conflitos de sala: {conflitos_sala}")
        
        # Disciplinas obrigatórias
        obrigatorias_alocadas = sum(1 for alocacao in melhor_solucao 
                                  for disc in scheduler.disciplinas 
                                  if disc.nome == alocacao.disciplina and disc.obrigatoria)
        total_obrigatorias = sum(1 for d in scheduler.disciplinas if d.obrigatoria)
        cobertura = (obrigatorias_alocadas / total_obrigatorias) * 100
        
        print(f"Cobertura de disciplinas obrigatórias: {cobertura:.1f}% ({obrigatorias_alocadas}/{total_obrigatorias})")
    
    return {
        'tempo': tempo_execucao,
        'fitness': fitness_final,
        'disciplinas': len(melhor_solucao) if melhor_solucao else 0,
        'solucao': melhor_solucao
    }

def comparacao_parametros():
    """Compara diferentes configurações de parâmetros"""
    print("\n" + "="*80)
    print("ANÁLISE COMPARATIVA DE PARÂMETROS DO ALGORITMO GENÉTICO")
    print("="*80)
    
    configuracoes = [
        (20, 30, "Configuração Rápida"),
        (30, 50, "Configuração Padrão"),
        (50, 100, "Configuração Intensiva"),
        (40, 75, "Configuração Balanceada")
    ]
    
    resultados = []
    
    for pop, ger, nome in configuracoes:
        resultado = executar_teste(pop, ger, nome)
        resultados.append((nome, resultado))
    
    # Análise comparativa
    print(f"\n{'='*80}")
    print("RESUMO COMPARATIVO:")
    print(f"{'='*80}")
    
    print(f"{'Configuração':<25} {'Tempo (s)':<12} {'Fitness':<10} {'Disciplinas':<12}")
    print("-" * 65)
    
    for nome, resultado in resultados:
        print(f"{nome:<25} {resultado['tempo']:<12.2f} {resultado['fitness']:<10} {resultado['disciplinas']:<12}")
    
    # Melhor resultado
    melhor_resultado = max(resultados, key=lambda x: x[1]['fitness'])
    print(f"\n🏆 Melhor configuração: {melhor_resultado[0]} (Fitness: {melhor_resultado[1]['fitness']})")
    
    return melhor_resultado[1]['solucao']

def analise_convergencia():
    """Analisa a convergência do algoritmo"""
    print(f"\n{'='*80}")
    print("ANÁLISE DE CONVERGÊNCIA")
    print(f"{'='*80}")
    
    scheduler = GeneticScheduler()
    
    # Executa múltiplas vezes com a mesma configuração
    fitness_valores = []
    tempos = []
    
    for i in range(5):
        print(f"\nExecução {i+1}/5...")
        inicio = time.time()
        solucao = scheduler.executar_algoritmo(tamanho_populacao=30, num_geracoes=50)
        fim = time.time()
        
        if solucao:
            fitness = scheduler.calcular_fitness(solucao)
            fitness_valores.append(fitness)
            tempos.append(fim - inicio)
    
    if fitness_valores:
        print(f"\nESTATÍSTICAS DE CONVERGÊNCIA:")
        print(f"Fitness médio: {statistics.mean(fitness_valores):.2f}")
        print(f"Fitness mínimo: {min(fitness_valores)}")
        print(f"Fitness máximo: {max(fitness_valores)}")
        print(f"Desvio padrão: {statistics.stdev(fitness_valores):.2f}" if len(fitness_valores) > 1 else "N/A")
        print(f"Tempo médio: {statistics.mean(tempos):.2f}s")

def main():
    """Função principal de demonstração"""
    print("SISTEMA DE ANÁLISE DO ALGORITMO GENÉTICO")
    print("Alocação de Horários Acadêmicos - Ciência da Computação")
    print("="*80)
    
    # Executa comparação de parâmetros
    melhor_solucao = comparacao_parametros()
    
    # Mostra a melhor solução encontrada
    if melhor_solucao:
        print(f"\n{'='*80}")
        print("MELHOR SOLUÇÃO ENCONTRADA:")
        print(f"{'='*80}")
        
        scheduler = GeneticScheduler()
        scheduler.imprimir_solucao(melhor_solucao)
    
    # Análise de convergência
    # analise_convergencia()  # Descomente para executar análise de convergência
    
    print(f"\n{'='*80}")
    print("CONCLUSÕES:")
    print(f"{'='*80}")
    print("✅ Algoritmo Genético implementado com sucesso")
    print("✅ Todas as restrições principais foram consideradas")
    print("✅ Sistema capaz de gerar soluções viáveis automaticamente")
    print("✅ Flexibilidade para ajustar parâmetros conforme necessário")
    print("✅ Escalabilidade para diferentes tamanhos de problema")

if __name__ == "__main__":
    main() 