# jarvis_project
**PoC**: extendible api.ai chatbot with microservice support

I've been watching too much __Iron Man__, lately so I decided to create a proof of concept of Jarvis with API.AI.

These are the requirements (in my head):

1. it should be **extensible**
2. its extensibility should **not require to kill-revive jarvis**
3. it should be able to **interact with IoT in my house** (or hypotetical IoT in my house)

so i wrote this awfull but simple python code.


### Details

On my machine run jarvis.py script, which is responsible to invoke API.AI and some scripts running on raspberry pi (this is how it'll interact with local IoT).

I defined a chatbot on API.AI (see the jarvis_api.ai/ folder)with a simple Welcome Intent, which is called at startup) and a fallback Intent.

When a user enter a query on che CLI, jarvis sends it to API.AI (i call this an Interaction). At this point an **Interaction** and its result could be:

1. another api.ai **query**
2. an **event**: which is an alphabetical constants in the form of 'gnrl-event-' 
3. an "**action**": which is an alphabetical constants in the form of 'gnrl-action-' 

When an event is received, it's invoked via API.AI. When an action is received a Provider for that action is searched. The search is performed on data stored on config/config.json where is specified which microservice will provide answer for a particular action

### Example

This is how it works, considering a very stupid and simple example. Jarvis is started so a Interaction of type event is created with information to call "welcome" event (that only says "hi!" to user, nothing special).

When the user type the query "open the door", for interact with wifi-connected door lock, the query is sent to API.AI. 

This return another query that asks the user for the password. User types "the password is password" (easy to remember) and this query is sent as well to API.AI that return an action: **gnrl-action-open-door**.

When this action is received, jarvis discovers that the provider for this action is at http://192.168.1.8:5000/providers/door_opener (flask python script running locally in my raspberry pi).

A POST operation is sent at that url, passing the API.AI context that contains the parameters. The password is verified and the door is opened (if password is matched) or the user is prompted for "wrong password".

### How to exdend jarvis

1. create an intent for your interaction
2. if you need jarvis to handle an action, you have to add it to config/config.json file and to create the microservice (keep the result syntax)
 