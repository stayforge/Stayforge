#!/bin/bash
kubectl apply -f k8s/
kubectl rollout status deployment/stayforge