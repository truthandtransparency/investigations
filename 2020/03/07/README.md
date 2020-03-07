A set of scripts used to interact wth the JiveData.com API to gather and compare all public holdings in the U.S. stock market tied to the Mormon Church.

Edit the config.yaml.example to your needs and save it as config.yaml. Then run the following commands:

```
docker build -t sec-filings .
docker run -it --rm -v $(pwd):/root sec-filingss get_filings.py
docker run -it --rm -v $(pwd):/root sec-filings compare_holdings.py
```

The news article reporting on this investigation can be read [here](https://truthandtransparency.org/news/2020/3/7/mormon-church-moves-public-stock-holdings-to-single-entity).
