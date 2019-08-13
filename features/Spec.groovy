pipeline {
  agent any
  stages {
    stage('Spec generation') {
      environment {
        SOFTOZOR_CREDENTIALS = credentials('softozor-credentials')
      }
      steps {
        sh "mono /opt/pickles/Pickles.exe --feature-directory=$WORKSPACE/features --output-directory=specification --system-under-test-name=shopozor-backend --system-under-test-version=0.0.0 --language=fr --documentation-format=dhtml --exp --et 'in-preparation'"
        sh "sshpass -p $SOFTOZOR_CREDENTIALS_PSW ssh -o StrictHostKeyChecking=no $SOFTOZOR_CREDENTIALS_USR@softozor.c 'rm -Rf ~/www/www.softozor.ch/shopozor/backend/*'"
        sh "sshpass -p $SOFTOZOR_CREDENTIALS_PSW scp -o StrictHostKeyChecking=no -r specification $SOFTOZOR_CREDENTIALS_USR@softozor.ch:~/www/www.softozor.ch/shopozor/backend/"
      }
    }
  }
}