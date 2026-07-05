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

        stage('Checkout') {
            steps {
                git branch: 'main',
                    credentialsId: 'github-creds',
                    url: 'https://github.com/sairamraavi/flask_Practice.git'
            }
        }

        stage('Install Dependencies') {
            steps {

                sh 'python3 --version'
                sh 'pip3 --version'

                sh '''
                python3 -m pip install --upgrade pip --break-system-packages
                '''

                sh '''
                pip3 install --break-system-packages -r requirements.txt
                '''
            }
        }

        stage('Code Formatting') {
            steps {
                sh 'black --check .'
            }
        }

        stage('Lint') {
            steps {
                sh 'pylint *.py || true'
            }
        }

        stage('Security Scan') {
            steps {
                sh 'bandit -r . || true'
            }
        }

        stage('Unit Tests') {

            environment {
                MONGO_URI = credentials('mongo-uri')
            }

            steps {
                sh 'pytest -v'
            }

        }

        stage('Deploy') {

            steps {

                sshagent(credentials: ['flask-server']) {

                    sh """
                    ssh -o StrictHostKeyChecking=no ${DEPLOY_USER}@${DEPLOY_HOST} '
                        set -e

                        cd ${APP_DIR}

                        echo "Pulling latest code..."

                        git pull origin main

                        echo "Installing packages in virtual environment..."

                        source venv/bin/activate

                        pip install -r requirements.txt

                        echo "Restarting Flask..."

                        sudo systemctl restart flask-app

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

            echo "================================"
            echo "BUILD SUCCESSFUL"
            echo "================================"

        }

        failure {

            echo "================================"
            echo "BUILD FAILED"
            echo "================================"

        }

        always {

            cleanWs()

        }

    }

}