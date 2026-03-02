pipeline {
    agent any

    environment {
        IMAGE_NAME = "fastapi-jenkins"
        PROD_CONTAINER = "fastapi"
        STAGING_CONTAINER = "fastapi-staging"
        PROD_PORT = "8000"
        STAGING_PORT = "8001"
    }

    stages {

        stage('Check Environment') {
            steps {
                sh 'whoami'
                sh 'docker version'
                sh 'docker ps'
            }
        }

        stage('Clone Repo') {
            steps {
                git branch: 'main', url: 'https://github.com/Suhar121/docker-prac.git'
            }
        }

        stage('Build Docker Image') {
    steps {
        script {
            TAG = sh(
                script: "git rev-parse --short HEAD",
                returnStdout: true
            ).trim()

            env.IMAGE_TAG = TAG
            env.FULL_IMAGE = "${IMAGE_NAME}:${env.IMAGE_TAG}"

            echo "Building image ${env.FULL_IMAGE}"
        }

        dir('backend') {
            sh "docker build -t ${FULL_IMAGE} ."
        }
    }
}

        stage('Deploy to STAGING') {
            steps {
                sh '''
                echo "Deploying to STAGING..."

                docker stop $STAGING_CONTAINER || true
                docker rm $STAGING_CONTAINER || true

                docker run -d -p $STAGING_PORT:8000 \
                --name $STAGING_CONTAINER $FULL_IMAGE

                docker ps
                '''
            }
        }

        stage('Approve Production Deploy') {
            steps {
                input message: 'Staging looks good? Deploy to PRODUCTION?'
            }
        }

        stage('Deploy to PRODUCTION') {
            steps {
                sh '''
                echo "Deploying to PRODUCTION..."

                docker stop $PROD_CONTAINER || true
                docker rm $PROD_CONTAINER || true

                docker run -d -p $PROD_PORT:8000 \
                --name $PROD_CONTAINER $FULL_IMAGE

                docker ps
                '''
            }
        }
    }

    post {
        success {
            echo 'Deployment Successful 🚀'
        }
        failure {
            echo 'Deployment Failed ❌'
        }
    }
}