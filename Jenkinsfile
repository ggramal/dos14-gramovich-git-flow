pipeline {
  agent {
    label 'test'
  }
  environment {
    ABC = sh(script: "cat main.py", returnStdout: true)
  }

  stages {
    stage('Lint') {
      agent {
        docker {
          image 'python:3.11.3-buster'
          args '-u 0'
        }
      }
      when {
        anyOf {
          branch "master"
          branch pattern: "feature-*", comparator: "GLOB"
        }
      }
      steps {
        sh "pip install poetry"
        sh "poetry install --with dev"
        sh "poetry run -- black --check *.py **/*.py"
      }
    }
    stage('Build') {
      when {
        anyOf {
          branch "master"
        }
      }
      steps {
        script {
          def image = docker.build "gramal/dos14-account:${env.GIT_COMMIT}"
          docker.withRegistry('','dockerhub-gramal') {
            image.push()
          }
        }
      }
    }
  }
}
