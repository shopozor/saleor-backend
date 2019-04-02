pipeline {
  agent {
    docker {
      image 'everpeace/curl-jq'
    }
  } 
  stages {
    stage('Acceptance tests') {
      environment {
        HIDORA_CREDENTIALS = credentials('hidora-credentials')
        ENVIRONMENT_NAME = "shopozor-backend-test"
      }
      steps {
        sh 'chmod u+x ./deploy-to-jelastic.sh'
        sh "./deploy-to-jelastic.sh $HIDORA_CREDENTIALS_USR $HIDORA_CREDENTIALS_PSW $ENVIRONMENT_NAME"
      }
    }
  }
}
