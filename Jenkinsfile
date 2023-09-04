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
	      catchError(buildResult: null) {
                sh 'cat file'
              }
	    }
        }
        stage('Build') {
            steps {
                sh 'ls -lrt'
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
}
