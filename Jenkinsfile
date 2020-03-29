pipeline {
    agent any

    stages {
        stage('Check out code') {
            steps {
                git 'https://github.com/shashank-ssriva/India-COVID-19-Stats.git'
            }
        }
        stage('SonarQube analysis') {
            steps {
                withSonarQubeEnv('SonarQube on cloud'){
                def scannerHome = tool name: 'Sonar on Mac', type: 'hudson.plugins.sonar.SonarRunnerInstallation';
                sh "$scannerHome/sonar-scanner"
                }
            }
        }
        stage('Deploy to Heroku') {
            steps {
                sh label: '', script: 'sh .deploy_scripts/deploy_heroku.sh'
            }
        }
    }
}
