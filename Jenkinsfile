pipeline {

    agent any

    environment {

        // Docker
        IMAGE_NAME = 'cloud-file-sharing:latest'
        CONTAINER_NAME = 'cloud-sharing-file'

        // MySQL
        MYSQL_HOST = 'host.docker.internal'
        MYSQL_USER = 'clouduser'
        MYSQL_PASSWORD = 'bh@rgava12'
        MYSQL_DATABASE = 'cloud_storage'

        // AWS S3
        AWS_REGION = 'ap-south-1'
        BUCKET_NAME = 'bhargava-s33'

        // EC2
        EC2_PUBLIC_IP = '34.229.20.232'
    }

    stages {

        stage('Checkout') {
            steps {

                echo '===== CHECKOUT PROJECT ====='

                git branch: 'main',
                    url: 'https://github.com/2400089004/Cloud-File-Sharing-Project.git'
            }
        }

        stage('Build Docker Image') {
            steps {

                echo '===== BUILD DOCKER IMAGE ====='

                sh '''
                    docker build -t ${IMAGE_NAME} .
                '''
            }
        }

        stage('Remove Old Container') {
            steps {

                echo '===== REMOVE OLD CONTAINER ====='

                sh '''
                    docker stop ${CONTAINER_NAME} || true
                    docker rm ${CONTAINER_NAME} || true
                '''
            }
        }

        stage('Run Docker Container') {
            steps {

                echo '===== RUN DOCKER CONTAINER ====='

                sh '''
                    docker run -d \
                        --name ${CONTAINER_NAME} \
                        --add-host=host.docker.internal:host-gateway \
                        -e MYSQL_HOST="${MYSQL_HOST}" \
                        -e MYSQL_USER="${MYSQL_USER}" \
                        -e MYSQL_PASSWORD="${MYSQL_PASSWORD}" \
                        -e MYSQL_DATABASE="${MYSQL_DATABASE}" \
                        -e AWS_REGION="${AWS_REGION}" \
                        -e BUCKET_NAME="${BUCKET_NAME}" \
                        -p 5000:5000 \
                        ${IMAGE_NAME}
                '''
            }
        }

        stage('Check Container') {
            steps {

                echo '===== CHECK CONTAINER ====='

                sh '''
                    sleep 5

                    echo "===== DOCKER CONTAINERS ====="

                    docker ps -a

                    echo "===== CONTAINER STATUS ====="

                    docker inspect ${CONTAINER_NAME} \
                        --format='Status={{.State.Status}} ExitCode={{.State.ExitCode}}'
                '''
            }
        }

        stage('Application Logs') {
            steps {

                echo '===== APPLICATION LOGS ====='

                sh '''
                    docker logs ${CONTAINER_NAME} || true
                '''
            }
        }

        stage('Verify Deployment') {
            steps {

                echo '===== VERIFY DEPLOYMENT ====='

                sh '''
                    sleep 5

                    echo "===== FINAL CONTAINER STATUS ====="

                    docker ps -a

                    echo "===== TEST APPLICATION ====="

                    curl -f http://$34.229.20.232:5000/
                '''
            }
        }
    }

    post {

        success {

            echo '''
========================================
       DEPLOYMENT SUCCESSFUL
========================================

Application:
http://34.229.20.232:5000/

Docker Container:
cloud-sharing-file

Docker Image:
cloud-file-sharing

========================================
'''
        }

        failure {

            echo '''
========================================
       DEPLOYMENT FAILED
========================================

Checking Docker container and logs...

========================================
'''

            sh '''
                echo "===== DOCKER CONTAINERS ====="

                docker ps -a

                echo "===== APPLICATION LOGS ====="

                docker logs ${CONTAINER_NAME} || true
            '''
        }
    }
}
