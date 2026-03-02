pipeline {
    agent any

    parameters {
        choice(
            name: 'ACTION',
            choices: ['DEPLOY', 'ROLLBACK'],
            description: 'Choose DEPLOY for new version or ROLLBACK to previous image'
        )

        string(
            name: 'ROLLBACK_TAG',
            defaultValue: '',
            description: 'Enter image tag to rollback (only used if ROLLBACK selected)'
        )
    }

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

        stage('Prepare Image') {
            steps {
                script {

                    if (params.ACTION == 'ROLLBACK') {

                        if (!params.ROLLBACK_TAG) {
                            error("Rollback selected but no tag provided")
                        }

                        env.FULL_IMAGE = "${IMAGE_NAME}:${params.ROLLBACK_TAG}"
                        echo "Rolling back to image: ${env.FULL_IMAGE}"

                    } else {

                        def TAG = sh(
                            script: "git rev-parse --short HEAD",
                            returnStdout: true
                        ).trim()

                        env.FULL_IMAGE = "${IMAGE_NAME}:${TAG}"
                        echo "Building new image: ${env.FULL_IMAGE}"

                        dir('backend') {
                            sh "docker build -t ${env.FULL_IMAGE} ."
                        }
                    }
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