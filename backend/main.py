from fastapi import FastAPI
app=FastAPI()

@app.get("/")
def read_root():
    return {"message":"hello world"}

@app.get("/items/{item_id}")
def read_items(item_id:int):
    return {"item_id":item_id}

@app.get("/getnumber")
def get_number():
    return {"message": "+91 6005231146"}
