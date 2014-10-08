DROP TABLE IF EXISTS banks;
CREATE TABLE banks 
AS SELECT
    name,
    idrssd,
    report_date,
    address,
    city,
    state,
    zip
FROM (
    SELECT 
        row_number() OVER (
            PARTITION BY idrssd ORDER BY report_date DESC
        ) report_idx,
        name,
        idrssd,
        report_date,
        address,
        city,
        state,
        zip
    FROM
        bulk_por
) x
WHERE
    report_idx = 1
;

DROP TABLE IF EXISTS banks_dynamodb;
CREATE EXTERNAL TABLE banks_dynamodb (
    name STRING,
    idrssd STRING,
    report_date STRING,
    address STRING,
    city STRING,
    state STRING,
    zip STRING
)
STORED BY 'org.apache.hadoop.hive.dynamodb.DynamoDBStorageHandler'
TBLPROPERTIES(
    "dynamodb.table.name"="banks",
    "dynamodb.column.mapping"="name:name,idrssd:idrssd,report_date:report_date,address:address,city:city,state:state,zip:zip"
);

INSERT OVERWRITE TABLE banks_dynamodb
SELECT
    *
FROM
    banks;
