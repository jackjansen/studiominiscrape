import sys
import os
import argparse
from .converter import *

def main():
    parser = argparse.ArgumentParser(description="Scrape StudioMini to local files or GarageBand projects")
    parser.add_argument("-g", "--garageband", action="store_true", help="Create garageband for Mac projects")
    parser.add_argument("-i", "--garagebandios", action="store_true", help="Create garageband for iOS projects")
    parser.add_argument("-v", "--verbose", action="store_true", help="More messages")
    parser.add_argument("url", help="URL from StudioMini (as reported in the app)")
    args = parser.parse_args()
    db = StumiData(verbose=args.verbose)
    db.parse(args.url)
    #db.dump()
    db.scrape()

if __name__ == '__main__':
    main()
    