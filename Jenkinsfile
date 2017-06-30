#!/usr/bin/env groovy

podTemplate(
  cloud: 'woogikube',
  name: 'airconditioner-ci',
  label: 'airconditioner-ci',
  containers: [
    containerTemplate(name: 'airflovski', image: 'wooga-docker.jfrog.io/bit/airflow/base:0.1', ttyEnabled: true, command: 'cat')
  ],
  volumes: [
    secretVolume(secretName: 'pypirc', mountPath: '/home/jenkins')
  ]
){
  node('airconditioner-ci'){
    container('airflovski'){
      stage('Build'){
        checkout scm
        sh 'make install'
      }
      stage('Test'){
        sh 'make test'
      }
      if (env.BRANCH_NAME == 'production') {
        stage('Release'){
          sh 'make release'
        }
      }
    }
  }
}
