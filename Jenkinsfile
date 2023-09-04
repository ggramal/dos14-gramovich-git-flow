pipeline {
    agent any

    stages {

        stage('Test') {
            steps {
                echo 'Testing..'
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
