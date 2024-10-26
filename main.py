from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI()

# Serve static files (like CSS, JS) from a "static" directory
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# Route to render the 'index.html' template
@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    # Pass the request object to the template (needed for Jinja2)
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/webhook")
async def webhook(request: Request):
    req = await request.json()

    # Check if 'queryResult' is in the request, if not return an error
    if 'queryResult' not in req:
        return JSONResponse(content={"fulfillmentText": "Error: Missing 'queryResult' in the request."})

    session_id = req.get("originalDetectIntentRequest", {}).get("payload", {}).get("sessionId", "")
    intent_name = req["queryResult"]["intent"]["displayName"]

    if intent_name == "share.tips":
        return await share_tips(req, session_id)
    elif intent_name == "get.resources":
        return await get_resources(req, session_id)
    else:
        return JSONResponse(content={"fulfillmentText": "Sorry, I didn't understand that."})

async def share_tips(req, session_id):
    user_query = req["queryResult"]["queryText"]  # Get user's query
    # Implement logic to choose a relevant tip based on user_query
    # For example, use a keyword-based approach or a more advanced NLP technique
    tip = "Here's a tip: " + choose_tip(user_query)
    return JSONResponse(content={"fulfillmentText": tip})

def choose_tip(user_query):
    # Simple keyword-based example:
    keywords = ["anxious", "sad", "stressed"]
    if any(keyword in user_query.lower() for keyword in keywords):
        return "Try practicing mindfulness or deep breathing exercises."
    else:
        return "You might find it helpful to set small, achievable goals."

async def get_resources(req, session_id):
    user_query = req["queryResult"]["queryText"]  # Get user's query
    # Implement logic to choose relevant resources based on user_query
    # For example, use a keyword-based approach or a more advanced NLP technique
    resources = choose_resources(user_query)
    resource_list = "\n".join(resources)
    return JSONResponse(content={"fulfillmentText": f"Here are some resources:\n{resource_list}"})

def choose_resources(user_query):
    # Simple keyword-based example:
    keywords = ["anxiety", "depression", "crisis"]
    if any(keyword in user_query.lower() for keyword in keywords):
        return ["National Alliance on Mental Illness (NAMI)", "Crisis Text Line"]
    else:
        return ["MentalHealth.gov", "Psychology Today"]