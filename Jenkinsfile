pipeline {
    agent any

    environment {
        IMAGE_NAME = 'cloud-file-sharing:latest'
        CONTAINER_NAME = 'cloud-sharing-file'

        MYSQL_HOST = 'host.docker.internal'
        MYSQL_USER = 'clouduser'
        MYSQL_DATABASE = 'cloud_storage'

        AWS_REGION = 'ap-south-1'
        BUCKET_NAME = 'bhargava-s33'
    }

    stages {

        stage('Checkout') {
            steps {
                echo '===== Checkout Source Code ====='
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                echo '===== Build Docker Image ====='

                sh '''
                    docker build --no-cache \
                        -t ${IMAGE_NAME} .
                '''
            }
        }

        stage('Test MySQL Credential') {
            steps {
                echo '===== Test Jenkins MySQL Credential ====='

                withCredentials([
                    string(
                        credentialsId: 'mysql-password',
                        variable: 'MYSQL_PASSWORD'
                    )
                ]) {
                    sh '''
                        if [ -z "$MYSQL_PASSWORD" ]; then
                            echo "ERROR: MYSQL_PASSWORD is EMPTY"
                            exit 1
                        else
                            echo "SUCCESS: MYSQL_PASSWORD is available"
                        fi
                    '''
                }
            }
        }

        stage('Stop Old Container') {
            steps {
                echo '===== Stop Old Container ====='

                sh '''
                    docker rm -f ${CONTAINER_NAME} || true
                '''
            }
        }

        stage('Deploy Container') {
            steps {
                echo '===== Deploy New Container ====='

                withCredentials([
                    string(
                        credentialsId: 'mysql-password',
                        variable: 'MYSQL_PASSWORD'
                    )
                ]) {
                    sh '''
                        docker run -d \
                          --name ${CONTAINER_NAME} \
                          --add-host=host.docker.internal:host-gateway \
                          -e MYSQL_HOST="${MYSQL_HOST}" \
                          -e MYSQL_USER="${MYSQL_USER}" \
                          -e MYSQL_PASSWORD="$MYSQL_PASSWORD" \
                          -e MYSQL_DATABASE="${MYSQL_DATABASE}" \
                          -e AWS_REGION="${AWS_REGION}" \
                          -e BUCKET_NAME="${BUCKET_NAME}" \
                          -p 5000:5000 \
                          ${IMAGE_NAME}
                    '''
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                echo '===== Verify Deployment ====='

                sh '''
                    sleep 10

                    echo "===== Docker Containers ====="
                    docker ps -a

                    echo "===== Application Test ====="
                    curl -f http://127.0.0.1:5000/
                '''
            }
        }
    }

    post {

        success {
            echo '''
========================================
 Cloud File Sharing Deployment SUCCESS
========================================

Application:
http://18.212.207.16:5000/

========================================
'''
        }

        failure {
            echo '''
========================================
 Cloud File Sharing Deployment FAILED
========================================

Checking Docker container and application logs...

========================================
'''

            sh '''
                echo "===== Docker Containers ====="
                docker ps -a

                echo "===== Container Logs ====="
                docker logs ${CONTAINER_NAME} || true
            '''
        }
    }
}
