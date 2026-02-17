pipeline {
    agent any

    environment {
        JIRA_URL = "https://getsetgo.atlassian.net"
        JIRA_ISSUE = "DWS-1"
        JIRA_CRED = credentials('Jira_API_Key')
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/jas09/DemoWebShop_Playwright_Feb.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '''
                    python -m venv venv
                    call venv\\Scripts\\activate
                    venv\\Scripts\\python.exe -m pip install --upgrade pip
                    venv\\Scripts\\python.exe -m pip install -r requirements.txt
                '''
            }
        }

        stage('Run Playwright Tests') {
            steps {
                bat '''
                    call venv\\Scripts\\activate
                    pytest -v -s -n 3 --browser_name=chrome --tracing=on ^
						--junitxml=results/playwright-results.xml ^
						--html=results/report.html --self-contained-html
                '''
            }
        }

        stage('Publish JUnit Results') {
            steps {
                junit 'results/playwright-results.xml'
            }
        }

        stage('Update Jira') {
            steps {
                script {
                    def status = currentBuild.currentResult == 'SUCCESS' ? "PASS" : "FAIL"
                    def message = "Playwright automation run completed. Status: ${status}. Build: ${env.BUILD_URL}"
                    bat """
                        curl -X POST ^
                        --ssl-no-revoke ^
                        -u ${JIRA_CRED_USR}:${JIRA_CRED_PSW} ^
                        -H "Content-Type: application/json" ^
                        --data "{\\"body\\":{\\"type\\":\\"doc\\",\\"version\\":1,\\"content\\":[{\\"type\\":\\"paragraph\\",\\"content\\":[{\\"type\\":\\"text\\",\\"text\\":\\"${message}\\"}]}]}}" ^
                        ${JIRA_URL}/rest/api/3/issue/${JIRA_ISSUE}/comment
                    """
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'results/*.xml', allowEmptyArchive: true
        }
    }
}