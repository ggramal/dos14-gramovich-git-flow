pipeline {
    agent any
    environment {
      CBA  = "Hello"
    }

    stages {
        stage('Test') {
            environment {
              ABC = sh(script: "echo World", returnStdout: true) 
            }
            steps {
                sh 'echo $ABC $CBA'
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
