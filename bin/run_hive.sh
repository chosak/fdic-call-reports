#! /usr/bin/env bash

export HIVE_OPTS=" \
    --hiveconf fs.s3n.awsAccessKeyId=$AWS_ACCESS_KEY_ID \
    --hiveconf fs.s3n.awsSecretAccessKey=$AWS_SECRET_ACCESS_KEY \
"

hive $@
