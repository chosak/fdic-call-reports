Domestically-chartered banks regulated by the FDIC are required to file quarterly financial reports to regulators, known colloquially as "[call reports](http://en.wikipedia.org/wiki/Call_report)". This data is made publically available [by the FFIEC](https://cdr.ffiec.gov/public/) but is difficult to download efficiently and hard to analyze in aggregate.

This project aims to simplify data access and open up new methods for analysis.

It currently consists of 3 major pieces:

1. A downloader to retrieve all bulk call report data,
2. A MapReduce job that processes raw data to produce aggregate data per bank, and
3. A Django-powered web application that allows for exploration and review of aggregated data

#### Downloading raw call report data

While the current [FFIEC download site](https://cdr.ffiec.gov/public/) does offer minimal bulk downloading capabilities, it's not easy to retrieve a detailed set of all call report data over time. Without an API, the only way to do this is to use a browser to retrieve each dataset.

The `bin/download_all_reports.py` script automates this process by using [Selenium](http://www.seleniumhq.org) to iteratively download all available single quarterly call reports. See the comments in that script for instructions on how to setup Selenium locally.

Files downloaded from this script are stored in their original archive format (`.zip`).

#### Preparing call report data for MapReduce

The `bin/extract.py` script extracts all raw text files from the downloaded call report archives and prepares them for processing by MapReduce. Each file is converted to line-JSON format, and optionally stored in a bucket on S3. Files are organized first by report date and then by report type.

Note that all code that leverages AWS resources like S3 follows standard convention and assumes that you have your `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` environment variables set.

#### Running MapReduce

A MapReduce job is written to handle the numerous input files, group data by report type and bank, and output in a normalized way.The excellent [mrjob](http://mrjob.readthedocs.org/en/latest/index.html) library is used so that the job can be written in Python.

See `bin/mrjob-transform.py` for the code; it currently handles two report types: "Bulk POR" (general bank metadata) and "Schedule RC" (balance sheet information).

To run locally, you can do something like:

```sh
python jobs/banks.py input/*/*Bulk*.txt input/*/*RC\ *.txt > output.txt
```

Optionally, you can also run on Elastic MapReduce. See mrjob [documentation](http://mrjob.readthedocs.org/en/latest/guides/emr-quickstart.html) for details.

#### Loading data into MySQL

MySQL is used as a datastore for the Django web application. A loader script is provided to read in the file generated in the previous MapReduce step.

To import data, simply run:

```sh
./manage.py load -f output.txt
```

This requires that you have the `DJANGO_RDS_HOST`, `DJANGO_RDS_USER`, and `DJANGO_RDS_PASSWORD` environment variables set to appropriate database credentials.

#### The Django web application

The Django web application allows for browsing of all data generated in previous steps.

The home page shows a list of all banks over all time, alphabetized by name.

![index](http://i.imgur.com/b8Oira5l.png)

Each bank's ID links to a page displaying the details of its balance sheet over time.

![bank](http://i.imgur.com/Q3CfGHJl.png)
