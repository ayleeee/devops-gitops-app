pipeline {
  agent any

  parameters {
    string(name: 'IMAGE_TAG', defaultValue: '0.1.0', description: 'Image tag to build and deploy')
    string(name: 'REGISTRY_ENDPOINT', defaultValue: 'localhost:30500', description: 'Internal registry endpoint')
  }

  environment {
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
            -t ${REGISTRY_ENDPOINT}/${IMAGE_NAME}:${IMAGE_TAG} .
        '''
      }
    }

    stage('Push Image') {
      steps {
        sh 'docker push ${REGISTRY_ENDPOINT}/${IMAGE_NAME}:${IMAGE_TAG}'
      }
    }
  }
}
