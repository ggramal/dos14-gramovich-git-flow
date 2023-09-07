pipeline {
    agent {
      docker {
        image 'python:3.11.3-buster'
	args '-u 0'
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
	    when {
	      anyOf {
	        branch "master"
		branch "jenkins"
		branch pattern: "feature-*", comparator: "GLOB"
	      }
	    }
            steps {
	      script {
	        println sh(script: "env", returnStdout: true)
	      }
            }
        }
    }
}
