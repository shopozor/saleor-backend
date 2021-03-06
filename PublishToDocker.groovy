def helpers = new ch.softozor.pipeline.Helpers()

pipeline {
  agent any
  environment {
    REPO = 'backend'
    DOCKER_CREDENTIALS = credentials('docker-credentials')
  }
  stages {
    stage('Build and publish docker image') {
      steps {
        script {
          helpers.publishBackendDockerImage(REPO, BRANCH, ENABLE_DEV_TOOLS, IMAGE_TYPE)
        }
      }
    }
  }
}