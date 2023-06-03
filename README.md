```bash
docker run \
  --name picbed \
  --restart always \
  -v /path/to/image:/image \
  -p 5000:5000 \
  picbed
```