from src.FIM import FIM


def main() -> None:
    try:
        fim = FIM()
        fim.run()
    except KeyboardInterrupt:
        print('\nSaliendo del programa...')

if __name__ == "__main__": main()