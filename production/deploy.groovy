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
    stage('Deploy environment') {
      environment {
        JELASTIC_APP_CREDENTIALS = credentials('jelastic-app-credentials')
        JELASTIC_CREDENTIALS = credentials('jelastic-credentials')
        PRODUCTION_ENV_NAME = "shopozor-backend"
        PATH_TO_JPS = "./production/manifest.jps"
      }
      steps {
        script {
          sh "./production/deploy-to-jelastic.sh $JELASTIC_APP_CREDENTIALS_USR $JELASTIC_APP_CREDENTIALS_PSW $JELASTIC_CREDENTIALS_USR $JELASTIC_CREDENTIALS_PSW $PRODUCTION_ENV_NAME cp $PATH_TO_JPS $TAG"
        }
      }
    }
  }
}
