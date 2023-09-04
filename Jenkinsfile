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
              sh 'echo ${ABC[0]}'
	    }
        }
        stage('Build') {
            steps {
                sh 'cat file'
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
