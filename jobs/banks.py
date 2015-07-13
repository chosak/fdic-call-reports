import mrjob.compat
import mrjob.conf
import mrjob.job
import mrjob.protocol
import mrjob.step
import os
import re



class BankMetadataJob(mrjob.job.MRJob):
    INPUT_PROTOCOL = mrjob.protocol.JSONValueProtocol
    OUTPUT_PROTOCOL = mrjob.protocol.JSONValueProtocol


    def steps(self):
        return [
            mrjob.step.MRStep(
                mapper=self.mapper,
                reducer=self.date_reducer
            ),
            mrjob.step.MRStep(
                reducer=self.bank_reducer
            ),
        ]


    def mapper(self, _, row):
        bank_id = row.pop('"IDRSSD"', None)

        if bank_id is None:
            self.increment_counter('mapper', 'no_id')
            return

        filename = mrjob.compat.get_jobconf_value('map.input.file')                      

        if 'Bulk POR' in filename:
            data = self.get_bank_info(row)
        elif 'Schedule RC ' in filename:
            data = self.get_balance_sheet_info(row)
        else:
            raise ValueError('unsupported filename: {}'.format(filename))

        date = self.get_filename_date(filename)

        yield (bank_id, date), data


    def get_filename_date(self, filename):
        filename = os.path.basename(filename)
        pattern = (
            'FFIEC CDR Call (Bulk|Schedule) (\w+) (\d{8})(\(\d+ of \d+\))?.txt'
        )
        match = re.compile(pattern).match(filename)

        if not match or 3 > len(match.groups()):
            raise ValueError('bad filename: {}'.format(filename))

        return match.group(3)


    def get_bank_info(self, row):
        return {
            'name': row['Financial Institution Name'],
            'address': row['Financial Institution Address'],
            'city': row['Financial Institution City'],
            'state': row['Financial Institution State'],
            'zip': row['Financial Institution Zip Code'],
        }


    def get_balance_sheet_info(self, row):
        return {
            'assets': row['TOTAL ASSETS'],
            'deposits': row['TOTAL DEPOSITS'],
            'liabilities': row['TOTAL LIABILITIES'],
        }


    def date_reducer(self, map_key, rows):
        bank_id, date = map_key

        data = mrjob.conf.combine_dicts(*rows)
        data['date'] = date

        yield bank_id, data


    def bank_reducer(self, bank_id, rows):
        data = {
            'IDRSSD': bank_id,
            'reports': sorted(rows, key=lambda r: r['date'])
        }

        self.increment_counter('banks', 'output')
        yield bank_id, data



if __name__ == '__main__':
    # Usage: python jobs/banks.py \
    #     input/*/*Bulk*.txt
    #     input/*/*RC\ *.txt
    # > output.txt
    BankMetadataJob.run()
