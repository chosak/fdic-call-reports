import logging, optparse, os, re
from boto.s3.connection import S3Connection
from glob import glob
from zipfile import ZipFile


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


S3_BUCKET = 'fdic-call-reports'
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']


def run(source_directory):
    '''
    Given a directory of downloaded call report archives (in .ZIP form),
    extract and upload individual raw TSV files to an S3 bucket.
    '''
    bucket = s3_bucket()
    logger.info('writing to s3 bucket {}'.format(bucket.name))

    for zf in glob(os.path.join(source_directory, 'FFIEC*.zip')):
        logger.info('extracting {}'.format(zf))
        with ZipFile(zf, 'r') as z:
            for fn in z.namelist():
                pattern = 'FFIEC CDR Call (Bulk|Schedule) (\w+) (\d{8}).*.txt'
                match = re.compile(pattern).match(fn)

                if not match or 3 > len(match.groups()):
                    continue

                report_type = '{}-{}'.format(*match.groups()[:2]).lower()
                report_date = 'report_date={}'.format(match.group(3))

                s3_key = os.path.join(report_type, report_date, fn)
                k = bucket.new_key(s3_key)

                logger.info('uploading to {}'.format(k.name))
                contents = z.read(fn)
                k.set_contents_from_string(contents)


def s3_bucket():
    conn = S3Connection(
        AWS_ACCESS_KEY_ID,
        AWS_SECRET_ACCESS_KEY
    )
   
    return conn.get_bucket(S3_BUCKET, validate=False)


if __name__ == '__main__':
    parser = optparse.OptionParser()

    parser.add_option(
        '-d', '--dir',
        dest='source_directory', 
        help='local directory path with call report archives to upload')

    opts, args = parser.parse_args()

    run(*args, **vars(opts))
