pipeline {
  agent {
    docker {
      image 'python:latest'
    }
  }
  stages {
    stage('Spec generation') {
      steps {
          sh "mono /opt/pickles/Pickles.exe --feature-directory=$WORKSPACE/features --output-directory=specification --system-under-test-name=shopozor-backend --system-under-test-version=0.0.0 --language=fr --documentation-format=dhtml --exp --et 'in-preparation'"
        }
    }
  }
}