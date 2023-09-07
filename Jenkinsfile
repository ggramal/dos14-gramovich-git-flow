pipeline {
    agent {
      docker {
        image 'python:3.11.3-buster'
	args '-u root'
      }
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
		branch "jenkins-pre-lesson"
	      }
	    }
            steps {
                script {
		  docker.build("gramal/dos14-account:${env.GIT_COMMIT}")
		}
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
