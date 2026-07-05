pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
        timestamps()
    }

    environment {
        DEPLOY_HOST = "13.232.118.126"
        DEPLOY_USER = "ubuntu"
        APP_DIR = "/home/ubuntu/flask_Practice"
    }

    stages {

        stage('Checkout') {
            steps {
                git(
                    branch: 'main',
                    credentialsId: 'github-creds',
                    url: 'https://github.com/sairamraavi/flask_Practice.git'
                )
            }
        }

        stage('Build') {
            environment {
                MONGO_URI = credentials('mongo-uri')
            }

            steps {
                sh '''
                    python3 -m pytest --version
                    python3 -m pip install --break-system-packages -r requirements.txt
                '''
            }
        }

        stage('Test') {
            environment {
                MONGO_URI = credentials('mongo-uri')
            }

            steps {
                sh '''
                    python3 -m pytest -v
                '''
            }
        }

        stage('Deploy') {
            steps {

                sshagent(credentials: ['flask-server']) {

                    sh """
ssh -o StrictHostKeyChecking=no ubuntu@13.232.118.126 '
cd /home/ubuntu/flask_Practice || exit 1

git fetch origin
git reset --hard origin/main

source venv/bin/activate

pip install -r requirements.txt >/dev/null 2>&1

sudo systemctl restart flask-app

sudo systemctl is-active flask-app
'
"""
                }

            }
        }

    }

    post {
        success {
            echo 'BUILD SUCCESS'
            cleanWs()
        }

        failure {
            echo 'BUILD FAILED'
            cleanWs()
        }
    }
}