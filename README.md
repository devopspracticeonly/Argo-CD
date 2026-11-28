# INC-006
Deploy k8s using Argo CD, destination order-production-006. Review prune before sync. Apply monitoring/ separately if kube-prometheus-stack is installed. Port-forward svc/frontend 9906:80 in order-production-006. Run scripts/traffic.ps1 in another PowerShell terminal. Import monitoring/dashboard.json. Application source is embedded in ConfigMaps; app/ contains matching source copies.
