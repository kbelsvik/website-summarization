import boto3
from botocore import UNSIGNED
from botocore.client import Config
import gzip
import random

def get_warc_paths(crawl = 'CC-MAIN-2017-43'):
    s3 = boto3.resource('s3', config=Config(signature_version=UNSIGNED))

    key = "crawl-data/" + crawl + "/warc.paths.gz"
    output_file = "data/paths/" + crawl + "-warc.paths.gz"
    s3.Bucket("commoncrawl").download_file(key, output_file)
    return output_file

def get_warc_files(path_archive, num_files=10):
    s3 = boto3.resource('s3', config=Config(signature_version=UNSIGNED))
    files = []
    
    with gzip.open(path_archive, 'rb') as f:
        files = [line.strip() for line in f]

    random.shuffle(files)
    sample = files[:num_files]

    for path in sample:
        s3.Bucket("commoncrawl").download_file(path, "data/warc/" + path.split("/")[-1])
    return sample
