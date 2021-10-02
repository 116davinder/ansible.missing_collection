# how to start docker registry locally

```bash
docker run --rm -p 5000:5000 --name registry \
-e REGISTRY_STORAGE_DELETE_ENABLED=true \
-v /tmp/data:/var/lib/registry:Z registry:2
```