import os
import hashlib
import pandas as pd

os.makedirs("datos", exist_ok=True)

if os.path.exists(os.path.join("datos", "telemetria_envios.csv")):
    ruta_original = os.path.join("datos", "telemetria_envios.csv")
elif os.path.exists("telemetria_envios.csv"):
    ruta_original = "telemetria_envios.csv"
else:
    raise FileNotFoundError("No se encuentra telemetria_envios.csv en la carpeta actual ni dentro de 'datos'.")

ruta_limpia = os.path.join("datos", "telemetria_limpia.csv")

def calcular_sha256(ruta):
    sha = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(4096), b""):
            sha.update(bloque)
    return sha.hexdigest()

df = pd.read_csv(ruta_original)
hash_original = calcular_sha256(ruta_original)
print(f"Total registros originales: {len(df)}")
print(f"SHA-256 (original): {hash_original}")

condicion_invalida = (
    df.isnull().any(axis=1) |
    df.duplicated() |
    (df['peso_kg'] <= 0) |
    (df['temp_celsius'] < -20) |
    (df['temp_celsius'] > 50) |
    (df['estado_envio'] == 'DESCONOCIDO_ERROR')
)

df_limpio = df[~condicion_invalida].copy()

df_limpio.to_csv(ruta_limpia, index=False)
hash_limpio = calcular_sha256(ruta_limpia)

print(f"Registros depurados: {len(df_limpio)} (se descartaron {len(df) - len(df_limpio)} registros corruptos)")
print(f"SHA-256 (limpio):    {hash_limpio}")
