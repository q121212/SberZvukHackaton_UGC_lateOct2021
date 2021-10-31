### Using
1. clone repo
2. `docker-compose up`
3. One prefix handled only one time!
4. 
```python
## on PROD
endpoint = 'http://46.243.143.231:80/recognize'
resp = requests.post(endpoint, data={'source': 'http://hackaton.sber-zvuk.com/hackathon_part_1.mp4',
                                     'prefix': 'your_prefix'})
resp
```