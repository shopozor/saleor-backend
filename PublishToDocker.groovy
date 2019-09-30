def helpers = new ch.softozor.pipeline.Helpers()

pipeline {
  agent any
  environment {
    REPO = 'shopozor-backend'
    DOCKER_CREDENTIALS = credentials('docker-credentials')
  }
  stages {
    stage('Build and publish docker image') {
      script {
        echo "BRANCH = $BRANCH"
        echo "REPO   = $REPO"
        echo "IMAGE_TYPE   = $IMAGE_TYPE"
        // TODO: repo can be deduced from the checked out code
        helpers.publishBackendDockerImage(REPO, BRANCH, ENABLE_DEV_TOOLS, IMAGE_TYPE)
      }
    }
  }
}