pipeline {
    agent any

    environment {
        METAFLOW_UI = 'metaflow-ui'
        METAFLOW_SERVICE = 'metaflow-service'
        FLOWS = 'flows'
        SERVER_DIR = 'server'
    }

    stages {
        stage('Clone Metaflow services'){
            steps{
                script {
                    sh 'rmdir metaflow-ui'
                    echo "Cloning the metaflow-ui repository..."
                    git 'https://github.com/Netflix/metaflow-ui.git'

                    sh 'rmdir metaflow-service'
                    echo "Cloning the metaflow-service repository..."
                    git 'https://github.com/Netflix/metaflow-service.git'
                }
            }
            post {
                success {
                    echo 'Services cloned successfully!'
                }
                failure {
                    echo 'There was an error cloning the repositories!'
                }
            }
        }

        stage('Build Metaflow UI'){
            steps(){
                dir("${env.METAFLOW_UI}") {
                    script{
                        sh "pwd"
                        sh "ls -a"
                        echo 'Building metaflow-ui image'
                        sh 'sudo docker build --tag metaflow-ui:latest .'
                    }
                    post{
                        success {
                            echo 'Metaflow-UI image created successfully!'
                        }
                        failure {
                            echo 'There was an error creating the Metaflow-UI image!'
                        }
                    }
                }
            }
        }

        stage('Run Metaflow UI Backend'){
            steps(){
                dir("${env.METAFLOW_SERVICE}") {
                    script{
                        sh "pwd"
                        sh "ls -a"
                        echo 'Building metaflow-service'
                        sh 'sudo docker compose -f docker-compose.development.yml up'
                        sh 'sudo docker run -d -p 3000:3000 -e METAFLOW_SERVICE=http://localhost:8083/ metaflow-ui:latest'
                    }
                    post{
                        success {
                            echo 'Metaflow-UI Backend started successfully!'
                        }
                        failure {
                            echo 'There was an error running the Metaflow-UI Backend!'
                        }
                    }
                }
            }
        }

        stage('Run Metaflow Pipeline') {
            steps {
                dir("${env.FLOWS}") {
                    script {
                        echo "Running Metaflow Pipeline..."
                        sh 'sudo docker compose up'
                    }
                }
            }
        }
        
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
            echo "All services started successfully!"
        }
        failure {
            echo "There was an error starting the services!"
        }
    }
}