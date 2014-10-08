from boto.dynamodb2 import types
from django.core.management.base import BaseCommand

from reports.dynamo import DynamoTable


class Command(BaseCommand):
    help = 'Create DynamoDB tables for processed call report data'


    def handle(self, *args, **options):
        DynamoTable('banks').create('name', types.STRING, 11, 5) 
