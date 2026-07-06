pipeline {
    agent any

    environment {
        SECRET_KEY = 'SairamFlaskApp'
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

                echo '========== BUILD =========='

                sh '''
                echo "Creating .env file..."

                cat > .env <<EOF
MONGO_URI=$MONGO_URI
SECRET_KEY=$SECRET_KEY
EOF

                echo "Workspace Contents:"
                ls -la

                python3 --version

                python3 -m pip install --break-system-packages -r requirements.txt
                '''
            }
        }

        stage('Test') {
            environment {
                MONGO_URI = credentials('mongo-uri')
            }

            steps {

                echo '========== TEST =========='

                sh '''
                python3 -m pytest -v
                '''
            }
        }

        stage('Deploy') {
            steps {

                echo '========== DEPLOY =========='

                sshagent(credentials: ['flask-server']) {

                    sh '''
                    ssh -o StrictHostKeyChecking=no ubuntu@13.203.103.161 "
                        cd /home/ubuntu/flask_Practice

                        git pull origin main

                        source venv/bin/activate

                        pip install -r requirements.txt

                        sudo systemctl restart flask-app

                        sudo systemctl status flask-app --no-pager

                        echo Deployment Successful
                    "
                    '''
                }
            }
        }
    }

    post {

        always {
            echo 'Pipeline Finished.'
        }

        success {

            echo 'Pipeline Successful!'

            emailext(
                to: 'YOUR_EMAIL@gmail.com',
                subject: "SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
The Jenkins build completed successfully.

Job: ${env.JOB_NAME}
Build Number: ${env.BUILD_NUMBER}
Build URL: ${env.BUILD_URL}

Status: SUCCESS
"""
            )
        }

        failure {

            echo 'Pipeline Failed!'

            emailext(
                to: 'sairamraavi1994@gmail.com',
                subject: "FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
The Jenkins build has failed.

Job: ${env.JOB_NAME}
Build Number: ${env.BUILD_NUMBER}
Build URL: ${env.BUILD_URL}

Status: FAILURE
"""
            )
        }
    }
}