pipeline {
    agent any

    environment {
        IMAGE_NAME = "fastapi-jenkins"
        CONTAINER_NAME = "fastapi"
        PORT = "8000"
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
                dir('backend') {
                    sh '''
                    echo "Removing old image..."
                    docker rmi $IMAGE_NAME || true

                    echo "Building new image..."
                    docker build -t $IMAGE_NAME .
                    '''
                }
            }
        }

        stage('Deploy Container') {
            steps {
                sh '''
                echo "Stopping old container..."
                docker stop $CONTAINER_NAME || true
                docker rm $CONTAINER_NAME || true

                echo "Running new container..."
                docker run -d -p $PORT:$PORT \
                --name $CONTAINER_NAME $IMAGE_NAME

                echo "Running containers:"
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