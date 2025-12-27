#Rodolfo Milhomem
#https://github.com/rodolfo-space-force/

import numpy as np
import requests
from sgp4.api import Satrec

# Parâmetros
R_EARTH = 6371  # km
V_REL = 10      # km/s (velocidade relativa típica)
A_COL = 300e-6  # km² (300 m²)
SHELL_WIDTH = 1 # km
ALT_MIN = 200
ALT_MAX = 2000

def download_starlink_tles():
    url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=starlink&FORMAT=tle"
    response = requests.get(url)
    tle_lines = response.text.strip().splitlines()
    tles = []
    for i in range(0, len(tle_lines) - 2, 3):
        name = tle_lines[i].strip()
        line1 = tle_lines[i+1].strip()
        line2 = tle_lines[i+2].strip()
        tles.append((line1, line2))
    return tles

def get_altitude_km(line1, line2):
    sat = Satrec.twoline2rv(line1, line2)
    a = sat.a  # semi-eixo maior em unidades do raio da Terra
    if a is None:
        return None
    a_km = a * 6378.135
    alt_km = a_km - R_EARTH
    return alt_km

def compute_crash_clock(altitudes):
    bins = np.arange(ALT_MIN, ALT_MAX + SHELL_WIDTH, SHELL_WIDTH)
    counts, _ = np.histogram(altitudes, bins)
    Gamma_total = 0

    for i in range(len(bins) - 1):
        h1 = bins[i]
        h2 = bins[i + 1]
        R1 = R_EARTH + h1
        R2 = R_EARTH + h2
        # Volume da concha esférica fina (evita overflow)
        V_shell = 4 * np.pi * ((R1 + R2) / 2)**2 * (R2 - R1)
        n = counts[i] / V_shell  # objetos/km³
        Gamma_total += (n**2) * A_COL * V_REL * V_shell

    tau_sec = 1 / Gamma_total if Gamma_total > 0 else float("inf")
    tau_days = tau_sec / (60 * 60 * 24)
    tau_hours = tau_sec / 3600
    return tau_days, tau_hours

if __name__ == "__main__":
    print("Baixando TLEs do grupo Starlink (Celestrak)...")
    tles = download_starlink_tles()

    altitudes = []
    for line1, line2 in tles:
        try:
            alt = get_altitude_km(line1, line2)
            if alt and ALT_MIN <= alt <= ALT_MAX:
                altitudes.append(alt)
        except:
            continue

    print(f"TLEs válidos lidos: {len(altitudes)} objetos em LEO")
    tau_days, tau_hours = compute_crash_clock(np.array(altitudes))
    print(f"CRASH Clock estimado (sem manobras): {tau_hours:.2f} horas")

# Licença
#Este projeto está licenciado sob a **Licença MIT**.  
#Você pode usar, modificar e redistribuir este código livremente, **desde que mencione o autor original**.
