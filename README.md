# MC714 - Heurísticas (Esqueleto)

Este repositório contém um esqueleto simples em Python para implementar heurísticas
(metaheurísticas ou construtivas) para o Trabalho 1.

## Estrutura
```
python/
  problem.py          # Modelo de definição do problema
  solution.py         # Representação imutável de solução
  heuristics/
    base.py           # Classe base para heurísticas
    random_choice.py  # Heurística de escolha aleatória
  main.py             # CLI para executar
  tests/
    test_random.py    # Teste básico
  pyproject.toml
```

## Executar
Instale dependências de desenvolvimento (pytest opcional):
```
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

Execute a heurística (arquivo de entrada fictício):
```
python -m python.main data/exemplo.txt --iters 500 --seed 123
```
Ajuste `build_problem_from_file` em `main.py` para interpretar o formato real.

## Próximos Passos
- Implementar avaliação real em `Problem.evaluate`.
- Definir geração de vizinhança específica.
- Adicionar limite de tempo e métricas.
- Incluir logging estruturado.
