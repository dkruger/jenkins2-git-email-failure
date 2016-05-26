# jenkins2-git-email-failure
Example of using a python and groovy script to send emails when a jenkins pipeline job fails

There are three components to this approach:
1. A python script to perform the git requests
2. A groovy file to make calling the python script easier
3. The Jenkinsfile which will make use of the groovy file

## .jenkins/gitbuildinfo.py
This is the simple python script that does all the manipulation of the git log. It provides a --help using argparse.
I used python here purely because I am more comfortable with it. This assumes that `git` is in your PATH.

## .jenkins/gitutils.groovy
This is based off of the jenkinsci pipeline-examples code: https://github.com/jenkinsci/pipeline-examples/blob/master/pipeline-examples/gitcommit/gitcommit.groovy

This just wraps `gitbuildinfo.py` to make interfacing with it in Jenkinsfile easier

## Jenkinsfile
The pipeline definition file. We import the gitutils.groovy file to email when the build fails.
