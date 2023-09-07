pipeline {
    agent {
      docker {
        image 'python:3.11.3-buster'
	args '-u root'
      }
    }
    environment {
      CBA  = "123"
    }

    stages {
        stage('Test') {
            environment {
              ABC = sh(script: "cat main.py", returnStdout: true)
            }
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
        stage('Deploy') {
	    when {
	      branch "master"
	    }
	    environment {
	      ANSIBLE_PIPELINING = "True" 
	    }
            steps {
	      sh "cd ansible && ansible-playbook -i 'ip' playbook.yaml"
            }
        }
    }

    post {
      failure {
        sh "echo I send message"
      }
    }
}
