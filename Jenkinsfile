pipeline {
  agent {
    kubernetes {
      defaultContainer 'docker'
      yaml '''
apiVersion: v1
kind: Pod
spec:
  containers:
    - name: docker
      image: docker:git
      command:
        - cat
      tty: true
      securityContext:
        runAsUser: 0
      volumeMounts:
        - name: docker-sock
          mountPath: /var/run/docker.sock
  volumes:
    - name: docker-sock
      hostPath:
        path: /var/run/docker.sock
        type: Socket
'''
    }
  }

  options {
    disableConcurrentBuilds()
    buildDiscarder(logRotator(numToKeepStr: '10'))
    timeout(time: 20, unit: 'MINUTES')
  }

  parameters {
    string(name: 'IMAGE_TAG', defaultValue: '0.1.0', description: 'Image tag to build and deploy')
    string(name: 'REGISTRY_ENDPOINT', defaultValue: 'localhost:30500', description: 'Internal registry endpoint')
    string(name: 'GITOPS_REPO_URL', defaultValue: '', description: 'GitOps manifests repository URL')
    string(name: 'GITOPS_BRANCH', defaultValue: 'main', description: 'GitOps manifests branch')
    string(name: 'GITOPS_CREDENTIALS_ID', defaultValue: 'github-token', description: 'Jenkins credentials ID for GitOps repository')
  }

  environment {
    IMAGE_NAME = 'devops-gitops-app'
    GITOPS_DIR = 'gitops-manifests'
    VALUES_FILE = 'apps/devops-app/values.yaml'
    GIT_AUTHOR_NAME = 'jenkins'
    GIT_AUTHOR_EMAIL = 'jenkins@example.local'
    GIT_COMMITTER_NAME = 'jenkins'
    GIT_COMMITTER_EMAIL = 'jenkins@example.local'
  }

  stages {
    stage('Validate Parameters') {
      steps {
        script {
          if (!params.IMAGE_TAG?.trim()) {
            error('IMAGE_TAG is required.')
          }

          if (!params.GITOPS_REPO_URL?.trim()) {
            error('GITOPS_REPO_URL is required.')
          }
        }

        sh '''
          set -eu
          case "${REGISTRY_ENDPOINT}" in
            *://*) echo "REGISTRY_ENDPOINT must not include scheme."; exit 1 ;;
          esac

          echo "Image: ${REGISTRY_ENDPOINT}/${IMAGE_NAME}:${IMAGE_TAG}"
          echo "GitOps repo: ${GITOPS_REPO_URL}"
          echo "GitOps branch: ${GITOPS_BRANCH}"
        '''
      }
    }

    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build Image') {
      steps {
        sh '''
          set -eu
          docker build \
            --build-arg APP_VERSION=${IMAGE_TAG} \
            -t ${REGISTRY_ENDPOINT}/${IMAGE_NAME}:${IMAGE_TAG} .
        '''
      }
    }

    stage('Push Image') {
      steps {
        sh '''
          set -eu
          docker push ${REGISTRY_ENDPOINT}/${IMAGE_NAME}:${IMAGE_TAG}
        '''
      }
    }

    stage('Update GitOps Values') {
      steps {
        dir(env.GITOPS_DIR) {
          git branch: params.GITOPS_BRANCH, credentialsId: params.GITOPS_CREDENTIALS_ID, url: params.GITOPS_REPO_URL
        }

        sh '''
          set -eu
          cd ${GITOPS_DIR}

          awk -v repo="${REGISTRY_ENDPOINT}/${IMAGE_NAME}" -v tag="${IMAGE_TAG}" '
            /^image:/ { in_image=1; print; next }
            in_image && /^  repository:/ { print "  repository: " repo; next }
            in_image && /^  tag:/ { print "  tag: \\"" tag "\\""; next }
            in_image && /^[^ ]/ { in_image=0 }
            { print }
          ' ${VALUES_FILE} > ${VALUES_FILE}.tmp
          mv ${VALUES_FILE}.tmp ${VALUES_FILE}

          echo "Updated ${VALUES_FILE}:"
          grep -A 3 '^image:' ${VALUES_FILE}
        '''
      }
    }

    stage('Commit and Push GitOps Change') {
      steps {
        withCredentials([gitUsernamePassword(credentialsId: params.GITOPS_CREDENTIALS_ID, gitToolName: 'Default')]) {
          sh '''
            set -eu
            cd ${GITOPS_DIR}

            git config --global --add safe.directory "$(pwd)"
            git status --short

            if git diff --quiet -- ${VALUES_FILE}; then
              echo "No GitOps change detected. Skipping commit."
              exit 0
            fi

            git add ${VALUES_FILE}
            git commit -m "Deploy ${IMAGE_NAME}:${IMAGE_TAG}"

            git push origin HEAD:${GITOPS_BRANCH}
          '''
        }
      }
    }
  }

  post {
    success {
      echo "Image pushed and GitOps repository updated: ${REGISTRY_ENDPOINT}/${IMAGE_NAME}:${IMAGE_TAG}"
    }
    failure {
      echo 'Pipeline failed. Check the failed stage logs for details.'
    }
  }
}
