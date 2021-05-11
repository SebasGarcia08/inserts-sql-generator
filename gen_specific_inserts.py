from src import SpecificDBPopulator
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Oracle SQL generator for "Modelado TP3" specific DDL.')
    parser.add_argument('-n', '--number-occurrences', type=int,
                        help='Minimum number of occurrences in each table')
    parser.add_argument('-out', '--output-file', default=None, type=str,
                        help='Output *.sql file where to save the inserts')

    args = parser.parse_args()
    db_pop = SpecificDBPopulator(2 * args.number_occurrences, args.output_file)
    db_pop.generate_inserts()
