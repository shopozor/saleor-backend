def helpers = new ch.softozor.pipeline.Helpers()

pipeline {
  agent any
  stages {
    stage('Spec generation') {
      environment {
        SOFTOZOR_CREDENTIALS = credentials('softozor-credentials')
      }
      steps {
        script {
          helpers.generateSpecification("$WORKSPACE/features", 'backend', GIT_COMMIT)
        }
      }
    }
  }
}