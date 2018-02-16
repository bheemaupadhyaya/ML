from flask import Flask
from flask import request
from translator.translator import Translator
import spacy
from flask import render_template
import sys
import feedparser
import requests
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import datetime as date
import base64
import hashlib as hasher
import json

## for chat bot

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
# Create a new chat bot named Charlie
chatbot = ChatBot('VWR2',
                  logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch'
        },
        {
            'import_path': 'chatterbot.logic.LowConfidenceAdapter',
            'threshold': 0.65,
            'default_response': 'I am sorry, but I can not be of help or I do not understand your query.'
        }
    ],)
chatbot.set_trainer(ListTrainer)

       
conversation = [
    'Hi',
    'Hi from VWR',
    'How are you',
    'I am good, how are you',
    'me too',
    'Thats awesome, how may I help you?',
    'Need help',
    'Sure, how can I help you?',    
    'Tell me about VWR',
    'VWR is major scientific equipment supplier',    
    'Where is head office of VWR',
    'VWR head office is at Radnor, USA',    
    'What are shift timings for Coimbatore',
    'Contact HR. I am not sure',    
    'Do we have day time savings',
    'No we dont have',    
    'How to get more info about VWR',
    'Visit https://intranet.vwr.com',
    'Great, thanks for helping me',
    'My pleasure. Have great day',
    'Do you have any other question',
    'Nope',
    'Okay, I sign-off now',
    
        ]
        
        



chatbot.train([
    "I have issue in in my PC",
    "You may contact our helpdesk.",
])
chatbot.train([
    "I have issue in in my Lotus Notes",
    "You may contact Bheema",
])

chatbot.train(conversation)

#chatbot.set_trainer(ChatterBotCorpusTrainer)
#chatbot.train("chatterbot.corpus.english.greetings", "chatterbot.corpus.english.conversations")

## end for chat bot

# Load English tokenizer, tagger, parser, NER and word vectors
nlp = spacy.load('en_core_web_sm')

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    print ("Login from :"+request.remote_addr)
    return """ <HTML><Title> AI @ VWR</Title><Body></Body> <H1><b>Welcome to AI/ML Portal at AI@VWR.</b></H1> <br><br>
    <br><br> <b>Everything what we do here is prediction ! The better the training, the better is prediction....</b>
    <br><br>Day 1 : Hello VWR - Installed Python, Installed Flask. Created this portal. That was easy work !
    <br><br>Day 2 : Created first ML program. Flower distribution model. Learning !
    <br><br> Day 3 : Installed tensorflow, space, NLTK. Just installation and testing of packages
    <br><br> Day 4 : First <a href=/ChatBot>ChatBot attempt </a> by importing ChatBot package. Its live, try to ask bot about VWR.
    <br><br> Day 5 : Improvements in chat bot plus learning. Working Chat Bot, added more VWR related training.
    <br><br> Day 6 : First implementation <a href=/Translation> Simple Machine Translation</a> via <b>Google</b> Translation.
    <br><br> Day 7 : Implementing  Machine Translation via OpenSource Google Tensorflow. Its too complex and still under development by Google. So having challenges...
    <br><br> Day 8 : Implementing Machine Translationvia another opensource NMT (neural machine translation) called OpenNMT. Unfortunately its developed for Ilnux based systems, trying with windows by using GitHUB.
    <br><br> 17-Jan-2018 : Improved : Added simple sentiment analysis to  <a href=/ChatBot>ChatBot</a> Its live, try to ask bot about VWR.Now it knows your sentiment ;)
    <br><br> 02-Feb-2018 : A simple demo for VWR. The technology behind cryptocurrencies like BitCoin. You can <a href=/txion> transcat here</a>. Once done your transaction can not broken and removed. You may check public blockchain  data <a href=/blocks>here</a>. Someone must <a href=/mine> mine</a> before transactions get into secured <a href=/blocks>blocks</a>
    </HTML>"""



@app.route('/ChatBot', methods=['GET','POST'])

