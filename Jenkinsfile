pipeline {
    agent any
    environment {
      ABC = "Hello"
    }

    stages {
        stage('Test') {
            steps {
                sh 'echo $ABC'
            }
        }
        stage('Build') {
	    when {
	      branch "master"
	    }

            steps {
                sh 'ls -lrt'
            }
        }
        stage('Deploy') {
	    when {
	      branch "master"
	    }
            steps {
                echo 'Deploying.......'
            }
        }
    }
}
