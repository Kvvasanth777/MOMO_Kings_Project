pipeline {

    agent any

    environment {
        IMAGE_NAME = "kvvasanth777/momo-kings"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
               sh '''
                    . venv/bin/activate
                    cd restaurant_management
                    python manage.py test
                  '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build \
                    -t $IMAGE_NAME:$BUILD_NUMBER \
                    -t $IMAGE_NAME:latest .
                '''
            }
        }

        stage('Security Scan') {
            steps {
                sh '''
                    trivy image $IMAGE_NAME:$BUILD_NUMBER
                '''
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-credentials',
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {
                    sh '''
                        echo "$DOCKER_PASSWORD" | \
                        docker login \
                        -u "$DOCKER_USERNAME" \
                        --password-stdin
                    '''
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                sh '''
                    docker push $IMAGE_NAME:$BUILD_NUMBER
                    docker push $IMAGE_NAME:latest
                '''
            }
        }
    }

    post {

        success {
            echo 'MOMO KINGS CI/CD pipeline completed successfully!'
        }

        failure {
            echo 'MOMO KINGS pipeline failed!'
        }
    }
}