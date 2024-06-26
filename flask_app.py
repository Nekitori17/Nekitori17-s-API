#Import Module
from flask import Flask, request, render_template, abort
import google.generativeai as genai
from datetime import datetime
import pytz
import json

#Set App
app = Flask(__name__)

#Host at / to render html web
@app.route('/')
def main():
    return render_template('index.html')

#Host at /api
@app.route("/api", methods=["POST"])

#Main Function
def index():
  #Get Data
  body = request.data.decode("UTF-8")
  data = json.loads(body)
  headers = request.headers
  rq_name = request.args.get("name")
  inputTimeZone = data.get("timezone")

  #Utilities
  if rq_name == "gemini-api":

    GEMINI_TOKEN = headers.get("Authorization")
    question = data.get("input")
    ai_model = data.get("model")

    #Config
    generation_config = {
      "temperature": 1,
      "top_p": 0.95,
      "top_k": 64,
      "max_output_tokens": 8192,
      "response_mime_type": "text/plain",
    }
    safety_settings = [
      {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
      },
      {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
      },
      {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
      },
      {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
      },
    ]

    #Check Data
    if not GEMINI_TOKEN:
      return "Error: GEMINI_TOKEN is missing"
    if not ai_model:
      return "Error: models is missing"
    if not question:
      return "Error: input is missing"
    try:
      genai.configure(api_key=GEMINI_TOKEN)
      model = genai.GenerativeModel(
        model_name=ai_model,
        safety_settings=safety_settings,
        generation_config=generation_config,
      )
      response = model.generate_content(question)
      return { "message": response.text, "timestamp": getTime(inputTimeZone)}
    except Exception as e:
      return f"『Error』: {e}"
  if rq_name == "banner-gen":
    input_data = [
      data.get("background"),
      data.get("text-1"),
      data.get("text-2"),
      data.get("text-3"),
      data.get("avatar")
    ]
    output_data = []
    result = None
    for i in range(len(input_data)):
      if input_data[i] is not None:
        output_data.append(input_data[i].strip().replace(" ", "+"))
      else:
        result = "Please check if the content is missing anything. (background, text-1, text-2, text-3, avatar)"
        break
    if result is None:
      result = f"https://api.popcat.xyz/welcomecard?background={output_data[0]}&text1={output_data[1]}&text2={output_data[2]}&text3={output_data[3]}&avatar={output_data[4]}"
    return { "url": result, "timestamp": getTime(inputTimeZone) }
  return abort(404)
#Optinal Function
def getTime(timezone):
  if timezone:
    try:
      timezone = pytz.timezone(timezone)
      current_time = datetime.now(timezone)
      return current_time.strftime('%a, %Y/%m/%d × %H:%M:%S. UTC%Z')
    except Exception as e:
      return f'『Error』: {e}'
  else:
    return datetime.now()