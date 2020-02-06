A set of scripts used to interact wth the SecurityTrails.com API in effort to find domains that once pointed to the Mormon Church's name servers but no longer do.

Edit the config.yaml.example to your needs and save it as config.yaml. Then run the following commands:

```
docker build -t securitytrails .
docker run -it --rm -v $(pwd):/root securitytrails get_domains.py
docker run -it --rm -v $(pwd):/root securitytrails parse_json.py
docker run -it --rm -v $(pwd):/root securitytrails check_ns_history.py
```

The news article reporting on this investigation can be read [here](https://truthandtransparency.org/news/2020/2/6/mormon-tied-public-holdings-near-35-billion-private-investments-in-pharma-and-tech-companies-discovered).
