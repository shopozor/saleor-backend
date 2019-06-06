// TODO: the best option here is to go for a pipeline with Dockerfile:
// https://jenkins.io/doc/book/pipeline/docker/#dockerfile
pipeline {
  agent {
    docker {
      image 'nikolaik/python-nodejs:latest'
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
          sh "virtualenv $VENV"
          sh ". $VENV/bin/activate && pip install dos2unix"
          sh "chmod u+x ./scripts/install/*.sh"
          sh "python venv/lib/python3.7/site-packages/dos2unix.py scripts/install/install.sh scripts/install/install.sh"
          sh "python venv/lib/python3.7/site-packages/dos2unix.py scripts/install/install-dev.sh scripts/install/install-dev.sh"
          sh ". $VENV/bin/activate && ./scripts/install/install.sh"
          sh ". $VENV/bin/activate && ./scripts/install/install-dev.sh"
        }
      }
    }
    stage('Build saleor frontend') {
      steps {
        withEnv(["HOME=$WORKSPACE"]) {
          sh "cd saleor && npm i && npm run build-assets && npm run build-emails"
        }
      }
    }
    stage('Performing saleor unit tests') {
      environment {
        DATABASE_URL = credentials('postgres-credentials')
        DJANGO_SETTINGS_MODULE = 'tests.settings'
        PYTHONPATH = "$PYTHONPATH:$WORKSPACE/saleor"
        SECRET_KEY = 'theSecretKey'
      }
      steps {
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
