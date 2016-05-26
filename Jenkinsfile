import hudson.model.Result

node() {
    try {
        // Do the build here
    } finally {
        // We use a try/finally to ensure that the email happens if the build fails, but that the stage that failed stays red
        if (currentBuild.rawBuild.result != Result.SUCCESS) {
            gitutils = load '.jenkins/gitutils.groovy'
            emailext attachLog: true, to: gitutils.blame_emails(), body: "Caught build failure ${env.BUILD_URL}", compressLog: true, subject: "Build Failed for ${env.JOB_NAME}"
        }
    }
}
