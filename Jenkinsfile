pipeline{
    agent any
    environment{
           // GEnerate random number between 0 and 1000
           DISCORD_WEBHOOK_URL = credentials('discord-webhook')
           INTEGRATION_TESTS_CONTAINERS_PREFIX = "${Math.abs(new Random().nextInt(1000+1))}"
           INTEGRATION_TESTS_NETWORK = "traefik_default"
    }

    stages{

        stage('Static code analysing') {
            stages {
                stage('Install dependencies')
                {
                    steps {
                        sh 'pip3 install pipenv==2021.5.29'
                        sh 'pipenv --rm || exit 0'
                        sh 'pipenv install --pre --dev'
                    }
                }
                stage ('PyDocStyle') {
                    steps {
                        sh 'pipenv run pydocstyle --config=.pydocstyle.ini ${MODULE_DIR_NAME}'
                    }
                }

                stage ('Mypy') {
                    steps {
                        sh 'pipenv run mypy -p notification_lib --config-file mypy.ini --no-incremental'
                    }
                }

                stage ('Pylint') {
                    steps {
                        sh 'pipenv run pylint notification_lib --output-format=parseable  --rcfile=.pylintrc'
                    }
                }
            }
        }

        stage('Launch-novu'){
            steps('Launch Novu'){
                sh "./tests/test_environment/start.sh  ${INTEGRATION_TESTS_NETWORK} ${INTEGRATION_TESTS_CONTAINERS_PREFIX}"
            }

        stage('Unit-test'){
            steps('Unit test'){
                sh "pipenv run coverage run --source=notification_lib -m pytest -v -s --junit-xml=reports/report.xml tests && pipenv run coverage xml"
            }

        }

        }
        stage('build && SonarQube analysis') {
            environment {
                scannerHome = tool 'SonarQubeScanner'
            }
            steps {
                withSonarQubeEnv('sonarqube') {
                    sh "echo $PATH & echo $JAVA_HOME"
                    sh "${scannerHome}/bin/sonar-scanner"
                }
            }
        }
        stage("Quality Gate") {
            steps {
                timeout(time: 10, unit: 'MINUTES') {
                    // Parameter indicates whether to set pipeline to UNSTABLE if Quality Gate fails
                    // true = set pipeline to UNSTABLE, false = don't
                    waitForQualityGate abortPipeline: true
                }
            }
        }
    }
    post{
        always{
            echo "build finished"
            junit 'reports/*.xml'
            sh "./tests/integration_utils/stop.sh ${INTEGRATION_TESTS_NETWORK} ${INTEGRATION_TESTS_CONTAINERS_PREFIX}"

        }

    }

}
