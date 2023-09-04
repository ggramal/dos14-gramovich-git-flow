pipeline {
    agent any
    environment {
      CBA  = "export H='123'"
    }

    stages {
        stage('Test') {
	    catchError(buildResult: null) {
              environment {
                ABC = sh(script: "cat file", returnStdout: true).split("\n")
              }
              steps {
                  sh 'echo ${ABC[0]} $CBA'
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
