# Incident 001 — Payment API
Practice only. Requires existing Argo CD and Prometheus Operator CRDs. No custom image build.

1. Push repository to GitHub. Set repoURL in argocd/application.yaml, then kubectl apply -f argocd/application.yaml. Sync manually in Argo CD. Alternatively kubectl apply -f k8s/.
2. Run kubectl get pods -n crashloop-demo -w. Allow several minutes for restart backoff.
3. In a separate terminal run kubectl port-forward svc/payment-gateway 9696:80 -n crashloop-demo. Run scripts/traffic.ps1 in PowerShell.
4. In Grafana select namespace crashloop-demo, pod All, last 15 minutes. Observe restarts, waiting reasons, readiness, unavailable replicas and HTTP metrics. ServiceMonitor requires Prometheus to select release=monitoring and this namespace. Check Prometheus targets if absent.
5. Share initial pod output with instructor before inspecting manifests or logs if you want a blind exercise.
6. Cleanup after exercise: delete the Argo CD application with cascading deletion, then kubectl delete namespace crashloop-demo (only this lab).

Gateway health checks are included in HTTP counters. The exporter is a lightweight lab implementation, not production log rotation or durable counters. Blackbox probes, HPA and PVC are not included. No live cluster validation performed.
