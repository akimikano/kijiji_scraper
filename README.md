# Kijiji website scraping

Small project scraping apartments from [website](https://www.kijiji.ca/b-apartments-condos/city-of-toronto/c37l1700273) and saving in DB

## Launching

Use docker-compose command to launch project

```bash
docker-compose up --build
```

If error occured try to restart container "app"
```bash
docker restart app
```

If everything is ok you will see according logs in every step 

## Libraries

Used libraries:
1. Selenium for scraping
2. Sqlalchemy for db queries
