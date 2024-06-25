## render setup

## render host and images
the folder "media" should always be added to gitignore
follow the documentation here

https://docs.render.com/deploy-django

the section of manual deplay NOT with render.yamal

https://docs.render.com/deploy-django#manual-deployment

  -Create a new PostgreSQL database on Render. Copy its internal database URL for now—you’ll need it later.

  -Select Python for the runtime and set the following properties (replace mysite with your project’s name):
    Property =   Value
    Build Command =    ./build.sh
    Start Command =    python -m gunicorn mysite.asgi:application -k uvicorn.workers.UvicornWorker

    Add the following environment variables under Advanced:
    Key =	Value
    DATABASE_URL = The postgres internal database URL for the database you created above
    SECRET_KEY = Click Generate to get a secure random value
    WEB_CONCURRENCY = 4

 
 if you want to upload images to render via github:
  - 1- add all images you want to "media_source" folder
  - 2- push your images
  - 3- go to render shell and run the command python manage.py import_images <imagesDirInside_media_source>
