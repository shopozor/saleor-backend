pipeline {
  agent {
    docker {
      image 'python:latest'
    }
  } 
  environment {
    REPORT = 'cucumber-report.json'
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
    stage('Performing acceptance tests') {
      environment {
        DATABASE_URL = credentials('postgres-credentials')
        DJANGO_SETTINGS_MODULE = 'features.settings'
        PYTHONPATH = "$PYTHONPATH:$WORKSPACE/saleor"
        JWT_EXPIRATION_DELTA_IN_DAYS = 30
        JWT_REFRESH_EXPIRATION_DELTA_IN_DAYS = 360
        JWT_SECRET_KEY = 'test_key'
        JWT_ALGORITHM = 'HS256'
        SECRET_KEY = 'trouduc'
      }
      steps {
        sh ". $VENV/bin/activate && python manage.py behave --format json -o $REPORT --tags=\"~wip\""
      }
    }
  }
  post {
    success {
      echo "Test succeeded"
      script {
        sh "echo $JENKINS_HOME/jobs/$JOB_NAME/builds/$BUILD_NUMBER/cucumber-html-reports/.cache"
        sh "ls $JENKINS_HOME/jobs/$JOB_NAME/builds/$BUILD_NUMBER/cucumber-html-reports/"
        cucumber fileIncludePattern: "$REPORT", sortingMethod: 'ALPHABETICAL'
      }
    }
    failure {
      echo "Test failed"
      script {
        sh "echo $JENKINS_HOME/jobs/$JOB_NAME/builds/$BUILD_NUMBER/cucumber-html-reports/.cache"
        sh "ls $JENKINS_HOME/jobs/$JOB_NAME/builds/$BUILD_NUMBER/cucumber-html-reports/"
        cucumber fileIncludePattern: "$REPORT", sortingMethod: 'ALPHABETICAL'
      }
    }
  }
}
