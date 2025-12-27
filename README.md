# crash_clock_starlink
Este projeto em Python estima o tempo médio entre colisões (sem manobras evasivas) entre satélites da constelação Starlink em órbita terrestre baixa (LEO), utilizando dados TLE públicos da Celestrak.

# 🛰️ Starlink Crash Clock Estimator

Este projeto em Python estima o tempo médio entre colisões (sem manobras evasivas) entre satélites da constelação **Starlink** em órbita terrestre baixa (LEO), utilizando dados TLE públicos da Celestrak. A métrica estimada é conhecida como **Crash Clock**, baseada na densidade espacial, na área de colisão efetiva e na velocidade relativa entre objetos.

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&style=flat-square)](https://www.python.org/)
[![MIT License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](./LICENSE)

## 📊 Modelo Teórico

A simulação adota a fórmula aproximada de colisões por unidade de tempo:

\[
\Gamma = n^2 \cdot A_{\text{col}} \cdot V_{\text{rel}} \cdot V_{\text{shell}}
\]

Onde:

- `n` = densidade espacial de satélites (objetos/km³) em uma concha esférica fina  
- `A_col` = área efetiva de colisão (300 m²)  
- `V_rel` = velocidade relativa típica (10 km/s)  
- `V_shell` = volume da concha entre altitudes \( h_1 \) e \( h_2 \)

O **tempo médio entre colisões** (\( \tau \)) é então estimado por:

\[
\tau = \frac{1}{\Gamma_{\text{total}}}
\]

---

##  Funcionamento

O script executa os seguintes passos:

1. **Download dos TLEs** da constelação Starlink diretamente do [Celestrak](https://celestrak.org/NORAD/elements/gp.php?GROUP=starlink).
2. **Extração da altitude orbital média** (semieixo maior – raio da Terra).
3. **Agrupamento em conchas de 1 km** entre 200 e 2000 km.
4. **Cálculo da densidade espacial** e somatório do risco de colisão por concha.
5. **Cálculo do Crash Clock** em dias e horas.

---

## 📁 Estrutura

```
├── crash_clock_starlink.py     # Script principal
├── README.md                   # Este arquivo
└── LICENSE                     # Licença MIT
```

---

##  Requisitos

- Python 3.10+
- Bibliotecas:
  - `numpy`
  - `requests`
  - `sgp4`

Instalação:

```bash
pip install numpy requests sgp4
```

---

##  Execução

Execute o script diretamente:

```bash
python crash_clock_starlink.py
```

Saída esperada (exemplo):

```
Baixando TLEs do grupo Starlink (Celestrak)...
TLEs válidos lidos: 4627 objetos em LEO
CRASH Clock estimado (sem manobras): 5.76 horas
```

---

## 🔬 Observações

- Este modelo **não considera manobras evasivas** realizadas por satélites, como as feitas automaticamente pela constelação Starlink.
- O valor obtido representa um cenário **hipotético de colisão** caso nenhum satélite mude sua trajetória.
- Baseado no artigo *An Orbital House of Cards* (Nature Astronomy, 2023) e em parâmetros típicos de risco orbital.

---

## 📚 Referências

- Celestrak TLE Data: https://celestrak.org/
- SGP4 Python: https://pypi.org/project/sgp4/
- An Orbital House of Cards – *Nature Astronomy* (2023)
- ESA Space Debris Report – https://www.esa.int/Safety_Security/Space_Debris

---

## 👤 Autor

**Rodolfo Milhomem**  
[GitHub – rodolfo-space-force](https://github.com/rodolfo-space-force)  
Especialista em Ciências Aeroespaciais | Engenharia de Computação | Direito Espacial

---

## 📄 Licença

Este projeto está licenciado sob a [Licença MIT](./LICENSE).  
Você pode usar, modificar e redistribuir este código livremente, **desde que mencione o autor original**.
