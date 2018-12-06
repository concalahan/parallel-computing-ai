# parallel-computing-ai
The assignment using K-means to detect whether the new comment/ new text/ new article is talked about Samsung or not. This project was run on Spark platform, using MLLib and Spark.

The article data was crawl from trustedreviews.com

## How to run
### Step 1: run the scrapy to get all url
cd in the spider directory

```
cd rust
```

```
scrapy crawl rust
```

### Step 2: parse it to HTML

```
cd parse
```

```
python3 parser_raw.py
```

### Step 3: filter to JSON

```
cd filter
```

```
python3 filter_main.py
```

### Step 4: run the k means application and input some text
```
cd filter
```

```
python k_means_with_spark.py
```
