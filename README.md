# jenkins2-git-email-failure

__UPDATE__: The emailext plugin added a feature to email culprits with the 2.44 release: https://issues.jenkins-ci.org/browse/JENKINS-35365

Example of using a python and groovy script to send emails when a jenkins pipeline job fails

There are three components to this approach:

1. A python script to perform the git requests
2. A groovy file to make calling the python script easier
3. The Jenkinsfile which will make use of the groovy file

You will need to add the following approvedSignatures to scriptApproval.xml (either manually or by building and allowing each one through `Manage Jenkins > In-process Script Approval`:
```
method hudson.model.Run getResult
method org.jenkinsci.plugins.workflow.support.steps.build.RunWrapper getRawBuild
staticField hudson.model.Result SUCCESS
```

## .jenkins/gitbuildinfo.py
This is the simple python script that does all the manipulation of the git log. It provides a --help using argparse.
I used python here purely because I am more comfortable with it. This assumes that `git` is in your PATH.

## .jenkins/gitutils.groovy
This is based off of the jenkinsci pipeline-examples code: https://github.com/jenkinsci/pipeline-examples/blob/master/pipeline-examples/gitcommit/gitcommit.groovy

This just wraps `gitbuildinfo.py` to make interfacing with it in Jenkinsfile easier

## Jenkinsfile
The pipeline definition file. We import the gitutils.groovy file to email when the build fails.
