DROP TABLE IF EXISTS bulk_por;
CREATE EXTERNAL TABLE bulk_por (
    idrssd INT,
    fdic_certificate_num INT,
    occ_charter_num INT,
    ots_docket_num INT,
    aba_routing_num INT,
    name STRING,
    address STRING,
    city STRING,
    state STRING,
    zip INT,
    type INT,
    update_time STRING
) PARTITIONED BY (report_date STRING)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
LINES TERMINATED BY '\n'
STORED AS TEXTFILE
LOCATION 's3n://fdic-call-reports/bulk-por/'
TBLPROPERTIES("skip.header.line.count"="1");

MSCK REPAIR TABLE bulk_por;
