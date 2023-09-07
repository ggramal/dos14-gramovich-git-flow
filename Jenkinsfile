pipeline {
    agent {
      docker {
        image 'python:3.11.3-buster'
      }
    }
    environment {
      ABC = sh(script: "cat main.py", returnStdout: true)
    }

    stages {
        stage('Lint') {
            steps {
	      sh "pip install poetry"
	      sh "poetry install --with dev"
	      sh "poetry run -- black --check *.py **/*.py"
	    }
        }
        stage('Build') {
            steps {
                sh 'echo Building'
            }
        }
    }

    post {
      failure {
        sh "echo I send message"
      }
    }
}
