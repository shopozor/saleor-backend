pipeline {
  agent any
  environment {
    DOCKER_CREDENTIALS = credentials('docker-credentials')
    DOCKER_REPO = "softozor/shopozor-$REPO:$BRANCH"
  }
  stages {
    stage('Publish staging docker container') {
      steps {
        script {
            sh "docker login -u $DOCKER_CREDENTIALS_USR -p $DOCKER_CREDENTIALS_PSW"
            sh "docker build --build-arg ENABLE_DEV_TOOLS=$ENABLE_DEV_TOOLS --network=host -t $DOCKER_REPO ."
            sh "docker push $DOCKER_REPO"
        }
      }
    }
  }
}