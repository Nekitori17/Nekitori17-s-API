#Import Module
from flask import Flask, request, render_template, abort
import google.generativeai as genai
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
  
  #Extended Utilities
  if rq_name == "gemini-api":
  	GEMINI_TOKEN = headers.get("Authorization")
  	question = data.get("input")
  	ai_model = data.get("model")
  	genai.configure(api_key=GEMINI_TOKEN)
  	model = genai.GenerativeModel(ai_model)
  	response = model.generate_content(question)
  	return response.text
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
    return result
  return abort(404)
#Optimal Function