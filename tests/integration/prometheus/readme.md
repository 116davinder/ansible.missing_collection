# Local Testing

```bash
docker run --rm -p 9090:9090 prom/prometheus \
--web.enable-lifecycle \
--config.file=/etc/prometheus/prometheus.yml \
--storage.tsdb.path=/prometheus \
--web.console.libraries=/usr/share/prometheus/console_libraries --web.console.templates=/usr/share/prometheus/consoles
```