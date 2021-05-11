from src import SpecificDBPopulator
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Oracle SQL generator.')
    parser.add_argument('--number-of-occurrences')