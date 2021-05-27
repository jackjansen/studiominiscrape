import sys
import os
import argparse
from .converter import *

def main():
    parser = argparse.ArgumentParser(description="Scrape StudioMini to local files or GarageBand projects")
    #parser.add_argument("-g", "--garageband", action="store_true", help="Create garageband for Mac projects")
    parser.add_argument("-i", "--garagebandios", action="store_true", help="Create garageband for iOS projects")
    parser.add_argument("-v", "--verbose", action="store_true", help="More messages")
    parser.add_argument("-o", "--output", action="store", default=".", help="Output directory (default: currnt directory)")
    parser.add_argument("url", help="URL from StudioMini (as reported in the app)")
    args = parser.parse_args()
    
    db = StumiData(verbose=args.verbose)
    if args.garagebandios:
        package_dir = os.path.dirname(__file__)
        data_dir = os.path.join(package_dir, 'templates')
        template = os.path.join(data_dir, 'GBios.band')
        db.set_template(template)
    db.parse(args.url)
    
    db.scrape(args.output)

if __name__ == '__main__':
    main()
    