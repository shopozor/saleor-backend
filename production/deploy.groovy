pipeline {
  agent any
  environment {
    DOCKER_CREDENTIALS = credentials('docker-credentials')
    // TODO: put tag here instead of "latest"!
    DOCKER_REPO = "softozor/shopozor-backend:latest"
  }
  stages {
    stage('Publish docker container') {
      steps {
        script {
            sh 'env'
            sh "cp production/Dockerfile production/.dockerignore ."
            sh "docker login -u $DOCKER_CREDENTIALS_USR -p $DOCKER_CREDENTIALS_PSW"
            sh "docker build -t $DOCKER_REPO ."
            sh "docker push $DOCKER_REPO"
        }
      }
    }
  }
}
