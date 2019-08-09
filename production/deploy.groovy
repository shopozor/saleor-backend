pipeline {
  agent any
  environment {
    DOCKER_CREDENTIALS = credentials('docker-credentials')
    DOCKER_REPO = "softozor/shopozor-backend:$TAG"
  }
  stages {
    stage('Publish docker container') {
      steps {
        script {
            sh "cp production/Dockerfile production/.dockerignore ."
            sh "docker login -u $DOCKER_CREDENTIALS_USR -p $DOCKER_CREDENTIALS_PSW"
            sh "docker build --network=host -t $DOCKER_REPO ."
            sh "docker push $DOCKER_REPO"
        }
      }
    }
  }
}
