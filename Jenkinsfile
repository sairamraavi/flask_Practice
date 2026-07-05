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

        stage('Install Dependencies') {
            steps {
                echo "========== INSTALL DEPENDENCIES =========="

                sh '''
                    python3 -m pip install --upgrade pip --break-system-packages
                    pip3 install --break-system-packages -r requirements.txt
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
                    ssh -o StrictHostKeyChecking=no ${DEPLOY_USER}@${DEPLOY_HOST} << EOF

                    set -e

                    cd ${APP_DIR}

                    git pull origin main

                    source venv/bin/activate

                    python -m pip install -r requirements.txt

                    sudo systemctl restart flask-app

                    sudo systemctl status flask-app --no-pager

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