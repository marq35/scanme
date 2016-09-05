import shutil
import os
import barcode
from barcode.writer import ImageWriter


def generate_barcode(barcode_vaue):
    code39 = barcode.get_barcode_class('code39')
    bc = code39(barcode_vaue, writer=ImageWriter(), add_checksum=False)
    fn = bc.save(barcode_vaue)
    src = '{0}.png'.format(barcode_vaue)
    dst = 'app/static/barcodes/'
    shutil.move(src, dst)


def barcode_file_exists(barcode_value):
    file_path = 'app/static/barcodes/%s' % barcode_value
    if os.path.isfile(file_path):
        return True
    else:
        return False


def delete_barcode(barcode_value):
    file_path = 'app/static/barcodes/%s' % barcode_value
    os.remove(file_path)


if __name__ == '__main__':
    generate_barcode('1234567891111')
