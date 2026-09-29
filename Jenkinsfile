pipeline {
agent any

```
environment {
    IMAGE_NAME = 'cloud-file-sharing:latest'
    CONTAINER_NAME = 'cloud-sharing-file'

    MYSQL_HOST = 'host.docker.internal'
    MYSQL_USER = 'clouduser'
    MYSQL_PASSWORD = 'bh@rgava12'
    MYSQL_DATABASE = 'cloud_storage'

    AWS_REGION = 'ap-south-1'
    BUCKET_NAME = 'bhargava-s33'

    EC2_PUBLIC_IP = '34.229.20.232'
}

stages {

    stage('Checkout') {
        steps {
            echo '===== CHECKOUT SOURCE CODE ====='
            checkout scm
        }
    }

    stage('Build Docker Image') {
        steps {
            echo '===== BUILD DOCKER IMAGE ====='

            sh '''
                docker build --no-cache -t ${IMAGE_NAME} .
            '''
        }
    }

    stage('Test MySQL Configuration') {
        steps {
            echo '===== TEST MYSQL CONFIGURATION ====='

            sh '''
                if [ -z "$MYSQL_PASSWORD" ]; then
                    echo "ERROR: MYSQL_PASSWORD IS EMPTY"
                    exit 1
                fi

                echo "SUCCESS: MYSQL_PASSWORD IS CONFIGURED"
            '''
        }
    }

    stage('Stop Old Container') {
        steps {
            echo '===== STOP OLD CONTAINER ====='

            sh '''
                docker rm -f ${CONTAINER_NAME} || true
            '''
        }
    }

    stage('Deploy Container') {
        steps {
            echo '===== DEPLOY NEW CONTAINER ====='

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

                curl -f http://${EC2_PUBLIC_IP}:5000/
            '''
        }
    }
}

post {

    success {
        echo '''
```

========================================
CLOUD FILE SHARING DEPLOYMENT SUCCESS
=====================================

Application:
http://34.229.20.232:5000/

Docker Container:
cloud-sharing-file

Docker Image:
cloud-file-sharing:latest

========================================
'''
}

```
    failure {
        echo '''
```

========================================
CLOUD FILE SHARING DEPLOYMENT FAILED
====================================

Checking Docker container and logs...

========================================
'''

```
        sh '''
            echo "===== DOCKER CONTAINERS ====="
            docker ps -a

            echo "===== APPLICATION LOGS ====="
            docker logs ${CONTAINER_NAME} || true
        '''
    }
}
```

}
