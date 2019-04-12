pipeline {
  agent {
    docker {
      image 'python:latest'
    }
  } 
  environment {
    REPORT = 'cucumber-report.json'
    VENV = 'venv'
    JWT_EXPIRATION_DELTA_IN_DAYS = 30
    JWT_REFRESH_EXPIRATION_DELTA_IN_DAYS = 360
    JWT_SECRET_KEY = 'test_key'
    JWT_ALGORITHM = 'HS256'
    SECRET_KEY = 'trouduc'
    PYTHONPATH = "$WORKSPACE/saleor"
    DJANGO_SETTINGS_MODULE = 'features.settings'
  }
  stages {
    stage('Virtual Environment Installation') {
      environment {
        DATABASE_URL = credentials('postgres-credentials')
      }
      steps {
        sh "pip install -r saleor/requirements.txt --user"
        sh "pip install -r requirements.txt --user"
        sh "pip install -r saleor/requirements_dev.txt --user"
      }
    }
    stage('Performing acceptance tests') {
      steps {
        sh "python manage.py behave --format json -o $REPORT --tags='~wip'"
      }
    }
  }
  post {
    success {
      echo "Test succeeded"
      script {
        cucumber fileIncludePattern: $REPORT, sortingMethod: 'ALPHABETICAL'
      }
    }
    failure {
      echo "Test failed"
      cucumber fileIncludePattern: $REPORT, sortingMethod: 'ALPHABETICAL'
    }
  }
}
