pipeline {
    agent any
    environment {
      CBA  = "123"
    }

    stages {
        stage('Test') {
            environment {
              ABC = sh(script: "cat main.py", returnStdout: true).split("\n")[0]
            }
            steps {
              sh 'echo ${ABC}'
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
