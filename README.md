# Find Incomplete S3 Multi-Part Uploads

This script will find incomplete multi-part uploads. It will find both in progress uploads and those that have been abandoned. It's purpose is to find out if abandoned uploads are taking up excess space in the archive.

## Prerequisites

* Developed with Python 3.6.5
* boto3 v1.7.60+

## Installation

1. Install python on your system.
   * Python can be found at: <http://www.python.org>
2. Install the AWS Boto3 module for Python.
   * `pip install boto3`

## Usage

```text
usage: find-incomplete-s3-multipart-uploads.py [-h]
                                               [--bucket BUCKET [BUCKET ...]]
                                               [--profile PROFILE] [--debug]
                                               [--verbose]

Expand the node disks for Find Incomplete S3 Multi Part Uploads in AWS

optional arguments:
  -h, --help            show this help message and exit
  --bucket BUCKET [BUCKET ...], -b BUCKET [BUCKET ...]
                        AWS bucket to check.
  --profile PROFILE, -P PROFILE
                        AWS Profile to use. If left blank the default profile
                        will be used.
  --debug, -D           Debug mode.
  --verbose, -v         Verbose mode.
```

## Notes

Running the script with no options will produce a summary output.

Using the `--verbose` option will produce detailed output about each file including upload date, filename and size.

## Licensing

Find Incomplete S3 Multi-Part Uploads is freely distributed under the [GPLv3 License](https://www.gnu.org/licenses/gpl-3.0.en.html "LICENSE"). See [LICENSE](https://github.com/rubrik-devops/find-incomplete-s3-multipart-uploads/blob/master/LICENSE) for details.

## Support

Please file bugs and issues on the Github issues page for this project. This is to help keep track and document everything related to this repo.
