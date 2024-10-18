import argparse
from src.project.core import Project

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    args = parser.parse_args()

    project = Project(args.input, args.output)
    project.process()
