pipeline {
    agent any
    environment {
        APPLICATION = "geoip-lite-api"
        GIT_COMMIT = sh (
            script: "git rev-parse HEAD",
            returnStdout: true
        ).trim()
        SLACK_CHANNEL = "#jenkins_pipelines"
    }
    stages {
        stage('Start') {
            steps {
                slackSend([
                    channel: "${env.SLACK_CHANNEL}",
                    color: "good",
                    message: "<${env.BUILD_URL}|${currentBuild.fullDisplayName}> started with <https://github.com/gengo/${env.APPLICATION}/commit/${env.GIT_COMMIT}|${env.GIT_COMMIT}>"
                ])
            }
        }
        stage('Build') {
            steps {
                sh "docker build . -t gcr.io/gengo-internal/${env.APPLICATION}:latest"
                sh "docker tag gcr.io/gengo-internal/${env.APPLICATION}:latest gcr.io/gengo-internal/${env.APPLICATION}:${env.GIT_COMMIT}"
            }
            post {
                failure {
                    slackSend([
                        channel: "${env.SLACK_CHANNEL}",
                        color: "danger",
                        message: "<${env.BUILD_URL}|${currentBuild.fullDisplayName}> failed on Build"
                    ])
                }
            }
        }
        stage('Push') {
            steps {
                withDockerRegistry(
                    registry: [
                        credentialsId: 'gcr:gengo-internal-gcr',
                        url: 'https://gcr.io/gengo-internal'
                    ]
                ) {
                    sh "docker push gcr.io/gengo-internal/${env.APPLICATION}:${env.GIT_COMMIT}"
                    sh "docker push gcr.io/gengo-internal/${env.APPLICATION}:latest"
                }
            }
            post {
                failure {
                    slackSend([
                        channel: "${env.SLACK_CHANNEL}",
                        color: "danger",
                        message: "<${env.BUILD_URL}|${currentBuild.fullDisplayName}> failed on Push"
                    ])
                }
            }
        }
        stage('Deploy') {
            steps {
                build job: 'tools/goship-deployer',
                parameters: [
                    string(name: 'APP_NAME', value: "${env.APPLICATION}"),
                    string(name: 'BRANCH', value: "${env.GIT_COMMIT}"),
                ]
            }
            post {
                failure {
                    slackSend([
                        channel: "${env.SLACK_CHANNEL}",
                        color: "danger",
                        message: "<${env.BUILD_URL}|${currentBuild.fullDisplayName}> failed on Deploy"
                    ])
                }
            }
        }
        stage('Finish') {
            steps {
                slackSend([
                    channel: "${env.SLACK_CHANNEL}",
                    color: "good",
                    message: "<${env.BUILD_URL}|${currentBuild.fullDisplayName}> finished successfully"
                ])
            }
        }
    }
}
