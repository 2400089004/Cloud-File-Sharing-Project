pipeline {
    agent any

    stages {

        stage('Clone') {
            steps {
                git branch: 'main',
                    url: 'git@github.com:2400089004/Cloud-File-Sharing-Project.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Deploy to EC2') {
            steps {
                sh '''
                    ssh -o StrictHostKeyChecking=no ubuntu@YOUR_EC2_IP "
                        cd ~/Cloud-File-Sharing-Project &&
                        git pull origin main &&
                        source venv/bin/activate &&
                        pip install -r requirements.txt
                    "
                '''
            }
        }
    }
}