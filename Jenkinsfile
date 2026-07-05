pipeline {
    agent any
    options {
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

                    python3 -m venv venv

                    . venv/bin/activate

                    python -m pip install --upgrade pip

                    pip install -r requirements.txt
                '''
            }
        }
        stage('Code Formatting') {
            steps {
                echo "========== BLACK =========="
                sh '''
                    . venv/bin/activate

                    black --check .
                '''
            }
        }
        stage('Lint') {
            steps {
                echo "========== PYLINT =========="
                sh '''
                    . venv/bin/activate

                    pylint *.py || true
                '''
            }
        }
        stage('Security Scan') {
            steps {
                echo "========== BANDIT =========="
                sh '''
                    . venv/bin/activate

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
                    set -e

                    . venv/bin/activate

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

                        echo "=================================="
                        echo "Deploying Flask Application"
                        echo "=================================="

                        cd ${APP_DIR}

                        echo "Current Directory:"
                        pwd

                        echo "Pulling Latest Code..."
                        git pull origin main

                        echo "Activating Virtual Environment..."
                        source venv/bin/activate

                        echo "Installing Dependencies..."
                        pip install -r requirements.txt

                        echo "Restarting Flask Service..."
                        sudo systemctl restart flask-app

                        echo "Checking Flask Service..."
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
            emailext(
                subject: "SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                Build Status : SUCCESS

                Job Name : ${env.JOB_NAME}
                Build No : ${env.BUILD_NUMBER}

                URL:
                ${env.BUILD_URL}
                """,
                to: "YOUR_EMAIL@gmail.com"
            )
        }
        failure {
            echo "========================================"
            echo "BUILD FAILED"
            echo "========================================"
            emailext(
                subject: "FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
                Build Status : FAILED

                Job Name : ${env.JOB_NAME}
                Build No : ${env.BUILD_NUMBER}

                URL:
                ${env.BUILD_URL}
                """,
                to: "YOUR_EMAIL@gmail.com"
            )
        }
        always {
            cleanWs()
        }
    }
}