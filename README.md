# ⚡ Simulador de Otimização de Carregamento de Veículos Elétricos

![Python](https://img.shields.io/badge/python-3.x-blue)
![Type](https://img.shields.io/badge/type-simulation-orange)
![Status](https://img.shields.io/badge/status-academic-green)

---

## 🧠 Sobre o Projeto

Este projeto simula diferentes cenários de uso de carregadores para veículos elétricos, com o objetivo de avaliar estratégias de **otimização de tempo, redução de ociosidade e melhoria na eficiência da infraestrutura**.

A simulação foi desenvolvida como validação prática de uma solução de **orquestração inteligente de carregadores**, integrando conceitos de:

- Gestão de filas
- Comportamento do usuário
- Uso eficiente de energia
- Integração entre software e hardware

---

## 🎯 Objetivo

Demonstrar, por meio de simulação computacional, como diferentes abordagens impactam:

- ⏱️ Tempo médio de espera  
- 🔌 Ociosidade dos carregadores  
- ⚡ Eficiência do sistema  

---

## ⚙️ O que o simulador faz

O sistema modela um ambiente realista com:

- Chegada dinâmica de veículos (com picos de demanda)
- Múltiplos carregadores simultâneos
- Tempo de recarga variável
- Atrasos na liberação da vaga (ociosidade)
- Comportamento dos usuários:
  - prioridade
  - reservas

---

## 🧪 Cenários simulados

O simulador compara diferentes níveis de solução:

- ❌ **Sem sistema (baseline)**
- 💻 **Apenas software**
- 🔌 **Apenas hardware**
- 🔗 **Hardware + software**
- ➕ **Hardware + expansão de carregadores**
- 🚀 **Sistema completo (orquestração total)**

---

## 📊 Parâmetros da simulação

- 🚗 **70 veículos por execução**
- 🔌 **6 carregadores base (+2 em expansão)**
- 🔁 **5 execuções por cenário (média dos resultados)**

### ⏱️ Modelagem:
- Tempo de recarga: **40 a 70 minutos**
- Ociosidade: **0 a 20 minutos**
- Intervalo entre chegadas:
  - Pico: 2–6 min  
  - Normal: 5–12 min  

---

## 📈 Resultados

A simulação demonstrou melhorias significativas:

- 🔻 Até **80% de redução no tempo de espera**
- 🔻 Até **80% de redução na ociosidade**
- 📊 Maior eficiência ao combinar:
  - software
  - hardware
  - expansão de infraestrutura

---

## 🧩 Diferenciais do modelo

- Integração entre sistema digital e ambiente físico  
- Simulação de comportamento real do usuário  
- Avaliação de impacto de hardware na eficiência  
- Modelagem de cenários escaláveis  

---

## 🔬 Metodologia

Os resultados foram obtidos através de simulações com múltiplos cenários, utilizando médias de execuções para reduzir variações aleatórias.

---

## 🚀 Próximos passos

- Desenvolvimento de protótipo com **Arduino**
- Implementação de comunicação via **BLE**
- Criação de um sistema básico (**CRUD**) para controle de carregadores
- Integração entre hardware e software

---

## 💻 Tecnologias utilizadas

- Python (simulação)
- GitHub (versionamento)

---

## 📂 Como executar

```bash
python nome_do_arquivo.py
