from __future__ import print_function

import argparse
import boto
import csv
import json
import os
import re
import shutil

from glob import glob
from tempfile import NamedTemporaryFile
from zipfile import ZipFile



class Extractor(object):
    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir


    def extract(self, convert_to_json=True):
        for zfn in glob(os.path.join(self.input_dir, 'FFIEC*.zip')):
            date_match = re.compile('.*(\d{8}).zip').match(zfn)
            date = date_match.groups()[0]
            print('extracting {} reports from {}'.format(date, zfn))

            report_path = os.path.join(self.output_dir, date)
            if not os.path.exists(report_path):
                os.makedirs(report_path)

            count = 0
            with ZipFile(zfn, 'r') as z:
                for fn in z.namelist():
                    if 'Readme.txt' == fn:
                        continue

                    efn = z.extract(fn, report_path)
                    count += 1

                    if convert_to_json:
                        self.convert_to_json(efn)

            print('extracted {} reports to {}'.format(count, report_path))


    def upload_to_s3(self, bucket, path):
        try:
            conn = boto.connect_s3()
            bucket = conn.get_bucket(bucket)
        except Exception:
            print(
                'Could not connect to S3 bucket.\n'
                'Make sure that AWS environment variables are set.\n'
                'AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY'
            )
            return

        for root, directories, filenames in os.walk(self.output_dir):
            for filename in filenames:
                full_filename = os.path.join(root, filename)
                keyname = full_filename.lstrip(self.output_dir)
                k = bucket.new_key(os.path.join(path, keyname))

                print('uploading {} to s3n://{}/{}'.format(
                    full_filename,
                    bucket.name,
                    k.name
                ))
                k.set_contents_from_filename(full_filename, replace=True)


    def convert_to_json(self, filename):
        with NamedTemporaryFile() as tf:
            with open(tf.name, 'wb') as outf:
                with open(filename, 'rb') as inf:
                    reader = csv.reader(
                        inf,
                        delimiter='\t',
                        quoting=csv.QUOTE_NONE
                    )

                    keys = reader.next()

                    if 'Bulk POR' not in filename:
                        keys = reader.next()
                        keys[0] = '"IDRSSD"'

                    for line in reader:
                        d = {k: v for k, v in zip(keys, line)}
                        data = json.dumps(d)
                        outf.write(data + '\n')

            shutil.copyfile(tf.name, filename)



if '__main__' == __name__:
    parser = argparse.ArgumentParser(description='extract archive data')
    parser.add_argument('-i', '--input-dir', help='input archive directory')
    parser.add_argument('-o', '--output-dir', help='output archive directory')
    parser.add_argument('--keep-raw-format', action='store_false',
                        dest='convert_to_json',
                        help='keep raw format (no json conversion)')
    parser.add_argument('--s3-bucket', help='s3 upload bucket (optional)')
    parser.add_argument('--s3-path', help='s3 upload path (optional)',
                        default='')
    args = parser.parse_args()

    extractor = Extractor(args.input_dir, args.output_dir)
    extractor.extract(args.convert_to_json)

    if args.s3_bucket:
        extractor.upload_to_s3(args.s3_bucket, args.s3_path)
