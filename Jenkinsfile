pipeline {
    agent any
    options {
        timestamps()
        ansiColor('xterm')
    }
    environment {
        APP_NAME = "Flask Student App"
        DEPLOY_HOST = "13.232.118.126"
        DEPLOY_USER = "ubuntu"
        APP_DIR = "/home/ubuntu/flask_Practice"
    }
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                credentialsId: 'github-creds',
                url: 'https://github.com/sairamraavi/flask_Practice.git'
            }
        }
        stage('Build') {
            steps {
                sh '''

                python3 -m venv venv

                . venv/bin/activate

                python -m pip install --upgrade pip

                pip install -r requirements.txt

                '''
            }
        }
        stage('Code Formatting') {
            steps {
                sh '''

                . venv/bin/activate

                black --check .

                '''
            }
        }
        stage('Lint') {
            steps {
                sh '''

                . venv/bin/activate

                pylint *.py || true

                '''
            }
        }
        stage('Security Scan') {
            steps {
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
                sh '''

                . venv/bin/activate

                pytest -v

                '''
            }
        }
        stage('Deploy To Staging') {
            steps {
                sshagent(credentials: ['flask-server']) {
                    sh '''

                    ssh -o StrictHostKeyChecking=no ${DEPLOY_USER}@${DEPLOY_HOST} << EOF

                    cd ${APP_DIR}

                    git pull origin main

                    source venv/bin/activate

                    pip install -r requirements.txt

                    sudo systemctl restart flask-app

                    sudo systemctl status flask-app --no-pager

                    EOF

                    '''
                }
            }
        }
    }
    post {
        success {
            echo "========================================"
            echo "Deployment Successful"
            echo "========================================"
        }
        failure {
            echo "========================================"
            echo "Deployment Failed"
            echo "========================================"
        }
        always {
            cleanWs()
        }
    }
}