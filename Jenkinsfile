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
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build --no-cache -t ${IMAGE_NAME} .
                '''
            }
        }

        stage('Stop Old Container') {
            steps {
                sh '''
                    docker rm -f ${CONTAINER_NAME} || true
                '''
            }
        }

        stage('Deploy Container') {
            steps {
                withCredentials([
                    string(
                        credentialsId: 'mysql_password',
                        variable: 'bh@rgava12'
                    )
                ]) {
                    sh '''
                        docker run -d \
                          --name ${CONTAINER_NAME} \
                          --add-host=host.docker.internal:host-gateway \
                          -e MYSQL_HOST=${MYSQL_HOST} \
                          -e MYSQL_USER=${MYSQL_USER} \
                          -e MYSQL_PASSWORD="${MYSQL_PASSWORD}" \
                          -e MYSQL_DATABASE=${MYSQL_DATABASE} \
                          -e AWS_REGION=${AWS_REGION} \
                          -e BUCKET_NAME=${BUCKET_NAME} \
                          -p 5000:5000 \
                          ${IMAGE_NAME}
                    '''
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                    sleep 5
                    echo "===== Docker Containers ====="
                    docker ps

                    echo "===== Application Test ====="
                    curl -f http://127.0.0.1:5000/
                '''
            }
        }
    }

    post {
        success {
            echo '======================================'
            echo 'Cloud File Sharing deployed successfully'
            echo '======================================'
            echo 'Application: http://18.212.207.16:5000/'
        }

        failure {
            echo '======================================'
            echo 'Deployment failed.'
            echo 'Check the Jenkins console output.'
            echo '======================================'

            sh '''
                echo "===== Container Status ====="
                docker ps -a

                echo "===== Container Logs ====="
                docker logs ${CONTAINER_NAME} || true
            '''
        }
    }
}
