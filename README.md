# Production incident INC-004

Deploy the k8s directory through Argo CD. Use namespace checkout-production and manual sync. If reusing an existing Application, review prune candidates before syncing and ensure the destination is permitted. Existing Prometheus Operator CRDs and discovery of release: monitoring are required.

Run `kubectl port-forward svc/frontend 9899:80 -n checkout-production` then run scripts/traffic.ps1 in a separate PowerShell terminal. Import monitoring/dashboard.json and select checkout-production. Allow several minutes for metrics and alerts. The app source is mirrored in the deployed ConfigMaps; edits to app/ alone do not deploy. No custom image build is needed.

For cleanup delete the Argo CD Application with cascading deletion if dedicated to this lab, or remove only this lab's resources from Git and prune after reviewing the deletion list.
