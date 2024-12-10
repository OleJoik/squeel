import argparse


def squeel():
    parser = argparse.ArgumentParser(description="Squeel")
    parser.add_argument("--name", type=str, help="Your name")
    args = parser.parse_args()

    name = args.name or "World"
    print(f"Hello, {name}!")
