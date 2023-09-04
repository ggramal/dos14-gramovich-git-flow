pipeline {
    agent any
    environment {
      CBA  = "export H='123'"
    }

    stages {
        stage('Test') {
            environment {
              ABC = sh(script: "cat main.py", returnStdout: true).split("\n")
            }
            steps {
	      try {
                sh 'echo ${ABC[0]}'
	      catch (Exception e) {
	        sh 'echo Error'
	      }
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
                echo 'Deploying.......'
            }
        }
    }

    post {
      failure {
        sh "echo I send message"
      }
    }
}
