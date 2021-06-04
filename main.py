import discord
import os
import requests
import json
import random
client = discord.Client()
sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing"]
started_encouragements = [
	"Cheer up!",
	"Hang in there.",
	"You are a great person / bot!"
]
def get_quote():
	response = requests.get("https://zenquotes.io/api/random")
	json_data = json.loads(response.text)
	quote = json_data[0]['q'] + " -" + json_data[0]['a']
	return quote
def update_encoragements(encouraging_message):
	if "encouragements" in db.keys():
		encouragements = db["encouragements"]
		encouragements.append(encouraging_message)
		db["encouragements"] = encouragements
	else:
		db["encouragements"] = [encouraging_message]
def delete_encouragment(index):
	encouragements = db["encouragements"]
	if len(encouragements) > index:
		del encouragements[index]
		db["encouragements"] = encouragements
@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))
@client.event
async def on_message(message):
	if message.author == client.user:
		return
	
	msg = message.content
	if msg.startswith('$inspire'):
		await message.channel.send(get_quote())
	options = started_encouragements
	#print(options)
	if "encouragements" in db.keys():
		#print(db["encouragements"])
		options = options + list(db["encouragements"])
	if any(word in msg for word in sad_words):
		await message.channel.send(random.choice(options))
	if msg.startswith("$new"):
		encouraging_message = msg.split("$new ", 1)[1]
		update_encoragements(encouraging_message)
		await message.channel.send("New encouraging message added.")
	if msg.startswith("$del"):
		encouragements = []
		if "encouragements" in db.keys():
			index = int(msg.split("$del", 1)[1])
			delete_encouragment(index)
			encouragements = db["encouragements"]
		await message.channel.send(encouragements)

#my_secret = os.environ['TOKEN']

client.run(os.environ['TOKEN'])