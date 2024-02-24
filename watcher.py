import sys,os,dropbox,json,time
import traceback
APP_KEY = os.getenv('DROPBOX_APPKEY', '')
APP_SECRET = os.getenv('DROPBOX_APPSECRET', '')
TOKEN_FILENAME = 'token.txt'
WATCHED_FILENAME = 'watched.json'
client = None

#remove this line
action = 'run'

def run():
	if action == 'run':
		if len(sys.argv) > 2:
			waitingPeriod = int(sys.argv[2])
		haveTokenFile = os.path.isfile(TOKEN_FILENAME)
		if haveTokenFile is True:
			tFile = open(TOKEN_FILENAME,'r')
			createClient(tFile.read())
		else:
			get_token()
	elif action == 'add':
		print "add"
		if len(sys.argv) < 4:
			print "argv < 4"
			sys.exit()
		have_list_of_watched_files = os.path.isfile(WATCHED_FILENAME)
		if have_list_of_watched_files is not True:
			quickWrite = open(WATCHED_FILENAME,'w+')
			quickWrite.write('[]')
			quickWrite.close()
		currentListFile = open(WATCHED_FILENAME,'r+')
		if sys.argv[2] == 'file':
			#add a file to watch
			separateFileAndFolder = sys.argv[3].rsplit('/',1)
			path = separateFileAndFolder[0]
			thefile = separateFileAndFolder[1]
			currentList = json.loads(currentListFile.read())
			currentList.append({
				'type' : 'file',
				'path' : path + '/',
				'name' : thefile,
				'size' : os.stat(thefile).st_size
			})
			overwrite = open(WATCHED_FILENAME,'w')
			overwrite.write(json.dumps(currentList)) 
		elif sys.argv[2] == 'folder':
			#add a folder to watch
			print "adding a folder"
			path = sys.argv[3].decode('string_escape')
			folderItems = []
			for path,folder_names, files in os.walk(path):
				pathSplit = path.rsplit('/',1)
				thisItem = {
					'type' : 'folder',
                                	'path' : pathSplit[0] + '/',
                                	'name' : pathSplit[1],
                                	'size' : 0
				}
			folderItems.append(thisItem)
			for items in folderItems:
				currentList.append(item)
			overwrite = open(WATCHED_FILENAME,'w')
			overwrite.write(json.dumps(currentList))
		else:
			print "invalid parameters"
	else:
		print "you've not passed a valid argument"
		print "run or add are valid arguments"

def load_list_of_watched_files_and_folders():
	f = open(WATCHED_FILENAME,'w')
	thingsWeAreWatching = json.loads(f.read())
	now_my_watch_begins(thingsWeAreWatching)
	f.close()

def now_my_watch_begins(fileList):
	print "now my watch begins"
	for item in fileList:
		if item['type'] == 'file':
			check_contents_of_file(item)
		elif item['type'] == 'folder':
			check_contents_of_folder(item)
global items
f = open(WATCHED_FILENAME,'w+')
f.write(json.dumps(items))
items = []
time.sleep(waitingPeriod)
f = open(WATCHED_FILENAME,'r+')
thingsWeAreWatching = json.loads(f.read())
now_my_watch_begins(thingsWeAreWatching)

def get_token():
	global client
	flow = dropbox.client.DropboxOAuth2FlowNoRedirect(APP_KEY,APP_SECRET)
	authorize_url = flow.start()
	print "Open the following in your browser..."
	print authorize_url
	token = raw_input("... and then enter your authorization code here: ").strip()
	access_token, user_id = flow.finish(token)
	print access_token
	
	#store the token
	storeToken = open(TOKEN_FILENAME,'w')
	storeToken.write(access_token)
	storeToken.close()
	
	#client = dropbox.client.DropboxClient(access_token)
	createClient(access_token)
	print client.account_info()

def createClient(token):
	global client
	try:
		client = dropbox.client.DropboxClient(token)
		load_list_of_watched_files_and_folders();
	except Exception,e:
		print "error accessing dropbox "
		print(traceback.format_exc())
		get_token()
		

if __name__ == '__main__':
	run()
