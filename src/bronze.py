import shutil

from config import BRONZE_DIR, RAW_DIR, TABLES


def run() -> None:
    BRONZE_DIR.mkdir(parents=True, exist_ok=True)
    for table in TABLES:
        source = RAW_DIR / f"{table}.csv"
        if not source.exists():
            raise FileNotFoundError(f"Arquivo de origem nao encontrado: {source}")
        shutil.copy2(source, BRONZE_DIR / source.name)
    print("Camada Bronze criada.")


if __name__ == "__main__":
    run()
