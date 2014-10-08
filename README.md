All banks regulated by the FDIC are required to file quarterly financial reports to regulators, known colloquially as "[call reports](http://en.wikipedia.org/wiki/Call_report)". This data is made publically available [by the FFIEC](https://cdr.ffiec.gov/public/), but the data is difficult to download efficiently and hard to analyze in aggregate.

This project aims to simplify data access and open up new methods for analysis. Goals include:

- easily download all available call report data without repetitive browsing/clicking
- collect and organize data by report type
- process data efficiently using [Apache Hive](https://hive.apache.org) and [Elastic MapReduce](http://aws.amazon.com/elasticmapreduce/)
- store processed data in a NoSQL [DynamoDB](http://aws.amazon.com/dynamodb/) database
- expose stored data in a protoype [Django](https://www.djangoproject.com) web application using [Elasticache](http://aws.amazon.com/elasticache/) for improved performance

#### Downloading raw call report data

The `download_all_reports.py` script uses [Selenium](http://www.seleniumhq.org) to iteratively download all available single quarterly call report available through the [FFIEC download site](https://cdr.ffiec.gov/public/). See the comments in that script for instructions on how to setup Selenium locally.

Files downloaded from this script are stored in their original archive format (zip).

#### Archiving call report data

The `upload_reports_to_s3.py` script extracts all raw text files from the downloaded call report archives and stores them in a bucket on S3. Files are organized first by report type (Schedule RC, Schedule RI, etc.) and then partitioned by report date.

#### Running Hive scripts

The `hive` subdirectory includes Hive HQL scripts that extract selected data elements from the raw call report files and stores them in a DynamoDB NoSQL table for easier lookup. 

These scripts can either be run on a local Hive installation or as part of an Elastic MapReduce cluster. The `run_hive_emr` Django management command exists to help easily run the scripts on EMR:

```sh
python manage.py run_hive_emr -b scripts-bucket -s /local/path/to/fdic-call-reports/hive -l logs-bucket -k ec2-keypair
```

This will produce output like:

```sh
uploading /local/path/to/fdic-call-reports/hive/bulk_por.hql to s3://scripts-bucket/hive/bulk_por.hql
uploading /local/path/to/fdic-call-reports/hive/banks.hql to s3://scripts-bucket/hive/banks.hql
starting EMR jobflow
started EMR jobflow j-2SSERH3DCE78T
```

The local scripts are first uploaded from the specified local path (`/local/path/to/fdic-call-reports/hive`) to the specified S3 bucket (`scripts-bucket`). An EMR cluster is started to execute the Hive scripts, with logs going to an S3 bucket if specified (`logs-bucket`). Authentication uses a specified EC2 keypair name (`ec2-keypair`) and the environment variables `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` must be set with valid AWS credentials.

#### The Django web application

The included Django app is still in its initial stages. To date its capabilities are limited to querying a DynamoDB table to display a list of all surveyed banks. Information shown includes bank name, address, IDRSSD number, and most recent call report date.

Caching of queried results is accomplished with ElastiCache to speed up response time. 
