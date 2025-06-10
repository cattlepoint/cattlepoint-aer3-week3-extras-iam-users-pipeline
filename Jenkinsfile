pipeline {
    agent any
    environment {
        STACK_NAME = 'ECRListCreateUser'
        TEMPLATE_FILE = 'create-ecr-user.yaml'
        AWS_REGION = 'us-east-1'
        AWS_CREDENTIALS = 'aws-jenkins-creds'
    }
    stages {
        stage('Deploy CloudFormation Stack') {
            steps {
                withAWS(region: env.AWS_REGION, credentials: env.AWS_CREDENTIALS) {
                    cfnCreateOrUpdate(stack: env.STACK_NAME,
                                      file: env.TEMPLATE_FILE,
                                      pollInterval: 1000,
                                      pollTimeout: 900000,
                                      capabilities: ['CAPABILITY_NAMED_IAM'])
                }
            }
        }
        stage('Fetch Access Keys') {
            steps {
                withAWS(region: env.AWS_REGION, credentials: env.AWS_CREDENTIALS) {
                    script {
                        def outputs = cfnDescribe(stack: env.STACK_NAME).stackOutputs
                        echo "AccessKeyId: ${outputs['AccessKeyId']}"
                        echo "SecretAccessKey: ${outputs['SecretAccessKey']}"
                    }
                }
            }
        }
    }
}
