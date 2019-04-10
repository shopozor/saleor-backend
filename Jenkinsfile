pipeline {
  agent {
    docker {
      image 'python:latest'
    }
  } 
  environment {
    REPORT = 'cucumber-report.json'
  }
  stages {
    environment {
      VENV = 'venv'
      JWT_EXPIRATION_DELTA_IN_DAYS = 30
      JWT_REFRESH_EXPIRATION_DELTA_IN_DAYS = 360
      JWT_SECRET_KEY = 'test_key'
      JWT_ALGORITHM = 'HS256'
      SECRET_KEY = 'trouduc'
      PYTHONPATH = "$WORKSPACE/saleor"
      DJANGO_SETTINGS_MODULE = 'features.settings'
      // TODO: double-check that this variable is accessible from the node (it should be defined!)
      //DATABASE_URL = postgres://${globals.PG_DB_USERNAME}:${globals.PG_USER_PASSWORD}@${nodes.sqldb.intIP}:5432/${globals.PG_DB_NAME}
    }
    stage('Virtual Environment Installation') {
      steps {
        sh 'echo "DATABASE_URL = $DATABASE_URL"'
        sh "virtualenv $VENV"
        sh "source $VENV/bin/activate"
        sh "chmod u+x ./scripts/install/*.sh"
        sh "./scripts/install/install.sh"
        sh "./scripts/install/install-dev.sh"
      }
    }

    stage('Performing acceptance tests') {
      steps {
        sh "python manage.py behave --format json -o $REPORT --tags='~wip'"
      }
    }

    // Do we clean up the virtual environment after the test?
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
