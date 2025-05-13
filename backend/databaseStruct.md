users (koleksiyon)
 └── {proID} (döküman)
     ├── nick
     └── password

singers (koleksiyon)
 └── {sid} (döküman)
     ├── name
     ├── avgRateSinger
     └── genres: [rock, pop, jazz] ← (array)

albums (koleksiyon)
 └── {albumID} (döküman)
     ├── sid (referans veya ID)
     ├── name
     ├── year
     └── genre
    └── avgRateAlbum

songs (koleksiyon)
 └── {songID} (döküman)
     ├── albumID (referans veya ID)
     ├── name
     └── avgRateSong (ortalama puan, cache)

logs (koleksiyon)
 └── {logID} (döküman)
     ├── songID
     ├── proID
     └── rate
     