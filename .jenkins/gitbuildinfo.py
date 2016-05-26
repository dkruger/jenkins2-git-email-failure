#!/usr/bin/env python
from __future__ import print_function
import argparse
import json
import subprocess
import sys
import urllib2
import urlparse



def main():
    parser = argparse.ArgumentParser(
        description='Utility script used for jenkins builds.')
    subparsers = parser.add_subparsers(title='commands')
    blame_emails_parser = subparsers.add_parser(
        'blame-emails',
        help="Return a comman-separated list of emails for committers")
    blame_emails_parser.set_defaults(func=blame_emails)
    blame_emails_parser.add_argument(
        'job_url',
        help='The URL of the job on jenkins (JOB_URL)')
    blame_emails_parser.add_argument(
        'build_number',
        type=int,
        help='The build number of the current build (BUILD_NUMBER)')
    args = parser.parse_args()
    args.func(args)



def blame_emails(args):
    print(get_blame_emails(
        args.job_url,
        args.build_number))



def get_blame_emails(job_url, build_number):
    last_successful_sha = get_build_sha(job_url, 'lastSuccessfulBuild')
    build_sha = get_build_sha(job_url, str(build_number))
    if last_successful_sha is None:
        revlist = build_sha
    else:
        revlist = '{}..{}'.format(last_successful_sha, build_sha)
    log_output = subprocess.check_output([
        'git',
        'log',
        '--format=%aE',
        revlist])
    emails = set()
    for line in log_output.split('\n'):
        if len(line):
            emails.add(line)
    return ','.join(emails)



def get_build_sha(job_url, build_id):
    build_api_url = build_json_api_url(job_url, build_id, 'git')
    build_git_data = get_json_data(build_api_url)
    if build_git_data is None:
        return None
    return build_git_data['lastBuiltRevision']['SHA1']



def build_json_api_url(base_url, *args):
    api_args = args + ('api', 'json')
    return build_url(base_url, *api_args)



def build_url(base_url, *args):
    if len(args) == 0:
        return base_url
    url = base_url
    for arg in args:
        if not url[-1] == '/':
            url += '/'
        url = urlparse.urljoin(url, arg)
    return url



def get_json_data(url):
    try:
        response = urllib2.urlopen(url)
    except urllib2.HTTPError as e:
        print(e, file=sys.stderr)
        return None
    return json.load(response)



if __name__ == "__main__":
    main()
