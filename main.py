import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description='EduScrapper: A web scraper for educational websites.')
    parser.add_argument('--module', type=str, help='The module to run scrapping. Available modules: [sive]')
    parser.add_argument('--output', type=str, help='The output file to save the data.')
    args = parser.parse_args()

    if args.module == 'sive':
        from src.sive.sive import Sive
        sive = Sive(output_file=args.output)
        sive.run()
    else:
        print('Module not found.')
        sys.exit(1)

if __name__ == '__main__':
    main()