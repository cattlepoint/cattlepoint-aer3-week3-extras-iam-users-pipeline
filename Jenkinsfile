pipeline {
    agent any
    environment {
        STACK_NAME       = 'ECRListCreateUser'
        TEMPLATE_FILE    = 'create-ecr-user.yaml'
        EKS_STACK_NAME   = 'EksDeployUser'
        EKS_TEMPLATE_FILE= 'create-eks-user.yaml'
        AWS_REGION       = 'us-east-1'
        AWS_CREDENTIALS  = 'aws-jenkins-creds'
    }
    stages {
        stage('Deploy CloudFormation Stack') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: env.AWS_CREDENTIALS,
                    accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                    secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
                ]]) {
                    sh '''
                        aws cloudformation deploy \
                            --stack-name "$STACK_NAME" \
                            --template-file "$TEMPLATE_FILE" \
                            --region "$AWS_REGION" \
                            --capabilities CAPABILITY_NAMED_IAM
                    '''
                }
            }
        }

        stage('Fetch Access Keys') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: env.AWS_CREDENTIALS,
                    accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                    secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
                ]]) {
                    script {
                        def accessKeyId = sh(
                            script: "aws cloudformation describe-stacks --stack-name ${env.STACK_NAME} --region ${env.AWS_REGION} --query \"Stacks[0].Outputs[?OutputKey=='AccessKeyId'].OutputValue\" --output text",
                            returnStdout: true
                        ).trim()
                        def secretAccessKey = sh(
                            script: "aws cloudformation describe-stacks --stack-name ${env.STACK_NAME} --region ${env.AWS_REGION} --query \"Stacks[0].Outputs[?OutputKey=='SecretAccessKey'].OutputValue\" --output text",
                            returnStdout: true
                        ).trim()
                        echo "AccessKeyId: ${accessKeyId}"
                        echo "SecretAccessKey: ${secretAccessKey}"
                    }
                }
            }
        }

        stage('Deploy EKS User') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: env.AWS_CREDENTIALS,
                    accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                    secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
                ]]) {
                    sh '''
                        aws cloudformation deploy \
                            --stack-name "$EKS_STACK_NAME" \
                            --template-file "$EKS_TEMPLATE_FILE" \
                            --region "$AWS_REGION" \
                            --capabilities CAPABILITY_NAMED_IAM
                    '''
                }
            }
        }

        stage('Fetch EKS Access Keys') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: env.AWS_CREDENTIALS,
                    accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                    secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
                ]]) {
                    script {
                        def eksAccessKeyId = sh(
                            script: "aws cloudformation describe-stacks --stack-name ${env.EKS_STACK_NAME} --region ${env.AWS_REGION} --query \"Stacks[0].Outputs[?OutputKey=='AccessKeyId'].OutputValue\" --output text",
                            returnStdout: true
                        ).trim()
                        def eksSecretAccessKey = sh(
                            script: "aws cloudformation describe-stacks --stack-name ${env.EKS_STACK_NAME} --region ${env.AWS_REGION} --query \"Stacks[0].Outputs[?OutputKey=='SecretAccessKey'].OutputValue\" --output text",
                            returnStdout: true
                        ).trim()
                        echo "EKS AccessKeyId: ${eksAccessKeyId}"
                        echo "EKS SecretAccessKey: ${eksSecretAccessKey}"
                    }
                }
            }
        }
    }
}
