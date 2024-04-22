import argparse

from processor.services import ProcessorService

parser = argparse.ArgumentParser(prog='start.py', description='my panorama stitch program')
parser.add_argument('folder', nargs='+', help='folder containing files to stitch', type=str)
parser.add_argument('--output', default='panorama.jpg', help='File name of the output file.', type=str,
                    dest='output')

__doc__ = '\n' + parser.format_help()

args = parser.parse_args()

ProcessorService(None, None).process(args.folder[0], args.output)

if __name__ == '__main__':
    pass
