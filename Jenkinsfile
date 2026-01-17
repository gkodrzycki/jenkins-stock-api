pipeline {
    agent {
        kubernetes {
            inheritFrom 'uv-agent'
        }
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Verify tools') {
            steps {
                container('uv') {
                    sh 'python --version'
                    sh 'uv --version'
                }
            }
        }

        stage('Install dependencies') {
            steps {
                container('uv') {
                    sh 'uv sync'
                }
            }
        }

        stage('Run tests') {
            steps {
                container('uv') {
                    sh 'uv run pytest'
                }
            }
        }

        stage('Archive Artifacts') {
            steps {
                container('uv') {
                    sh "tar -czf jenkins-stock-api-v${BUILD_NUMBER}.tar.gz src pyproject.toml uv.lock Dockerfile"
                    sh "curl -F \"file=@jenkins-stock-api-v${BUILD_NUMBER}.tar.gz\" \"http://miniserve.jenkins.svc.cluster.local:8080/upload?path=/\""
                }
            }
        }

        stage('Trigger Deploy') {
            steps {
                script {
                   echo "Triggering deployment pipeline..."
                    build job: 'deploy-app', wait: false, parameters: [
                        string(name: 'UPSTREAM_BUILD_NUMBER', value: "${BUILD_NUMBER}")
                    ]
                }
            }
        }
    }
}
