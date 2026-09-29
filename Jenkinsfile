pipeline {
agent any

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

    stage('Test MySQL Configuration') {
        steps {
            echo '===== Test MySQL Configuration ====='

            sh '''
                if [ -z "$MYSQL_PASSWORD" ]; then
                    echo "ERROR: MYSQL_PASSWORD is EMPTY"
                    exit 1
                fi

                echo "SUCCESS: MYSQL_PASSWORD is configured"
            '''
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
            echo '===== Check Container ====='

            sh '''
                sleep 3

                echo "===== Container Status ====="

                docker ps -a

                echo "===== Checking MYSQL_PASSWORD ====="

                if docker inspect ${CONTAINER_NAME} \
                    --format '{{range .Config.Env}}{{println .}}{{end}}' \
                    | grep -q '^MYSQL_PASSWORD='; then

                    echo "SUCCESS: MYSQL_PASSWORD exists inside container"

                else

                    echo "ERROR: MYSQL_PASSWORD missing inside container"
                    exit 1
                fi
            '''
        }
    }

    stage('Check Application Logs') {
        steps {
            echo '===== Application Logs ====='

            sh '''
                docker logs ${CONTAINER_NAME} || true
            '''
        }
    }

    stage('Verify Deployment') {
        steps {
            echo '===== Verify Deployment ====='

            sh '''
                sleep 5

                echo "===== Docker Containers ====="

                docker ps -a

                echo "===== Container Status ====="

                docker inspect ${CONTAINER_NAME} \
                    --format='Status: {{.State.Status}} ExitCode: {{.State.ExitCode}}'

                echo "===== Testing Application ====="

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
Cloud File Sharing Deployment SUCCESS
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
Cloud File Sharing Deployment FAILED
====================================

Checking container information...

========================================
'''

```
        sh '''
            echo "===== Docker Containers ====="

            docker ps -a

            echo "===== Container Logs ====="

            docker logs ${CONTAINER_NAME} || true
        '''
    }
}
```

}
