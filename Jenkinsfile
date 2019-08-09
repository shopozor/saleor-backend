pipeline {
  agent {
    docker {
      image 'python:3.7'
    }
  }
  environment {
    REPORTS_FOLDER = 'junit-reports'
  }
  stages {
    stage('Virtual Environment Installation') {
      steps {
        withEnv(["HOME=$WORKSPACE"]) {
          sh "env"
          sh "pip install pipenv --user"
          sh "$WORKSPACE/.local/bin/pipenv install --deploy --dev"
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
        SECRET_KEY = 'theSecretKey'
      }
      steps {
        withEnv(["HOME=$WORKSPACE"]) {
          sh "$WORKSPACE/.local/bin/pipenv run python manage.py behave --junit --junit-directory $REPORTS_FOLDER --tags ~wip"
        }
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
