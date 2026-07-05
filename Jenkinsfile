pipeline {
    agent any
    options {
        skipDefaultCheckout(true)
        timestamps()
        ansiColor('xterm')
        disableConcurrentBuilds()
    }
    environment {
        APP_NAME = "Flask Student Management"
        DEPLOY_HOST = "13.232.118.126"
        DEPLOY_USER = "ubuntu"
        APP_DIR = "/home/ubuntu/flask_Practice"
    }
    stages {
        stage('Checkout Source') {
            steps {
                echo "========== CHECKOUT =========="
                git(
                    branch: 'main',
                    credentialsId: 'github-creds',
                    url: 'https://github.com/sairamraavi/flask_Practice.git'
                )
                sh 'ls -la'
            }
        }
        stage('Build') {
            steps {
                echo "========== BUILD =========="
                sh '''
                    set -e

                    python3 --version
                    pip3 --version

                    python3 -m pip install --upgrade pip --break-system-packages

                    pip3 install --break-system-packages -r requirements.txt
                '''
            }
        }
        stage('Code Formatting') {
            steps {
                echo "========== BLACK =========="
                sh '''
                    black --check .
                '''
            }
        }
        stage('Lint') {
            steps {
                echo "========== PYLINT =========="
                sh '''
                    pylint *.py || true
                '''
            }
        }
        stage('Security Scan') {
            steps {
                echo "========== BANDIT =========="
                sh '''
                    bandit -r . || true
                '''
            }
        }
        stage('Unit Tests') {
            environment {
                MONGO_URI = credentials('mongo-uri')
            }
            steps {
                echo "========== PYTEST =========="
                sh '''
                    pytest -v
                '''
            }
        }
        stage('Deploy to Staging') {
            steps {
                echo "========== DEPLOY =========="
                sshagent(credentials: ['flask-server']) {
                    sh """
                    ssh -o StrictHostKeyChecking=no ${DEPLOY_USER}@${DEPLOY_HOST} '
                        set -e

                        echo "======================================="
                        echo "Deploying Flask Application"
                        echo "======================================="

                        cd ${APP_DIR}

                        echo "Pulling latest code..."
                        git pull origin main

                        echo "Installing dependencies..."
                        pip3 install --break-system-packages -r requirements.txt

                        echo "Restarting Flask service..."
                        sudo systemctl restart flask-app

                        echo "Checking service status..."
                        sudo systemctl status flask-app --no-pager

                        echo "Deployment Successful"

                    '
                    """
                }
            }
        }
    }
    post {
        success {
            echo "========================================"
            echo "BUILD SUCCESSFUL"
            echo "Application Successfully Deployed"
            echo "========================================"
        }
        failure {
            echo "========================================"
            echo "BUILD FAILED"
            echo "========================================"
        }
        always {
            cleanWs()
        }
    }
}