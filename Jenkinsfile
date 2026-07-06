pipeline {
    agent any

    options {
        timestamps()
        timeout(time: 20, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    environment {
        GIT_REPO      = 'https://github.com/sairamraavi/flask_Practice.git'
        BRANCH        = 'main'
        FLASK_SERVER  = '13.203.103.161'
        APP_DIR       = '/home/ubuntu/flask_Practice'
        SECRET_KEY    = 'SairamFlaskApp'
    }

    stages {

        stage('Checkout Source') {
            steps {
                cleanWs()

                git(
                    branch: "${BRANCH}",
                    credentialsId: 'github-creds',
                    url: "${GIT_REPO}"
                )
            }
        }

        stage('Build') {

            environment {
                MONGO_URI = credentials('mongo-uri')
            }

            steps {

                echo "========== BUILD =========="

                sh '''
                set -e

                echo "Creating .env file..."

                cat > .env <<EOF
MONGO_URI=$MONGO_URI
SECRET_KEY=$SECRET_KEY
EOF

                python3 --version

                python3 -m venv jenkins_venv

                . jenkins_venv/bin/activate

                python -m pip install --upgrade pip

                pip install -r requirements.txt

                ls -la
                '''
            }
        }

        stage('Unit Test') {

            steps {

                echo "========== UNIT TEST =========="

                sh '''
                set -e

                . jenkins_venv/bin/activate

                python -m pytest -v
                '''
            }
        }

        stage('Deploy to Flask Server') {

            steps {

                echo "========== DEPLOY =========="

                sshagent(credentials: ['flask-server']) {

                    sh '''
                    set -e

                    echo "Copying .env file..."

                    scp -o StrictHostKeyChecking=no .env ubuntu@$FLASK_SERVER:/tmp/.env

                    echo "Deploying application..."

                    ssh -o StrictHostKeyChecking=no ubuntu@$FLASK_SERVER << EOF

                        set -e

                        cd $APP_DIR

                        git pull origin main

                        if [ ! -d venv ]
                        then
                            python3 -m venv venv
                        fi

                        source venv/bin/activate

                        pip install -r requirements.txt

                        cp /tmp/.env .env

                        sudo systemctl restart flask-app

                        sudo systemctl is-active flask-app

                        rm -f /tmp/.env

EOF
                    '''
                }
            }
        }

        stage('Health Check') {

            steps {

                echo "========== HEALTH CHECK =========="

                sh '''
                sleep 5

                curl -I http://13.203.103.161
                '''
            }
        }
    }

    post {

        always {

            echo "Cleaning workspace..."

            sh '''
            rm -rf jenkins_venv
            rm -f .env
            '''

            cleanWs()
        }

        success {

            echo "BUILD SUCCESSFUL"

            emailext(
                to: 'sairamraavi1994@gmail.com',
                subject: "SUCCESS : ${JOB_NAME} #${BUILD_NUMBER}",
                body: """
Job Name : ${JOB_NAME}

Build Number : ${BUILD_NUMBER}

Status : SUCCESS

Build URL :
${BUILD_URL}
"""
            )
        }

        failure {

            echo "BUILD FAILED"

            emailext(
                to: 'sairamraavi1994@gmail.com',
                subject: "FAILED : ${JOB_NAME} #${BUILD_NUMBER}",
                body: """
Job Name : ${JOB_NAME}

Build Number : ${BUILD_NUMBER}

Status : FAILED

Build URL :
${BUILD_URL}
"""
            )
        }
    }
}