def VWRchatbot():
    if request.method == 'GET':
        htmltext=  """<html><title>AI@VWR</title><body>
<H1><b>Welcome to AI/ML  Test Bot using AI@VWR.</b></H1><br><br>
Any query related to VWR. <input type=text id="query">

<button type="button" onclick="loadDoc(document.getElementById(\'query\').value)">Ask VWR Bot !</button> 
<button type="button" onclick="history.back()">Home</button>
<p id="demo">.</p>
<script>
function loadDoc(myquery) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("demo").innerHTML = "You :<font color=blue>" +myquery+"</font><br> VWR Bot:<font color=green>"+ this.responseText+"</font><br>"+document.getElementById("demo").innerHTML;
      document.getElementById("query").value="";
    }
  };
  //alert (myquery);
      
    
  xhttp.open("POST", "/ChatBot", true);
  xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhttp.send("query="+myquery);
}
</script>
<script>
//loadDoc('Hi');
</script>
</body></html>"""
        return htmltext
    elif request.method == 'POST':
        # -*- coding: utf-8 -*-
                       
        #conversation.append(myquery)        
        #chatbot.train(conversation)
        #print (conversation)
        

        # Get a response to the input text 'How are you?'
        
        
        myquery= (request.form['query'])
        myresponse = chatbot.get_response(myquery)
        #myconv=myconv.append(myquery)
        #chatbot.train(myconv)
        
        senti=''
        sid = SentimentIntensityAnalyzer()
        ss = sid.polarity_scores(myquery)
        #senti=senti+'{0}: {1}, '.format(k, ss[k])
        print (ss['compound'])
        if ss['compound']>=0.75:
            senti='Your sentiment :Highly positive :'+str(ss['compound'])
        elif ss['compound']>=0.5:
            senti='Your sentiment :Positive :'+str(ss['compound'])
        elif ss['compound']>=0.25:
            senti='Your sentiment :Neutral :'+str(ss['compound'])
        elif ss['compound']<=-0.50:
            senti='Your sentiment :Too negative :'+str(ss['compound'])
        elif ss['compound']<=-0.25:
            senti='Your sentiment :Negative :'+str(ss['compound'])
        elif ss['compound']<0.0:
            senti='Your sentiment :Slighly negative :'+str(ss['compound'])
       
        
        
            
                
        return (myresponse.text+'<br>'+senti)
       # return "<html><title>AI@VWR - response </title>"+response+"</html>"

@app.route('/Translation', methods=['GET', 'POST'])
def translate():
  
    if request.method == 'GET':
        htmltext=  """<html><title>AI@VWR</title><body>
<H1><b>Welcome to AI/ML  Test English to German Translate Bot using Google.</b></H1><br><br>
Your English text here : <input type=text id="query">

<button type="button" onclick="loadDoc('de')">German Bot!</button>
<button type="button" onclick="loadDoc('fr')">French Bot!</button>
<button type="button" onclick="history.back()">Home</button>
<p id="demo">.</p>
<script>
function loadDoc(mylang) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("demo").innerHTML = mylang+":<br> <font color=green>"+ this.responseText+"</font><br>"+document.getElementById("demo").innerHTML;
      document.getElementById("query").value="";
    }
  };
 //alert (mylang);
      
    
  xhttp.open("POST", "/Translation", true);
  xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhttp.send("query="+document.getElementById("query").value+"&lang="+mylang);
}
</script>

</body></html>"""
        return htmltext 
    elif request.method == 'POST':
        #Google Translation using "translate" package from github
        text= (request.form['query'])
        lang= (request.form['lang'])
        trans = Translator("en", lang, text)
        print ("Translating to : "+ lang)
        trans.translate()
        output_string = trans.prettify()
        
    return output_string

