pipeline {
    agent any

    environment {
        SERVER_DIR = 'server'
    }

    stages {
        stage('Run Flask App') {
            steps {
                dir("${env.SERVER_DIR}") {
                    script {
                        echo "Running Flask App..."
                        sh 'sudo docker compose up'
                    }
                }
            }
        }
    }

    post {
        success {
            echo "Flask app running on port 5000!"
        }
        failure {
            echo "There was an error starting the services!"
        }
    }
}