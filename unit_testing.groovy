pipeline {
  agent {
    docker {
      image 'python:latest'
    }
  } 
  environment {
    REPORTS_FOLDER = 'junit-reports'
    VENV = 'venv'
  }
  stages {
    stage('Virtual Environment Installation') {
      steps {
        withEnv(["HOME=$WORKSPACE"]) {
          sh "pip install virtualenv --user"
          sh "$WORKSPACE/.local/bin/virtualenv $VENV"
          sh "chmod u+x ./scripts/install/*.sh"
          sh ". $VENV/bin/activate && ./scripts/install/install.sh"
          sh ". $VENV/bin/activate && ./scripts/install/install-dev.sh"
        }
      }
    }
    stage('Build saleor frontend') {
      sh "cd saleor && npm i && npm run build-assets && npm run build-emails"
    }
    stage('Performing saleor unit tests') {
      environment {
        DATABASE_URL = credentials('postgres-credentials')
        DJANGO_SETTINGS_MODULE = 'tests.settings'
        PYTHONPATH = "$PYTHONPATH:$WORKSPACE/saleor"
        SECRET_KEY = 'theSecretKey'
      }
      steps {
        // TODO: do we need to perform database migration?
        sh ". $VENV/bin/activate && cd saleor && pytest -ra --junitxml=$REPORTS_FOLDER/unit-tests.xml"
      }
    }
  }
  post {
    always {
      script {
         junit "**/$REPORTS_FOLDER/*.xml"
      }
    }
  }
}
