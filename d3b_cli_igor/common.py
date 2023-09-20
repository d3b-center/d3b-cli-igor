import logging
import yaml
import sys
import colorlog
import numpy
import boto3
import os,json
from pathlib import Path

logger = logging.getLogger()
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

RESULT_SUCCESS = {"Result": "success"}
RESULT_FAILURE = {"Result": "failure"}
RESULT_ABORTED = {"Result": "aborted"}
AVAILABLE_OPERATIONS = ["delete_objects", "delete_bucket", "md5check", "thaw_objects"]

path = os.path.dirname(__file__)
config_file = "config/account_info.json"

def get_account_info():
    account_information={}
    with open(path + "/" + config_file ) as json_file:
        account_information = json.load(json_file)
    return account_information

def setup(client_name=""):
    client = boto3.client(client_name)
    return client


def progress_bar(
    iteration, prefix="", suffix="", decimals=1, length=100, fill="█", printEnd="\r"
):
    print(f"\r{prefix} | {iteration} {suffix}", end=printEnd)


def list_objects(bucket_name, s3_client, next_marker):
    if next_marker == "":
        objects = s3_client.list_object_versions(Bucket=bucket_name)
    else:
        objects = s3_client.list_object_versions(
            Bucket=bucket_name, KeyMarker=next_marker
        )
    return objects


def get_object_versions(bucket_name, s3_client, next_marker, all_versioned_objects):
    all_versioned_objects = []
    objects = list_objects(bucket_name, s3_client, "")
    while "NextKeyMarker" in objects and objects["NextKeyMarker"] != "":
        if "Versions" in objects:
            all_versioned_objects = all_versioned_objects + objects["Versions"]
        elif "DeleteMarkers" in objects:
            all_versioned_objects = all_versioned_objects + objects["DeleteMarkers"]
        objects = list_objects(bucket_name, s3_client, objects["NextKeyMarker"])
        printProgressBar(
            str(len(all_versioned_objects)), "Number of objects found in the bucket "
        )
    result = split_objects_into_slices(all_versioned_objects)
    return result


def divide_chunks(l, n):
    return [l[i : i + n] for i in range(0, len(l), n)]


def split_objects_into_slices(objects):
    return list(divide_chunks(objects, 1000))


def reduce_array_keys(objects):
    mod_array = []
    for item in objects:
        mod_array.append({"Key": item["Key"], "VersionId": item["VersionId"]})
    return mod_array


def get_logger(dunder_name, testing_mode, log_format) -> logging.Logger:
    if log_format == "simple":
        log_format = "%(message)s"
    else:
        log_format = (
            "%(asctime)s - "
            "%(name)s - "
            "%(funcName)s - "
            "%(levelname)s - "
            "%(message)s"
        )
    bold_seq = "\033[1m"
    colorlog_format = f"{bold_seq} " "%(log_color)s " f"{log_format}"
    colorlog.basicConfig(format=colorlog_format)
    logger = logging.getLogger(dunder_name)

    if testing_mode:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    Path("/tmp/igor/logs").mkdir(parents=True, exist_ok=True)
    # Output full log
    fh = logging.FileHandler("/tmp/igor/logs/app.log")
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter(log_format)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # Output warning log
    fh = logging.FileHandler("/tmp/igor/logs/app.warning.log")
    fh.setLevel(logging.WARNING)
    formatter = logging.Formatter(log_format)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # Output error log
    fh = logging.FileHandler("/tmp/igor/logs/app.error.log")
    fh.setLevel(logging.ERROR)
    formatter = logging.Formatter(log_format)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger
