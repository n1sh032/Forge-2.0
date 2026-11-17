import argparse
import json

from src.agents.architect import Architect


def main():
    parser = argparse.ArgumentParser(description="Draft a Forge plan for review")
    parser.add_argument("task")
    args = parser.parse_args()
    print(json.dumps(Architect().run(args.task), indent=2))


if __name__ == "__main__":
    main()
