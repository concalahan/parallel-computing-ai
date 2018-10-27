# parallel-computing-ai
The assignment using K-means to detect what products (cellphones) were mentioned in some article.

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