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

                sh 'git log --oneline -1'
            }
        }

        stage('Verify Dependencies') {
            steps {
                echo "========== VERIFY DEPENDENCIES =========="

                sh '''
                    python3 --version
                    pip3 --version

                    python3 -c "import flask"
                    python3 -c "import flask_pymongo"
                    python3 -c "import pytest"
                    python3 -c "import black"
                    python3 -c "import bandit"

                    echo "Dependencies Verified."
                '''
            }
        }

        stage('Code Formatting') {
            steps {
                echo "========== BLACK =========="

                sh '''
                    python3 -m black --check . || true
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
                    python3 -m pytest -v
                '''
            }
        }

        stage('Security Scan') {
            steps {

                echo "========== BANDIT =========="

                sh '''
                    python3 -m bandit -r . || true
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

                        cd ${APP_DIR}

                        echo "Current Branch:"
                        git branch

                        echo "Pulling Latest Code..."
                        git pull origin main

                        echo "Activating Virtual Environment..."
                        source venv/bin/activate

                        echo "Installing Dependencies..."
                        pip install -r requirements.txt

                        echo "Restarting Flask Service..."
                        sudo systemctl restart flask-app

                        echo "Checking Service..."
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

            echo "===================================="
            echo "BUILD SUCCESSFUL"
            echo "APPLICATION DEPLOYED SUCCESSFULLY"
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