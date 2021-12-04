# URL Shortener Web App / API using Python, FastAPI, and MongoDB

A simple FastAPI app that shortens a URL and redirects browser to the original URL.

**Demo available at https://ay-us.herokuapp.com/**

## Requirements

Developed and tested with:

- Windows 11
    - Should work with other versions of Windows and Linux
- Firefox 94
- Python 3.9
- Miniconda3
- Python packages listed in [requirements.txt](requirements.txt)

## How to Run

1. Create a file named `app.env` and insert the environment variables below:
    ```shell
    BASE_URL=http://127.0.0.1:8000
    MONGODB_URI=mongodb+srv://user:<password>@cluster0.abc.mongodb.net/url-shortener?retryWrites=true&w=majority
    MONGODB_URI_TESTS=mongodb+srv://user:<password>@cluster0.abc.mongodb.net/url-shortener-tests?retryWrites=true&w=majority
    RNG_LENGTH=5
    ```
    - `BASE_URL` is the domain name of your server
        - The default is `http://127.0.0.1:8000` if running locally
    - `MONGODB_URI` is your connection string to MongoDB for real database. Get this from your MongoDB dashboard
    - `MONGODB_URI_TESTS` is your connection string to MongoDB for test database. Get this from your MongoDB dashboard
    - `RNG_LENGTH` is the number of characters the short URL has
    - To actually set these variables, make your IDE automatically export them via a `.env` file
      (PyCharm has a plugin for this), _or_ export them manually
2. Activate virtual environment and execute `uvicorn app.main:app`
    1. Add `--reload` to make the server restart after code changes [**Only use for development**]
3. Open your `BASE_URL` in a browser to view the home page

## How to Run Tests

1. Execute `pytest` in terminal

## List of API

### [1] POST: /api/shorten

**Input**

Request body:

```json
{
  "url": "string",
  "custom_name": "string"
}
```

Example request body:

```json
{
  "url": "https://duckduckgo.com",
  "custom_name": "ddg"
}
```

**Output**

Response:

```json
{
  "url": "string",
  "short_url": "string"
}
```

Example response:

```json
{
  "url": "https://duckduckgo.com",
  "short_url": "https://me.com/ddg"
}
```

## Future Improvements / Features

1. ~~Check the original URL if it's already in database, and return the existing short URL instead of creating a new one~~
    1. Will reduce duplicate entries
    2. Added in [commit 2c7ff7c](https://github.com/adibyhy/url-shortener-fastapi/commit/2c7ff7ce60377247c4ad0ffae4176dedac63131a)
2. Remove unvisited link after a certain length of time has elapsed
    1. Will reduce size of database
    2. Less hoarding of custom names
3. Use Docker to containerize this app
    1. Easier to deploy
4. A page to show statistics
    1. Top 10 URLs, etc
5. Prettier home page
    1. Mobile version too

## References & Credits

1. [Blog post](https://simiokunowo.hashnode.dev/build-a-url-shortener-with-fastapi-mongodb-and-python) by Similoluwa
   Okunowo
    1. The main inspiration for this project. I reused many of their codes and added my own flavor where I see fit
2. [FastAPI documentation](https://fastapi.tiangolo.com/)
