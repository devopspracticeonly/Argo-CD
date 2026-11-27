# INC-003
Push this folder to GitHub. Set repoURL in argocd/application.yaml and apply it, then manually sync. Alternatively create the Application in the UI with path k8s.
Port forward: kubectl port-forward svc/frontend 9898:80 -n inventory-production
Run scripts/traffic.ps1 in another terminal for at least five minutes or longer. Import monitoring/dashboard.json and select inventory-production.
Prometheus must select ServiceMonitor, Probe and PrometheusRule resources in this namespace with release: monitoring. Existing infrastructure exporters are required.
Application source is mirrored in ConfigMaps for deployment without image builds. Do not inspect files before investigation if you want a blind lab. Cleanup removes the isolated namespace.
