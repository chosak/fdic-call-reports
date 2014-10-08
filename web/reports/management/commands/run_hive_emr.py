import logging, os
from boto import emr, s3
from boto.emr.step import HiveStep, InstallHiveStep
from boto.s3.key import Key
from django.core.management.base import BaseCommand
from optparse import make_option


logger = logging.getLogger(__name__)


class HiveRunner(object):
    def __init__(self):
        self.key_path = 'hive'
        self.s3_conn = s3.connect_to_region('us-east-1')
        self.emr_conn = emr.connect_to_region('us-east-1')

        self.scripts = [
            'bulk_por.hql',
            'banks.hql',
        ]


    def upload_scripts_to_s3(self, script_path, script_bucket):
        bucket = self.s3_conn.get_bucket(script_bucket)
        for script in self.scripts:
            self.upload_script_to_s3(script_path, bucket, script)


    def upload_script_to_s3(self, script_path, bucket, script):
        key_name = os.path.join(self.key_path, script)
        k = bucket.new_key(key_name)
        filename = os.path.join(script_path, script)

        logger.info('uploading {} to s3://{}'.format(
            filename,
            os.path.join(bucket.name, key_name)
        ))
                
        k.set_contents_from_filename(filename)


    def run_scripts(self, script_bucket, keyname, log_bucket=None):
        steps = [
            InstallHiveStep(),
        ]

        for script in self.scripts:
            s3_path = 's3://' + os.path.join(
                script_bucket,
                self.key_path,
                script
            )

            steps.append(HiveStep(script, s3_path))

        logger.info('starting EMR jobflow')
        jobflow = self.emr_conn.run_jobflow(
            'Hive scripts',
            log_uri='s3n://' + log_bucket,
            ami_version='latest',
            ec2_keyname=keyname,
            master_instance_type='m1.medium',
            slave_instance_type='m1.medium',
            num_instances=2,
            enable_debugging=bool(log_bucket),
            steps=steps,
            job_flow_role='EMR_EC2_DefaultRole',
            service_role='EMR_DefaultRole',
            visible_to_all_users=True
        ) 
        logger.info('started EMR jobflow {}'.format(jobflow))



class Command(BaseCommand):
    help = 'Run Hive scripts on Elastic MapReduce to process call report data'


    option_list = BaseCommand.option_list + (
        make_option(
            '-s', '--script-path',
            dest='script_path',
            help='full local path to Hive scripts'
        ),
        make_option(
            '-b', '--bucket',
            dest='script_bucket',
            help='S3 bucket to copy Hive scripts to'
        ),
        make_option(
            '-k', '--keyname',
            dest='keyname',
            help='EC2 key to use for EMR instances'
        ),
        make_option(
            '-l', '--log-bucket',
            dest='log_bucket',
            default=None,
            help='S3 bucket to log Hive execution to (optional)'
        ),
    )


    def handle(self, *args, **options):
        script_path = options['script_path']
        script_bucket = options['script_bucket']
        keyname = options['keyname']
        log_bucket = options['log_bucket']

        runner = HiveRunner()
        runner.upload_scripts_to_s3(script_path, script_bucket)
        runner.run_scripts(script_bucket, keyname, log_bucket)
