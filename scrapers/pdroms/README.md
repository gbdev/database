# pdroms scraper

Created by [max-m](https://github.com/max-m) and [avivace](https://github.com/avivace)

```
npm install
node download.js
```

On the result:
-  `unzip.py` extracts and finds the game ROM. GB/GBC gets flagged here.
- `moveFiles.py` then hashes the files and adapts the json to the new schema.
- `improv.py` tries to find keywords in title to flag the demos (*intro* or *menu*)

### Issues

Those issues had to be fixed manually:

- *FGB, Binary Chaos, Pazeek, Jumping Jack, Run!!, Espionage* had nested folders and/or zipfiles, so the ROM file had to be found and moved manually
- Duplicates: 
