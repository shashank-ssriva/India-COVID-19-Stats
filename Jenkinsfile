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
                withSonarQubeEnv('SonarQube on cloud', credentialsId: 'sonar-cloud-login'){
                sh "/Users/admin/Downloads/sonar-scanner-4.0.0.1744-macosx/bin/sonar-scanner"
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