@app.route('/EasyEmail', methods=['GET', 'POST'])
def email():

    if request.method == 'GET':
        htmltext=  """<html><title>AI@VWR</title><body>
<H1><b>Welcome to AI/ML  Email Helper</b></H1><br><br>
Your email here : <br> From : <input type=text id="from"><br>Subject : <input type=text id="subject"><br>Body : <input type=text id="body">

<button type="button" onclick="loadDoc('summary')">Summarize !</button>

<button type="button" onclick="history.back()">Home</button>
<p id="demo">.</p>
<script>
function loadDoc(param) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("demo").innerHTML = param+":<br> <font color=green>"+ this.responseText+"</font><br>"+document.getElementById("demo").innerHTML;
      document.getElementById("body").value="";
    }
  };
 //alert (param);
      
    
  xhttp.open("POST", "/EasyEmail", true);
  xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhttp.send("body="+document.getElementById("body").value+"&task="+param+"&from="+document.getElementById("from").value);
}
</script>

</body></html>"""
        return htmltext 
    elif request.method == 'POST':
        emailfrom= (request.form['from'])
        emailbody= (request.form['body'])
        task= (request.form['task'])
        doc = nlp(emailbody)
        result=''
        for entity in doc.ents:
            #print(entity.text, entity.label_)
            result = result+(entity.text)+':'+(entity.label_)+"<br>"
           
        #for token in doc:
            #result = (token.text, token.lemma_, token.pos_,token.tag_, token.dep_)
    
    return result

@app.route('/rss', methods=['GET', 'POST'])
def rss():
    
    
    
    #feedurl1='http://www.moneycontrol.com/rss/business.xml'
    feedurl2='http://wap.business-standard.com/rss/companies-101.rss'
    #data1 = requests.post(feedurl1)
    data2 = requests.post(feedurl2)
    
    parsedData = feedparser.parse(data2.content)
    # set main section to description if empty
    sid = SentimentIntensityAnalyzer()
    resp='<html><title>RSS reader</Title><body>'
    senti=''
    for entry in range(len(parsedData.entries)):
       
           resp=resp+"<a href="+(parsedData.entries[entry]['links'][0]['href'])+'>'+(parsedData.entries[entry]['title'])+'</a><br>'
           resp=resp+(parsedData.entries[entry]['summary'])+'<br><br>'
          
           resp=resp+'</body>,</html>'  
    
    
    
     
     
    
    return resp

""" BLOCK CHAIN CONCEPT"""

# Define what a Snakecoin block is
class Block:
  def __init__(self, index, timestamp, data, previous_hash):
    self.index = index
    self.timestamp = timestamp
    self.data = data
    self.previous_hash = previous_hash
    self.hash = self.hash_block()
  
  def hash_block(self):
    sha = hasher.sha256()
    sha.update((str(self.index) + 
                       str(self.timestamp) + 
                       str(self.data) + 
                       str(self.previous_hash)).encode('utf-8'))
    return sha.hexdigest()

# Generate genesis block
def create_genesis_block():
  # Manually construct a block with
  # index zero and arbitrary previous hash
  return Block(0, date.datetime.now(), {
    "proof-of-work": 9,
    "transactions": None
  }, "0")

# A completely random address of the owner of this node
miner_address = "q3nf394hjg-random-miner-address-34nf3i4nflkn3oi"
# This node's blockchain copy
blockchain = []
blockchain.append(create_genesis_block())
# Store the transactions that
# this node has in a list
this_nodes_transactions = []
# Store the url data of every
# other node in the network
# so that we can communicate
# with them
peer_nodes = []
# A variable to deciding if we're mining or not
mining = True


@app.route('/blocks', methods=['GET'])
def get_blocks():
  
  #chain_to_send = blockchain
  printblocks=''
  # Convert our blocks into dictionaries
  # so we can send them as json objects later
  for i in range(len(blockchain)):
    #block = chain_to_send[i]
    block_index = str(blockchain[i].index)
    block_timestamp = str(blockchain[i].timestamp)
    block_data = str(blockchain[i].data)
    block_hash = blockchain[i].hash
    printblocks=printblocks+"index :"+ block_index+"<br>timestamp : "+block_timestamp+"<br>data :"+block_data+"<br>hash : "+ block_hash+"<br>"    


  return ("<html><Title>Blocks</Title>"+printblocks+"<br><a href=/>Home</a></html>")

def find_new_chains():
  # Get the blockchains of every
  # other node
  other_chains = []
  for node_url in peer_nodes:
    # Get their chains using a GET request
    block = requests.get(node_url + "/blocks").content
    # Convert the JSON object to a Python dictionary
    block = json.loads(block)
    # Add it to our list
    other_chains.append(block)
  return other_chains

