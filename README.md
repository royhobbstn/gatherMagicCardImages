# gatherMagicCardImages
Get Magic Card images from Scryfall.

Previous to running for the first time, download the bulk data from Scryfall:

```
wget https://archive.scryfall.com/json/scryfall-default-cards.json
```

Other Bulk Options (not suported currently)

https://scryfall.com/docs/api/bulk-data


To load all images (will load into a separate folder for each set):
```
node index.js
```

To load only one set:
```
node index.js setname
```

(see https://scryfall.com/sets and note the grey text; that is the setname)


