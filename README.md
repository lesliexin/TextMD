# TextMD


2. clone the [repository](https://bitbucket.org/livebungalow/bungalow-website/overview)
3. from the root project directory, launch the app

`docker-compose up`

4. in a new terminal window (still in the root project directory), migrate the database:

`docker-compose exec pineapple ./manage.py migrate`

5. populate the database with the latest data from salesforce:

`docker-compose exec pineapple ./manage.py sf_sync_all`

6. (optional) sync images for properties (this could take 20-30 minutes...get a coffee):

`docker-compose exec pineapple ./manage.py box_sync_all`

7. Navigate to `http://localhost:8080` for web access and `http://localhost:8000` for api access

8. Run api tests. The `-- -s` passed `-s` in to pytest to show print statement output, not required

`docker-compose exec pineapple ./manage.py test -- -s`

# TIPS

- To allow for PDB inside of docker containers:

`docker ps` to get list of running containers `docker attach [name of container e.g bungalow_pineappple_1]`

During an attach `ctrl-c` will stop the underlying container, you can use `ctrl-p ctrl-q` to detach instead.

- to reset your local postgres database (IMPORTANT - Ensure you are connected to your local db instance before running this command)

`docker-compose run pineapple ./manage.py rese
