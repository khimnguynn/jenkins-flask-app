pipeline {
    agent any
    
    stages {
        
        stage('delete old source') {
            steps {
                sh 'rm -rf *'
            }
        }
        
        stage('docker login') {
            steps {
                withCredentials([string(credentialsId: 'password docker', variable: 'dockerpwd')]) {
                    sh 'docker login -u khimnguynn -p ${dockerpwd}'
                }
            }
        }
        
        stage('Git Clone') {
            steps {
                git branch: 'main', credentialsId: '76368a06-b300-4b62-aa09-8fef307ddcd7', url: 'https://github.com/khimnguynn/jenkins-flask-app.git'
            }
        }
        
        stage('docker build') {
            steps {
                
                sh """cat << EOF> Dockerfile
            FROM python:3.7-slim
            ADD . .
            RUN pip3 install flask
            ENTRYPOINT ["python3", "main.py"]"""
                sh 'docker build -t khimnguynn/flask-app:${BUILD_NUMBER} .'

            }
        }
        stage('docker push images') {
            steps {
                sh 'docker push khimnguynn/flask-app:${BUILD_NUMBER}'
                
            }
        }
        stage('deploy server') {
            steps {
                script {
                    remove_container = 'docker rmi --force $(docker images --quiet --filter=reference="khimnguynn/flask-app")'
                }
                sshagent(['9927e8a2-cb26-4d8c-a1d9-1c400a670b79']) {
                    
                    sh """ssh -o StrictHostKeyChecking=no -l root 10.168.112.64 '
                    docker ps -f name=flask-app -q | xargs --no-run-if-empty docker container stop
                    docker container ls -a -fname=flask-app -q | xargs -r docker container rm
                    ${remove_container}
                    docker run --name flask-app -d -p 2222:2222 khimnguynn/flask-app:${BUILD_NUMBER}'"""
                    sh 'docker rmi --force $(docker images --quiet --filter=reference="khimnguynn/flask-app")'
                }
            }
        }
    }
}


