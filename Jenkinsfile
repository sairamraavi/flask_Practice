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
            options {
                timeout(time: 5, unit: 'MINUTES')
            }
            steps {
                echo "========== CHECKOUT =========="
                git(
                    branch: 'main',
                    credentialsId: 'github-creds',
                    url: 'https://github.com/sairamraavi/flask_Practice.git'
                )
                sh 'pwd'
                sh 'ls -la'
                sh 'git log --oneline -1'
            }
        }
        stage('Install Dependencies') {
            options {
                timeout(time: 10, unit: 'MINUTES')
            }
            steps {
                echo "========== INSTALL DEPENDENCIES =========="
                sh 'python3 --version'
                sh 'pip3 --version'
                sh '''
                    python3 -m pip install --upgrade pip --break-system-packages
                '''
                sh '''
                    pip3 install --break-system-packages -r requirements.txt
                '''
                sh 'echo "Dependencies Installed Successfully"'
            }
        }
        stage('Code Formatting') {
            options {
                timeout(time: 2, unit: 'MINUTES')
            }
            steps {
                echo "========== BLACK =========="
                sh '''
                    echo "Running Black..."
                    python3 -m black --check . || true
                    echo "Black Completed"
                '''
            }
        }
        stage('Unit Tests') {
            options {
                timeout(time: 5, unit: 'MINUTES')
            }
            environment {
                MONGO_URI = credentials('mongo-uri')
            }
            steps {
                echo "========== PYTEST =========="
                sh '''
                    echo "Running Pytest..."
                    python3 -m pytest -v
                    echo "Pytest Completed"
                '''
            }
        }
        stage('Security Scan') {
            options {
                timeout(time: 3, unit: 'MINUTES')
            }
            steps {
                echo "========== BANDIT =========="
                sh '''
                    echo "Running Bandit..."
                    python3 -m bandit -r . || true
                    echo "Bandit Completed"
                '''
            }
        }
        stage('Lint') {
            options {
                timeout(time: 10, unit: 'MINUTES')
            }
            steps {
                echo "========== PYLINT =========="
                sh '''
                    echo "Starting pylint..."
                    date
                    pwd
                    ls -la
                    python3 -m pylint --exit-zero --disable=missing-module-docstring,missing-function-docstring,missing-class-docstring app.py test_app.py
                    echo "Pylint completed."
                    date
                '''
            }
        }
        stage('Deploy to Staging') {
            options {
                timeout(time: 10, unit: 'MINUTES')
            }
            steps {
                echo "========== DEPLOY =========="
                sshagent(credentials: ['flask-server']) {
                    sh """
                    ssh -o StrictHostKeyChecking=no ${DEPLOY_USER}@${DEPLOY_HOST} << EOF

                    set -euo pipefail

                    echo "===== Connected to Flask Server ====="
                    hostname
                    pwd

                    cd ${APP_DIR}

                    echo "Repository Status"
                    git status

                    echo "Current Branch"
                    git branch

                    echo "Pulling Latest Code"
                    git pull origin main

                    if [ ! -d venv ]; then
                        echo "Creating Python virtual environment"
                        python3 -m venv venv
                    fi

                    echo "Activating Virtual Environment"
                    source venv/bin/activate

                    echo "Installing Python Packages"
                    python -m pip install --upgrade pip
                    python -m pip install -r requirements.txt

                    echo "Restarting Flask Service"
                    sudo systemctl restart flask-app || sudo systemctl start flask-app

                    echo "Checking Flask Status"
                    sudo systemctl status flask-app --no-pager

                    echo "Deployment Successful"

EOF
                    """
                }
            }
        }
    }
    post {
        success {
            echo "========================================"
            echo "BUILD SUCCESSFUL"
            echo "APPLICATION DEPLOYED SUCCESSFULLY"
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