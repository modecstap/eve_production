pipeline {
    agent any

    environment {
        COMPOSE_FILE = "docker-compose.yaml"
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Stop Running Containers') {
            steps {
                script {
                    bat "docker-compose -f %COMPOSE_FILE% down"
                }
            }
        }

        stage('Build and Start Containers') {
            steps {
                script {
                    bat "docker-compose -f %COMPOSE_FILE% pull"
                    bat "docker-compose -f %COMPOSE_FILE% up --build -d"
                }
            }
        }

        stage('Cleanup Unused Images') {
            steps {
                script {
                    bat "docker system prune -a -f"
                    bat "docker builder prune -a -f"
                }
            }
        }
    }
}
