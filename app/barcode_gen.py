import shutil
import barcode
from barcode.writer import ImageWriter


def generate_barcode(barcode_vaue):
    # EAN = barcode.get_barcode_class('ean13')
    # bc = EAN(barcode_vaue, writer=ImageWriter(), add_checksum=False)
    # bc.save(barcode_vaue)

    code39 = barcode.get_barcode_class('code39')
    bc = code39(barcode_vaue, writer=ImageWriter(), add_checksum=False)
    fn = bc.save(barcode_vaue)
    src = '{0}.png'.format(barcode_vaue)
    dst = 'app/static/barcodes/'
    shutil.move(src, dst)


if __name__ == '__main__':
    generate_barcode('1234567891111')
