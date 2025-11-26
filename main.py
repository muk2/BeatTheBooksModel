from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}



@app.get("/scrape")
async def scrape_data():

    


    return {"message": "Scraping data... (functionality not yet implemented)"}