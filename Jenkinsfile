pipeline {
  agent any

  parameters {
    string(name: 'IMAGE_TAG', defaultValue: '0.1.0', description: 'Image tag to build and deploy')
  }

  environment {
    REGISTRY = '172.31.9.119:30500'
    IMAGE_NAME = 'devops-gitops-app'
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build Image') {
      steps {
        sh '''
          docker build \
            --build-arg APP_VERSION=${IMAGE_TAG} \
            -t ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG} .
        '''
      }
    }

    stage('Push Image') {
      steps {
        sh 'docker push ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}'
      }
    }
  }
}
