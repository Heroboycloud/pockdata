from bottle import route,run,request,response,template
from faker import Faker
from faker.providers import internet
import json
import bottle
from requests import get,post

fake= Faker()


@route("/")
def home():
  return "<h1> This is a random data generator i built for fun...</h1><p>Apis include /user?list=[any no]</p>"

@route("/user")
def get_user():
  fake.add_provider(internet)
  user_data=[]
  user_list= request.query.list or 1
  for _ in range(int(user_list)):
      user = {
           'Name': fake.name(),
           'Email': fake.free_email(),
           'Phone Number': fake.phone_number(),
           'Birthdate': fake.date_of_birth().ctime(),
           'Address': fake.address(),
           'City': fake.city(),
           'Country': fake.country(),
           'ZIP Code': fake.zipcode(),
           'Job Title': fake.job(),
           'Company': fake.company(),
           'IP Address': fake.ipv4_private(),
           'Credit Card Number': fake.credit_card_number(),
           'Username': fake.user_name(),
           'Password': fake.password(),
#           'Profile': fake.profile(),
           'Website': fake.url(),
           'SSN': fake.ssn(),
           'User-Agent': fake.user_agent(),
       }
      user_data.append(user)
  response.set_header("content_type","application/json")
  return json.dumps(user_data)



@route("/user-agent")
def useragent():
  return fake.user_agent()

@route("/sentence/<val:int>")
def sentence(val=10):
  return fake.sentence(val)



@route("/advice")
def insult_api():
  try:
   url= "https://api.adviceslip.com/advice"
   r= get(url).json()
   return r["slip"]["advice"]
  except:
   return "Error retrieving contents,Will get back later"

@route("/insult")
def insult_api():
  try:
   url= "https://evilinsult.com/generate_insult.php?lang=en&type=json"
   r= get(url).json()
   return r
  except:
   return "Error retrieving contents,Will get back later"


@route("/dad_joke")
def getdad_joke():
  url= "https://icanhazdadjoke.com/"
  headers= {"Accept":"application/json","User-Agent":"Pockdata services"}
  try:
    r=get(url,headers=headers).json()
    return r
  except:
    return "Dad has no jokes now"


@route("/joke")
def get_joke():
  url= "https://v2.jokeapi.dev/joke/{}?blacklistFlags={}&format={}"
  if request.query.category:
     cat= request.query.category or "Programming"
     flags= request.query.flags or "racist"
     format= request.query.format or "json"
     if request.query.format == "text":
        r= get(url.format(cat,flags,format)).text
     else:
        r= get(url.format(cat,flags,format)).json()
  else:
     url= "https://v2.jokeapi.dev/joke/Programming?format=txt"
     r= get(url).text
  return r




#run(reloader=True,port=3000)
if __name__ == "__main__":
    run(port=8080)

app = bottle.default_app()
