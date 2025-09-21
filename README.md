## Documentação e Relatório - Balanceador de Carga

### 1. Instruções de Execução

**Pré-requisitos:**  
- Python 3.x instalado  

**Passos para executar:**

1. **Inicie os servidores** (em três terminais separados):
   ```bash
   python server0.py
   python server1.py
   python server2.py
   ```

2. **Inicie o balanceador de carga** (escolha a política: `random`, `round robin`, `shortest queue`):
   ```bash
   python load_balancer.py "random"
   # ou
   python load_balancer.py "round robin"
   # ou
   python load_balancer.py "shortest queue"
   ```

3. **Execute o cliente** (fluxo normal ou rajada):
   ```bash
   python client.py
   python burst_client.py
   ```

---

### 2. Estrutura do Código

- `server0.py`, `server1.py`, `server2.py`: Simulam servidores, cada um com fila de requisições e atraso variável conforme o tipo de pedido.
- `load_balancer.py`: Implementa o balanceador de carga, alternando entre três políticas e registrando métricas globais.
- `client.py`: Simula tráfego normal, com intervalos aleatórios entre requisições.
- `burst_client.py`: Simula rajadas de requisições para testar o sistema sob carga intensa.

---

### 3. Escolhas de Projeto

- **Sockets TCP:** Utilizados para comunicação entre cliente, balanceador e servidores, simulando um ambiente realista.
- **Fila de requisições:** Cada servidor mantém uma lista para simular processamento sequencial.
- **Logs:** Todas as estruturas: cliente, servidor e balanceador de carga possuem logs que permitem entender o que está acontecendo em tempo real 
- **Atraso variável:** O tempo de processamento depende do tipo de requisição, tornando o teste mais próximo do real.
- **Métricas globais:** O balanceador registra tempo médio de resposta, throughput e distribuição de carga por servidor.
- **Políticas configuráveis:** O usuário pode alternar facilmente entre as políticas via argumento de linha de comando.

---

### 4. Como Testar o Balanceador

- Execute os servidores e o balanceador conforme instruções acima.
- Use `client.py` para tráfego constante e `burst_client.py` para rajadas.
- Observe os logs do balanceador para ver as métricas e distribuição de carga.
- Troque a política do balanceador e compare os resultados.

---

### 5. Análise dos Resultados

- **Random:** Distribui as requisições de forma uniforme, mas pode sobrecarregar servidores em rajadas.
- **Round Robin:** Garante distribuição sequencial, útil para cargas constantes.
- **Shortest Queue:** Equilibra melhor em cenários de rajada, evitando filas longas em um único servidor.
- **Métricas:** O tempo médio de resposta e a vazão variam conforme a política e o padrão de tráfego. Em rajadas, a política de fila mais curta tende a apresentar melhor desempenho.