def consensus():
  # Get the blocks from other nodes
  other_chains = find_new_chains()
  # If our chain isn't longest,
  # then we store the longest chain
  longest_chain = blockchain
  for chain in other_chains:
    if len(longest_chain) < len(chain):
      longest_chain = chain
  # If the longest chain isn't ours,
  # then we stop mining and set
  # our chain to the longest one
  blockchain = longest_chain

def proof_of_work(last_proof):
  # Create a variable that we will use to find
  # our next proof of work
  incrementor = last_proof + 1
  # Keep incrementing the incrementor until
  # it's equal to a number divisible by 9
  # and the proof of work of the previous
  # block in the chain
  while not (incrementor % 9 == 0 and incrementor % last_proof == 0):
    incrementor += 1
  # Once that number is found,
  # we can return it as a proof
  # of our work
  return incrementor

@app.route('/mine', methods = ['GET'])
def mine():
  
  # Get the last proof of work
  last_block = blockchain[len(blockchain) - 1]
  last_proof = last_block.data['proof-of-work']
  # Find the proof of work for
  # the current block being mined
  # Note: The program will hang here until a new
  #       proof of work is found
  proof = proof_of_work(last_proof)
  # Once we find a valid proof of work,
  # we know we can mine a block so 
  # we reward the miner by adding a transaction
  this_nodes_transactions.append(
    { "from": "network", "to": miner_address, "amount": 1 }
  )
  # Now we can gather the data needed
  # to create the new block
  new_block_data = {
    "proof-of-work": proof,
    "transactions": list(this_nodes_transactions)
  }
  new_block_index = last_block.index + 1
  new_block_timestamp = this_timestamp = date.datetime.now()
  last_block_hash = last_block.hash
  # Empty transaction list
  this_nodes_transactions[:] = []
  # Now create the
  # new block!
  mined_block = Block(
    new_block_index,
    new_block_timestamp,
    new_block_data,
    last_block_hash
  )
  blockchain.append(mined_block)
  # Let the client know we mined a block
  return "<html>"+json.dumps({
      "index": new_block_index,
      "timestamp": str(new_block_timestamp),
      "data": new_block_data,
      "hash": last_block_hash
  }) + "<br><a href=/>Home</a></html>"




@app.route('/txion', methods=['POST','GET'])

def transaction():
  
  if request.method == 'GET':
        htmltext=  """<html><title>AI@VWR</title><body>
    <H1><b>Welcome to VWR Crypto</b></H1><br><br>
    Your crypto ID here : <br> From : <input type=text id="from"><br>Reciepients ID here <input type=text id="to"><br>Amount INR : <input type=text id="amount">

    <button type="button" onclick="payAmt('')">Pay using VWRCrypto !</button><br>

    <button type="button" onclick="location.href='/blocks'">View Block Chain </button><button type="button" onclick="history.back()">Home</button> 
    <p id="demo">.</p>
    <script>
    function payAmt(param) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("demo").innerHTML = param+":<br> <font color=green>"+ this.responseText+"</font><br>"+document.getElementById("demo").innerHTML;
      document.getElementById("body").value="";
    }
    };
    //alert (param);
      

    xhttp.open("POST", "/txion", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send("from="+document.getElementById("from").value+"&to="+document.getElementById("to").value+"&amount="+document.getElementById("amount").value);
    }
    </script>

    </body></html>"""
        return htmltext
  if request.method == 'POST':
    # On each new POST request,
    # we extract the transaction data
    
    new_txion = request.form
    
    print (new_txion["from"])
    # Then we add the transaction to our list
    this_nodes_transactions.append(new_txion)
    # Because the transaction was successfully
    # submitted, we log it to our console
    print ("New transaction")
    print ("FROM: {}".format(new_txion['from']))
    print ("TO: {}".format(new_txion['to']))
    print ("AMOUNT: {}\n".format(new_txion['amount']))
    
    
    return ("Congrats ! You made a transcation using VWR crypto. Now a minor can <a href=/mine> mine now</a> to authenticate transact and he/she will get a VWR coin for that work. <A href=/>Home</a>")
""" The code for block chain is from https://gist.github.com/aunyks/47d157f8bc7d1829a729c2a6a919c173"""
