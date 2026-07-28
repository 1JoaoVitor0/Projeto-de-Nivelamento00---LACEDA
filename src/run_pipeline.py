from bronze import run as run_bronze
from gold import run as run_gold
from silver import run as run_silver


def run() -> None:
    run_bronze()
    run_silver()
    run_gold()


if __name__ == "__main__":
    run()
