#!groovy

def FAILED_STAGE

pipeline {
  agent none

  environment {
    REPO_NAME = "braintree-python"
    SLACK_CHANNEL = "#auto-team-sdk-builds"
  }

  options {
    buildDiscarder(logRotator(numToKeepStr: '50'))
    timestamps()
    timeout(time: 120, unit: 'MINUTES')
  }

  stages {
    stage("Audit") {
      parallel {
        stage("CodeQL") {
          agent {
            node {
              label ""
              customWorkspace "workspace/${REPO_NAME}"
            }
          }

          steps {
            codeQLv2(python: true)
          }

          post {
            failure {
              script {
                FAILED_STAGE = env.STAGE_NAME
              }
            }
          }
        }

        stage("SonarQube") {
          agent {
            node {
              label ""
              customWorkspace "workspace/${REPO_NAME}-sonar"
            }
          }

          steps {
            script {
              sh "docker build -t braintree-python ."
              sh "docker run --rm -e COVERAGE=1 -v \"\$(pwd):/braintree-python\" braintree-python /bin/bash -l -c 'pip3 install coverage && pip3 install . && python3 -m coverage run -m unittest discover tests/unit && python3 -m coverage xml'"
              executeSonarQubeScan()
            }
          }

          post {
            failure {
              script {
                FAILED_STAGE = env.STAGE_NAME
              }
            }
          }
        }
      }
    }

    stage("SDK Tests") {
      when {
        branch 'master'
      }

      parallel {
        stage("Python 3.5 Stretch") {
          agent {
            node {
              label ""
              customWorkspace "workspace/${REPO_NAME}"
            }
          }

          steps {
            build job: 'python_3.5-stretch_server_sdk_master', wait: true
          }

          post {
            failure {
              script {
                FAILED_STAGE = env.STAGE_NAME
              }
            }
          }
        }

        stage("Python 3.12 Bullseye") {
          agent {
            node {
              label ""
              customWorkspace "workspace/${REPO_NAME}"
            }
          }

          steps {
            build job: 'python_3.12-bullseye_server_sdk_master', wait: true
          }

          post {
            failure {
              script {
                FAILED_STAGE = env.STAGE_NAME
              }
            }
          }
        }
      }
    }
  }

  post {
    unsuccessful {
      slackSend color: "danger",
        channel: "${env.SLACK_CHANNEL}",
        message: "${env.JOB_NAME} - #${env.BUILD_NUMBER} Failure after ${currentBuild.durationString} at stage \"${FAILED_STAGE}\"(<${env.BUILD_URL}|Open>)"
    }
  }
}
