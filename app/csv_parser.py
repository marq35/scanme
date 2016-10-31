import csv
import os
import re


def get_barcodes(filename):
    barcodes = []
    with open(os.path.join(filename), 'r') as f:
        try:
            reader = csv.reader(f)
            for row in reader:
                m = re.match("\d{8}", row[0])
                barcodes.append(m.group())
        finally:
            f.close()
    return barcodes


if __name__ == '__main__':
    print get_barcodes('barcodelist.csv')