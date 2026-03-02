pipeline {
    agent any

    parameters {
        choice(
            name: 'ACTION',
            choices: ['DEPLOY', 'ROLLBACK'],
            description: 'Choose DEPLOY for new version or ROLLBACK to previous image'
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

        stage('Clone Repo') {
            steps {
                git branch: 'main', url: 'https://github.com/Suhar121/docker-prac.git'
            }
        }

        stage('Prepare Image') {
            steps {
                script {

                    if (params.ACTION == 'ROLLBACK') {

                        def tags = sh(
                            script: "docker images ${IMAGE_NAME} --format '{{.Tag}}' | grep -v latest",
                            returnStdout: true
                        ).trim().split("\n")

                        if (tags.size() == 0) {
                            error("No images available for rollback")
                        }

                        def selected = input(
                            message: "Select version to rollback",
                            parameters: [
                                choice(name: 'VERSION', choices: tags.join('\n'), description: 'Choose image tag')
                            ]
                        )

                        env.FULL_IMAGE = "${IMAGE_NAME}:${selected}"
                        echo "Rolling back to ${env.FULL_IMAGE}"

                    } else {

                        // get branch name
                        def BRANCH = sh(
                            script: "git rev-parse --abbrev-ref HEAD",
                            returnStdout: true
                        ).trim()

                        // get commit short id
                        def COMMIT = sh(
                            script: "git rev-parse --short HEAD",
                            returnStdout: true
                        ).trim()

                        // get date
                        def DATE = sh(
                            script: "date +%Y-%m-%d",
                            returnStdout: true
                        ).trim()

                        def TAG = "${BRANCH}-${DATE}-${COMMIT}"
                        env.FULL_IMAGE = "${IMAGE_NAME}:${TAG}"

                        echo "Building new image ${env.FULL_IMAGE}"

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
                docker stop $STAGING_CONTAINER || true
                docker rm $STAGING_CONTAINER || true

                docker run -d -p $STAGING_PORT:8000 \
                --name $STAGING_CONTAINER $FULL_IMAGE
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
                docker stop $PROD_CONTAINER || true
                docker rm $PROD_CONTAINER || true

                docker run -d -p $PROD_PORT:8000 \
                --name $PROD_CONTAINER $FULL_IMAGE
                '''
            }
        }
    }
}