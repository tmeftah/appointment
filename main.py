from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
import uvicorn


app = FastAPI()


# Configure CORS to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Structure to store customer info: name and appointment status
customer_list: List[Dict[str, str | bool]] = []  # List of dictionaries


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/submit_name")
async def submit_name(
    name: str = Form(...), appointment: bool = Form(False)
):  # Add appointment boolean
    global customer_list
    name = "-" if name.strip() == "" else name.strip()
    customer = {
        "name": name,
        "appointment": appointment,
    }  # Create customer dict
    customer_list.append(customer)

    return JSONResponse(
        content={"message": f"Vielen Dank Herr/Frau. {name}!"}
    )  # Return the message as JSON


@app.get("/office", response_class=HTMLResponse)
async def office_view(request: Request):
    return templates.TemplateResponse(
        "office.html", {"request": request, "customers": customer_list}
    )


@app.delete("/customer/{name}")
async def delete_customer(name: str):
    global customer_list
    print(customer_list)
    print(name)
    # Find the customer dictionary by name
    for customer in customer_list:
        if customer["name"] == name:
            customer_list.remove(customer)
            return {"status": "deleted", "name": name}  # return the name
    raise HTTPException(status_code=404, detail="Customer not found")


@app.get("/customers")
async def get_customers():
    global customer_list

    return customer_list  # Returns the full  customers list as  JSON


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5006)
