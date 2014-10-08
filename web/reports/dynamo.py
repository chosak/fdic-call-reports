import logging, os
from boto import dynamodb2
from boto.dynamodb2.fields import HashKey
from boto.dynamodb2.table import Table


logger = logging.getLogger(__name__)


class DynamoTable(object):
    '''
    Class that represents an Amazon DynamoDB table.
    '''
    def __init__(self, name):
        self.name = name
        self.connection = dynamodb2.connect_to_region('us-east-1')


    def __unicode__(self):
        return unicode(self.name)


    def create(self, hash_key_name, hash_key_type, read_tp, write_tp):
        hash_key = HashKey(hash_key_name, data_type=hash_key_type)
        schema = [hash_key]

        throughput = {
            'read': read_tp,
            'write': write_tp,
        }

        logger.info('creating dynamodb table {}'.format(self.name))
        Table.create(
            self.name,
            schema=schema,
            throughput=throughput,
            connection=self.connection
        )


    def get_table(self):
        return Table(self.name, connection=self.connection)


    def delete(self):
        logger.info('deleting dynamodb table {}'.format(self.name))
        self.get_table().delete()
