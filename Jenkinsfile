pipeline {
    agent any

    environment {
        METAFLOW_UI = 'metaflow-ui'
        METAFLOW_SERVICE = 'metaflow-service'
        FLOWS = 'flows'
        SERVER_DIR = 'server'
    }

    stages {
        stage('Configure Metaflow Directories'){
            steps{
                script{
                    if (!fileExists("metaflow-ui")) {
                        echo "Creating metaflow-ui directory..."
                        sh "mkdir metaflow-ui" 
                    } else {
                        echo "Repository already exists!"
                    }

                    if (!fileExists("metaflow-service")) {
                        echo "Creating metaflow-service directory..."
                        sh "mkdir metaflow-service" 
                    } else {
                        echo "Repository already exists!"
                    }

                }
            }
        }
        stage('Clone Metaflow Services'){
            steps{
                script{
                    dir("metaflow-ui"){
                        echo 'Cloning into metaflow-ui...'
                        git 'https://github.com/Netflix/metaflow-ui.git'
                    }

                    dir("metaflow-service"){
                        echo 'Cloning into metaflow-service...'
                        git 'https://github.com/Netflix/metaflow-service.git'
                    }
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
                dir("metaflow-ui") {
                    script{
                        echo 'Building metaflow-ui image'
                        sh 'sudo docker build --tag metaflow-ui:latest .'
                    }
                }
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

        stage('Run Metaflow UI Backend'){
            steps {
                dir("metaflow-service") {
                    script {
                        echo 'Starting metaflow-service backend...'
                        sh 'sudo docker compose -f docker-compose.development.yml up -d'
                        
                        // Add a health check or sleep to ensure backend is ready
                        echo 'Waiting for backend to be ready...'
                        // sh 'sleep 30'  // Simple approach with fixed delay
                        
                        // Or better, use a health check loop (more reliable)
                        sh '''
                            timeout=60
                            while ! curl -s http://localhost:8083/ > /dev/null; do
                                if [ $timeout -le 0 ]; then
                                    echo "Timeout waiting for backend"
                                    exit 1
                                fi
                                echo "Waiting for backend to be ready..."
                                sleep 5
                                timeout=$((timeout - 5))
                            done
                        '''
                        
                        echo 'Starting metaflow-ui...'
                        sh 'sudo docker run -d -p 3000:3000 -e METAFLOW_SERVICE=http://localhost:8083/ metaflow-ui:latest'
                    }
                }
            }
            post {
                success {
                    echo 'Metaflow-UI Backend and UI started successfully!'
                }
                failure {
                    echo 'There was an error running the Metaflow services!'
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