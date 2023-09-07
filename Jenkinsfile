pipeline {
    agent any

    stages {
        stage('Lint') {
            agent {
              docker {
                image 'python:3.11.3-buster'
                args '-u root'
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
		branch "jenkins-pre-lesson"
	      }
	    }
            steps {
                script {
		  def image = docker.build("gramal/dos14-account:${env.GIT_COMMIT}")
                  docker.withRegistry('', 'dockerhub-gramal') {
                    image.push()
                  }
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
