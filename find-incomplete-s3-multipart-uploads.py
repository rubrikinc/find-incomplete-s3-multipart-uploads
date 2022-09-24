#!/usr/bin/env python3

import sys, boto3, json, botocore, argparse, pprint, logging, datetime 
from datetime import datetime, timedelta, timezone


product = "Find Incomplete S3 Multi Part Uploads"

parser = argparse.ArgumentParser(description='Expand the node disks for {product} in AWS'.format(product=product))
parser.add_argument('--bucket', '-b', metavar='BUCKET', nargs='+',required=False,
                    help='AWS bucket to check.')
parser.add_argument('--profile', '-P', metavar='PROFILE',required=False,
                    help='AWS Profile to use. If left blank the default profile will be used.')
parser.add_argument('--debug', '-D', action='store_true',
                    help='Debug mode.')
parser.add_argument('--verbose', '-v', action='store_true',
                    help='Verbose mode.')
args = parser.parse_args()

def setup_custom_logger(name):
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    handler = logging.FileHandler(__file__ + '.' + datetime.now().strftime('%Y-%m-%d.%H:%M:%S') + '.log', mode='w')
    handler.setFormatter(formatter)
    screen_handler = logging.StreamHandler(stream=sys.stdout)
    screen_handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.addHandler(screen_handler)
    return logger

# Proccess args
debug = args.debug
buckets = args.bucket
profile = args.profile
verbose = args.verbose

# Start Logger
logger = setup_custom_logger('find-incomplete-s3-multipart-upload')

# Set AWS Profile
if profile:
# Create custom session
    logger.info('Using profile {}'.format(profile))
    session = boto3.session.Session(profile_name=profile)
else:
# Use default session
    logger.info('Using default profile')
    session = boto3.session.Session()

# Create an S3 client
s3 = session.client('s3')

# Call S3 to list current buckets
response = s3.list_buckets()

# Get a list of all bucket names from the response
if not buckets: 
    buckets = [bucket['Name'] for bucket in response['Buckets']]
if debug:
    logger.debug('buckets is: {}'.format(buckets))

#Search and report on multi-part uploads
totalallbucketsize = 0
for bucket in buckets:
    totalbucketsize = 0
    if verbose:
        logger.info ('Bucket: {}'.format(bucket))
    multipartuploads = s3.list_multipart_uploads(Bucket=bucket)
    if debug:
        logger.debug('multipartuploads is: {}'.format(pprint.pprint(multipartuploads)))
    if multipartuploads['NextKeyMarker']:
        totaluploadsize = 0
        for upload in multipartuploads['Uploads']:
            if debug:
                logger.debug ('upload is: {}'.format(pprint.pprint(upload)))
            if verbose:
                logger.info ('Initiated: {}, Initiator: {}, StorageClass: {}'.format(upload['Initiated'],upload['Initiator']['DisplayName'],upload['StorageClass']))
                logger.info ('File: {}'.format(upload['Key']))
            parts = s3.list_parts(Bucket=bucket,Key=upload['Key'],UploadId=upload['UploadId'])
            if debug:
                logger.debug ('parts: {}'.format(pprint.pprint(parts)))
            totalfilesize = 0
            if parts['NextPartNumberMarker'] > 0:
                for part in parts['Parts']:
                    if verbose:
                        logger.info ('PartNumber: {}, LastModified: {}, Size: {} bytes'.format(part['PartNumber'], part['LastModified'], part['Size']))
                    totalfilesize += part['Size']
                totalfilesizekb = totalfilesize / 1024
                totalfilesizemb = totalfilesizekb / 1024
                totalfilesizegb = totalfilesizemb / 1024
                totalfilesizetb = totalfilesizegb / 1024
                totaluploadsize += totalfilesize
                if verbose:
                    logger.info ('Total file size: {0:.2f}Bytes, {1:.2f}KB, {2:.2f}MB, {3:.2f}GB, {4:.2f}TB'.format(totalfilesize,totalfilesizekb,totalfilesizemb,totalfilesizegb,totalfilesizetb))
            else:
                if verbose:
                    logger.info ('No parts for file.')
            totaluploadsizekb = totaluploadsize / 1024
            totaluploadsizemb = totaluploadsizekb / 1024
            totaluploadsizegb = totaluploadsizemb / 1024
            totaluploadsizetb = totaluploadsizegb / 1024
            totalbucketsize += totalfilesize
    else:
        if verbose:
            logger.info ('No outstanding multipart uploads for bucket: {}'.format(bucket))
    totalbucketsizekb = totalbucketsize / 1024
    totalbucketsizemb = totalbucketsizekb / 1024
    totalbucketsizegb = totalbucketsizemb / 1024
    totalbucketsizetb = totalbucketsizegb / 1024
    logger.info('Total bucket size of outstanding multipart uploads in bucket {0}: {1:.2f}Bytes, {2:.2f}KB, {3:.2f}MB, {4:.2f}GB, {5:.2f}TB'.format(bucket,totalbucketsize,totalbucketsizekb,totalbucketsizemb,totalbucketsizegb,totalbucketsizetb))
    totalallbucketsize += totalbucketsize
totalallbucketsizekb = totalallbucketsize / 1024
totalallbucketsizemb = totalallbucketsizekb / 1024
totalallbucketsizegb = totalallbucketsizemb / 1024
totalallbucketsizetb = totalallbucketsizegb / 1024
logger.info('Total size multipart uploads across all buckets: {0:.2f}Bytes, {1:.2f}KB, {2:.2f}MB, {3:.2f}GB, {4:.2f}TB'.format(totalallbucketsize,totalallbucketsizekb,totalallbucketsizemb,totalallbucketsizegb,totalallbucketsizetb))
