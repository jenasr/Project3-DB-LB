# Project3-DB-LB
## Joseph Nasr
## Harrold Ventayen
## Samuel Valls
## Kevin Garcia


#### Databases:
1. Initialize database: execute create_stats_db.sh in the terminal
2. Create shards: execute create_shards.py in the terminal

#### Starting services:
##### Standalone:
1. uvicorn m1:app --reload
2. uvicorn m2:app --reload
3. uvicorn m3:app --reload

##### Using Traefik:
1. ./traefik --configFile=traefik.toml
2. foreman start -m 'word=1, game=1, stat=3'
