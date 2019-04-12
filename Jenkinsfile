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
    // stage('Virtual Environment Installation') {
    //   steps {
    //     withEnv(["HOME=$WORKSPACE", "PATH+LOCAL_BIN=$WORKSPACE/.local/bin"]) {
    //       sh "pip install -r saleor/requirements.txt --user"
    //       sh "pip install -r requirements.txt --user"
    //       sh "pip install -r saleor/requirements_dev.txt --user"
    //     }
    //   }
    // }
    stage('Performing acceptance tests') {
      environment {
        DATABASE_URL = credentials('postgres-credentials')
      }
      steps {
        withEnv(["HOME=$WORKSPACE", "PATH+LOCAL_BIN=$WORKSPACE/.local/bin", "DJANGO_SETTINGS_MODULE=features.settings", "PYTHONPATH=$WORKSPACE/.local/lib/python3.7/site-packages/:$WORKSPACE/saleor", "JWT_EXPIRATION_DELTA_IN_DAYS=30", "JWT_REFRESH_EXPIRATION_DELTA_IN_DAYS=360", "JWT_SECRET_KEY=test_key", "JWT_ALGORITHM=HS256", "SECRET_KEY=trouduc"]) {
          // sh "python manage.py behave --format json -o $REPORT --tags='~wip'"
          sh "echo $DJANGO_SETTINGS_MODULE"
          sh "python ./manage.py help --settings features.settings"
        }
      }
    }
  }
  // post {
  //   success {
  //     echo "Test succeeded"
  //     script {
  //       cucumber fileIncludePattern: "$REPORT", sortingMethod: 'ALPHABETICAL'
  //     }
  //   }
  //   failure {
  //     echo "Test failed"
  //     cucumber fileIncludePattern: "$REPORT", sortingMethod: 'ALPHABETICAL'
  //   }
  // }
}
