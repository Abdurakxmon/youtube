from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
import os 
from pytube import YouTube
import glob
import requests
from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import moviepy.editor as mp
import shutil
from pytube.cli import on_progress
from time import time
import sqlite3

database = sqlite3.connect('data.db')

app = Client(
    "--bot id--",
    api_id="--api_id--",
    api_hash="--api_hash--"
)

print('Sucsess!')
global loo
global admin
global ban_list

ban_list=['']
loo=[]
admin='--admin_id--' 
async def progress(current, total,ids,message,ans):
	prog = f"{current * 100 / total:.1f}"
	count=int(prog[:prog.index('.')])
	padjn = (count//5)*'█'
	proga = f'|{padjn}| {count}%'
	if count not in loo:
		loo.append(count)
		try:
			await app.edit_message_caption(ids,message,f'🔉{ans.title}<a href = "{link}"> → </a>\n👤<a href = "{ans.channel_url}">#{ans.author}</a>\n\nSending...\n{proga}\n\n@YouTube_Mp4_bot', parse_mode = "HTML")
		except:
			pass
		if count==100:
			loo.clear()

@app.on_message()
async def start(client, message):
	if (f'<code>{message.chat.id}</code> @{message.from_user.username}' in ban_list):
		await app.send_message(message.chat.id,f'You are banned. Unban: @abdurakhmonnn')
	elif message.text=='/start':
		try:
			database.execute("INSERT INTO USERS VALUES (?,?);",(message.chat.id,message.from_user.username));
			database.commit()	
			await app.send_document(admin,'data.db', caption=f'🤖 <code>{message.chat.id}</code> @{message.from_user.username} botga start bosdi.', parse_mode='HTML')
			database.save()
		except:
			pass
		await app.send_message(message.chat.id,'👋 This is youtube saver bot.')
	elif message.text=='/help':
		await app.send_photo(message.chat.id,open('example.jpg', "rb"),caption='👋 This bot for download videos from YouTube.\nSand me link like this.')
	elif (message.chat.id==admin) and ('/ban' in message.text):
		user_id=int(message.text[5:])
		try:
			for row in database.execute("SELECT * FROM USERS WHERE ID = '%s'" % user_id):
				user_infos='<code>'+str(user_id)+'</code>'+' @'+str(row[1])
		except:
			pass
		try:
			ban_list.append(user_infos)
			await app.send_message(user_id,'You are banned 🚫 by admin.')
			await app.send_message(admin,f'{user_infos} is banned 🚫 by admin.')
		except:
			await app.send_message(admin,f'{user_infos} isn`t banned.')
	elif (message.chat.id==admin) and ('/unban' in message.text):
		user_id=int(message.text[7:])
		try:
			for row in database.execute("SELECT * FROM USERS WHERE ID = '%s'" % user_id):
				user_infos='<code>'+str(user_id)+'</code>'+' @'+str(row[1])
		except:
			pass
		try:
			ban_list.remove(user_infos)
			await app.send_message(user_id,'You are unbanned ♻️ by admin.')
			await app.send_message(admin,f'{user_infos} is unbanned ♻️ by admin.')
		except:
			await app.send_message(admin,f'{user_infos} isn`t unbanned.')
	elif (message.chat.id == admin) and ('/members'== message.text):
		strr=''
		count=0
		cursor = database.execute("SELECT id, name from USERS")
		for row in cursor:
		   strr+='<code>'+str(row[0])+'</code>'+" @"+str(row[1])+'\n'
		   count+=1
		await app.send_document(admin,'data.db')
		await app.send_message(admin,f'Userlar soni: {count}\n{strr}', parse_mode='HTML')
		await app.send_message(admin,f'Ban users: {ban_list}', parse_mode='HTML')

	elif (message.chat.id == admin) and ('/storage'==message.text):
		mapp=glob.glob('*')
		directory=''
		for i in range(len(mapp)):
			directory+=f'{mapp[i]}\n'
		await app.send_message(admin,directory)
	elif (message.chat.id == admin) and ('/del' in message.text):
		try:
			shutil.rmtree(f'{message.text[5:]}//')
			await app.send_message(admin,'Done!')
		except:
			await app.send_message(admin,'Error path!')
	else:
		try:
			database.execute("INSERT INTO USERS VALUES (?,?);",(message.chat.id,message.from_user.username));
			database.commit()
			await app.send_document(admin,'data.db', caption=f'🤖 <code>{message.chat.id}</code> @{message.from_user.username} botga start bosdi.', parse_mode='HTML')
			database.save()
		except:
			pass
		try:
			global ans
			global link
			link = message.text
			ans=YouTube(message.text,on_progress_callback=on_progress)
			yt=ans.streams.filter(progressive=True,file_extension='mp4').all()
			ls=[]
			size=[]
			for i in range(len(yt)):
				size.append(yt[i].filesize)
				ls.append(int(yt[i].resolution.replace('p','')))
			ls=list(set(ls))
			markup_ls=[]
			test=[]
			for i in range(len(ls)):
				sizes = f"{size[i] / 1024000:.1f}"
				test.append(InlineKeyboardButton(f'📹{ls[i]}p ({sizes}mb)',callback_data=f'{ls[i]}'))
				if i%3==0 and i!=0:
					markup_ls.append(test)
					test=[]
			markup_ls.append(test) 
			sizes = f"{ans.streams.filter(only_audio=True,file_extension='mp4').first().filesize / 1024000:.1f}"
			test=[InlineKeyboardButton(f'🔊MP3 ({sizes}mb)',callback_data=f'audio'),InlineKeyboardButton('🖼',callback_data='img')]
			markup_ls.append(test)
			markup=InlineKeyboardMarkup(markup_ls)
			await app.send_photo(message.chat.id,ans.thumbnail_url,reply_markup=markup, caption=f'📹{ans.title}<a href = "{message.text}"> → </a>\n👤<a href = "{ans.channel_url}">#{ans.author}</a>\n\nResolution for download. ↓', parse_mode = "HTML")
		except:
			await app.send_message(message.chat.id,'Please send YouTube link. /help')


@app.on_callback_query()
async def answer(client, callback_query):
	await app.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id)
	await app.edit_message_caption(callback_query.message.chat.id, callback_query.message.message_id,f'{ans.title}<a href = "{link}"> → </a>\n👤<a href = "{ans.channel_url}">#{ans.author}</a>\n\nDownloading...\n\n@YouTube_Mp4_bot', parse_mode = "HTML")
	if os.path.isdir(f'./{callback_query.message.chat.id}'):
		await app.send_message(callback_query.message.chat.id,'You are already shooting a video.')
	else:
		if callback_query.data == 'img':
			with open('files/pic.jpg', 'wb') as handle:
				response = requests.get(ans.thumbnail_url, stream=True)
				for block in response.iter_content(1024):
					if not block:
						break
					handle.write(block)
			os.rename('files/pic.jpg',f'files/{ans.title}.jpg')
			await callback_query.message.reply_document(open(f'files/{ans.title}.jpg', "rb"),progress=progress,progress_args=(callback_query.message.chat.id,callback_query.message.message_id,ans), caption=f'🖼{ans.title}<a href = "{link}"> → </a>\n\n@YouTube_Mp4_bot', parse_mode = "HTML")
			os.rename(f'files/{ans.title}.jpg','files/pic.jpg')
		
		elif callback_query.data == 'audio':
			try:		
				ans.streams.filter(only_audio=True).first().download(f'{callback_query.message.chat.id}//')
				await callback_query.message.reply_audio(open(min(glob.glob(f'{callback_query.message.chat.id}//'), key=os.path.getctime),'rb').name,progress=progress,progress_args=(callback_query.message.chat.id,callback_query.message.message_id,ans), caption=f'🔉{ans.title}<a href = "{link}"> → </a>\n👤<a href = "{ans.channel_url}">#{ans.author}</a>\n\n@YouTube_Mp4_bot:🔉 MP3', parse_mode = "HTML")		
			except:
				await callback_query.message.reply_text('Something went wrong. Try again.')
			try:
				shutil.rmtree(f'{callback_query.message.chat.id}//')
			except:
				pass
		else:
			if ans.streams.filter(progressive=True,res=f'{callback_query.data}p',file_extension='mp4').first().filesize >= 2147483648:
				await callback_query.message.reply_text('This video large then 2gb. 🛑')
			else:
				try:
					ans.streams.filter(progressive=True,res=f'{callback_query.data}p',file_extension='mp4').first().download(f'{callback_query.message.chat.id}')
					await callback_query.message.reply_video(open(min(glob.glob(f'{callback_query.message.chat.id}//*'), key=os.path.getctime),'rb').name,progress=progress,progress_args=(callback_query.message.chat.id,callback_query.message.message_id,ans), caption=f'📹{ans.title}<a href = "{link}"> → </a>\n👤<a href = "{ans.channel_url}">#{ans.author}</a>\n\n@YouTube_Mp4_bot:📹{callback_query.data}p', parse_mode = "HTML")	
				except:
					await callback_query.message.reply_text('Something went wrong. Try again.')
				try:
					shutil.rmtree(f'{callback_query.message.chat.id}//')
				except:
					pass
	await app.delete_messages(callback_query.message.chat.id,callback_query.message.message_id)	
app.run()
