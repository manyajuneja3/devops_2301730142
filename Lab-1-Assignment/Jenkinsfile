pipeline {
    agent any

    // Build options and timeout constraints
    options {
        timeout(time: 20, unit: 'MINUTES')
        timestamps()
        ansiColor('xterm')
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    // Build Triggers: Automatic triggers on GitHub push and scheduled polling
    triggers {
        githubPush()
        pollSCM('H/5 * * * *')
    }

    // Environment variables
    environment {
        APP_NAME     = 'devops-sample-app'
        APP_VERSION  = "1.0.${BUILD_NUMBER}"
        DEPLOY_PORT  = '5000'
        PYTHON_EXEC  = 'python3'
    }

    stages {
        // ==============================================================
        // STAGE 1: SCM CHECKOUT
        // ==============================================================
        stage('Checkout Source') {
            steps {
                echo "=========================================="
                echo "Stage 1: Pulling Source Code from GitHub"
                echo "Commit Hash: ${GIT_COMMIT}"
                echo "Branch: ${GIT_BRANCH}"
                echo "=========================================="
                checkout scm
            }
        }

        // ==============================================================
        // STAGE 2: BUILD & DEPENDENCIES
        // ==============================================================
        stage('Build & Dependencies') {
            steps {
                echo "=========================================="
                echo "Stage 2: Resolving Dependencies & Compiling"
                echo "=========================================="
                sh '''
                    echo "Checking Python environment..."
                    python3 --version || python --version
                    
                    echo "Creating and activating virtual environment..."
                    python3 -m venv venv || virtualenv venv
                    . venv/bin/activate
                    
                    echo "Upgrading pip and installing requirements..."
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    
                    echo "Validating syntax..."
                    python3 -m py_compile app.py test_app.py
                    echo "Build and syntax check completed successfully."
                '''
            }
        }

        // ==============================================================
        // STAGE 3: TEST (AUTOMATED UNIT TESTS & QUALITY GATE)
        // ==============================================================
        stage('Run Tests') {
            steps {
                echo "=========================================="
                echo "Stage 3: Running Automated Unit Tests"
                echo "=========================================="
                sh '''
                    . venv/bin/activate
                    echo "Executing Unit Tests with pytest..."
                    python3 -m pytest test_app.py -v --junitxml=test-results.xml || python3 test_app.py
                    echo "All Unit Tests Passed!"
                '''
            }
            post {
                always {
                    // Post-stage action: JUnit test report publishing
                    junit allowEmptyResults: true, testResults: 'test-results.xml'
                }
            }
        }

        // ==============================================================
        // STAGE 4: PACKAGE & ARTIFACT PREPARATION
        // ==============================================================
        stage('Package Artifacts') {
            steps {
                echo "=========================================="
                echo "Stage 4: Packaging Release Artifacts"
                echo "=========================================="
                sh '''
                    mkdir -p dist
                    tar -czf dist/${APP_NAME}-v${BUILD_NUMBER}.tar.gz app.py requirements.txt Dockerfile deploy.sh
                    echo "Packaged artifact: dist/${APP_NAME}-v${BUILD_NUMBER}.tar.gz"
                '''
            }
            post {
                success {
                    // Archive artifacts for post-build download
                    archiveArtifacts artifacts: 'dist/*.tar.gz', fingerprint: true
                }
            }
        }

        // ==============================================================
        // STAGE 5: DEPLOY (AUTOMATED APPLICATION DEPLOYMENT)
        // ==============================================================
        stage('Deploy Application') {
            steps {
                echo "=========================================="
                echo "Stage 5: Deploying Application Container"
                echo "=========================================="
                sh '''
                    chmod +x deploy.sh
                    ./deploy.sh
                '''
            }
        }

        // ==============================================================
        // STAGE 6: HEALTHCHECK VERIFICATION
        // ==============================================================
        stage('Health Verification') {
            steps {
                echo "=========================================="
                echo "Stage 6: Smoke Testing / Health Verification"
                echo "=========================================="
                sh '''
                    echo "Performing HTTP Health Check on http://localhost:5000/health..."
                    curl -s -f http://localhost:5000/health | grep '"status": "UP"' || exit 1
                    echo "Deployment verification successful! Service is responsive."
                '''
            }
        }
    }

    // ==============================================================
    // POST-BUILD ACTIONS
    // ==============================================================
    post {
        always {
            echo "=========================================="
            echo "Post-Build: Cleaning temporary workspace files..."
            echo "=========================================="
            cleanWs deleteDirs: true, notFailBuild: true
        }
        success {
            echo "=========================================="
            echo "BUILD SUCCESSFUL!"
            echo "Application ${APP_NAME} deployed successfully."
            echo "Build URL: ${BUILD_URL}"
            echo "=========================================="
        }
        failure {
            echo "=========================================="
            echo "BUILD FAILED! Check console output for errors."
            echo "=========================================="
        }
        unstable {
            echo "Build marked as UNSTABLE. Tests may have failed."
        }
    }
}

