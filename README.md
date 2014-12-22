=================
Command Line News
=================

A command line rss news feed reader.

### Version
0.1.0

### Installation


### Configuration
All you need to do is to add your RSS urls into the ```config.py``` under the ```CHANNELS``` dictionary as following:

```
"nbc": {
    "name": "NBC",
    "url": "http://feeds.nbcnews.com/feeds/topstories"
}
```
### Usage
```python clnews.py```

##### Options
```.help```: show the help message and exit

```.list```: lists all the available channels

```.get```: retrieves the news of a given channel, e.g.: .get cnn

### License
MIT

