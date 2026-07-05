pipeline {
    agent any
    options {
        skipDefaultCheckout(true)
        timestamps()
        ansiColor('xterm')
        disableConcurrentBuilds()
    }
    environment {
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
                sh "git log --oneline -1"
            }
        }
        stage('Install Dependencies') {
            steps {
                echo "========== INSTALL DEPENDENCIES =========="
                sh '''
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
                    black --check . || true
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
                        ssh -o StrictHostKeyChecking=no ${DEPLOY_USER}@${DEPLOY_HOST} << 'EOF'

                        set -e

                        echo "===== Connected to Flask Server ====="

                        cd ${APP_DIR}

                        echo "Current Directory:"
                        pwd

                        echo "Current Branch:"
                        git branch

                        echo "Pulling latest code..."
                        git pull origin main

                        echo "Activating Virtual Environment..."
                        source venv/bin/activate

                        echo "Installing Dependencies..."
                        pip install -r requirements.txt

                        echo "Restarting Flask Service..."
                        sudo systemctl restart flask-app

                        echo "Checking Service Status..."
                        sudo systemctl status flask-app --no-pager

                        echo "Deployment Completed Successfully"

EOF
                    """
                }
            }
        }
    }
    post {
        success {
            echo "===================================="
            echo "BUILD SUCCESSFUL"
            echo "Application Successfully Deployed"
            echo "===================================="
        }
        failure {
            echo "===================================="
            echo "BUILD FAILED"
            echo "===================================="
        }
        always {
            cleanWs()
        }
    }
}