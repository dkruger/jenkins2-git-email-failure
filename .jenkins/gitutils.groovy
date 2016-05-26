def current_sha() {
    def git_commit_file = 'GIT_COMMIT_' + env.BUILD_TAG
    sh("git rev-parse HEAD > ${git_commit_file}")
    return get_file_content(git_commit_file)
}

def blame_emails() {
    def emails_file = 'BLAME_EMAILS_' + env.BUILD_TAG
    sh("python .jenkins/gitbuildinfo.py blame-emails ${env.JOB_URL} ${env.BUILD_NUMBER} > ${emails_file}")
    return get_file_content(emails_file)
}

def get_file_content(file_path) {
    content = readFile(file_path)
    return content.trim()
}

return this;
