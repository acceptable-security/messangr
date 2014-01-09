import sqlite3, os, sys, uuid, lib
class MessangrPostsData:
	def __init__(self, filename="posts.db"):
		self.filename = filename
		if not os.path.exists(filename):
			self.conn = sqlite3.connect(filename)
			if not self.initSQL():
				print "Can't init SQL."
				sys.exit(1)
			else:
				print "init SQL"
		else:
			self.conn = sqlite3.connect(filename)
	def initSQL(self):
		try:
			curr = self.conn.cursor()

			curr.execute('CREATE TABLE posts(posterID text, fileName text, fileInfo text, message text, postID text)')
			curr.execute('CREATE TABLE comments(posterID text, fileName text, fileInfo text, message text, postID text, opID text)')

			self.conn.commit()
			return True
		except:
			return False

	def reinitSQL(self):
		self.conn = sqlite3.connect(self.filename)

	def addPost(self, posterID, fileName, message):
		try:
			self.reinitSQL()
			curr = self.conn.cursor()

			if os.path.exists("static/uploads/" + fileName):
				fileInfo = lib.imageSize("static/uploads/" + fileName)
				fileInfo = fileName + " (" + str(fileInfo[0][0]) + "x" + str(fileInfo[0][1]) + ", " + str(fileInfo[1]) + fileInfo[2] +")"
			else:
				fileInfo = ""

			curr.execute('INSERT INTO posts VALUES (?,?,?,?,?)',(posterID,fileName,fileInfo,message,str(uuid.uuid4())))

			self.conn.commit()
			self.conn.close()
			return True
		except:
			return False

	def addComment(self, posterID, fileName, message, postID):
		try:
			if self.getPostID(postID) == None:
				return False
			self.reinitSQL()
			curr = self.conn.cursor()
			if not fileName == "":
				if os.path.exists("static/uploads/" + fileName):
					fileInfo = lib.imageSize("static/uploads/" + fileName)
					fileInfo = fileName + " (" + str(fileInfo[0][0]) + "x" + str(fileInfo[0][1]) + ", " + str(fileInfo[1]) + fileInfo[2] +")"
			else:
				fileInfo = ""

			curr.execute('INSERT INTO comments VALUES (?,?,?,?,?,?)',(posterID,fileName,fileInfo,message,str(uuid.uuid4()),postID))

			self.conn.commit()
			self.conn.close()
			return True
		except:
			return False

	def getPostID(self, postID):
		try:
			self.reinitSQL()
			curr = self.conn.cursor()

			curr.execute('SELECT * FROM posts WHERE postID=?',(postID,))
			fetch = curr.fetchone()

			self.conn.close()
			return fetch
		except:
			return None

	def getPosts(self,amount=10, offset="", page=""):
		try:
			self.reinitSQL()
			curr = self.conn.cursor()

			curr.execute('SELECT * FROM posts')
			fetch = curr.fetchall()

			self.conn.close()
			fetch = fetch[::-1]
			if offset != "":
				return fetch[offset:offset+amount]
			elif page != "":
				print (page*amount)+amount
				return fetch[page*amount:(page*amount)+amount]
			else:
				return fetch
		except:
			return []

	def getPostComments(self, postID):
		try:
			self.reinitSQL()
			curr = self.conn.cursor()

			curr.execute('SELECT * FROM comments WHERE opID=?',(postID,))
			fetch = curr.fetchall()

			self.conn.close()
			return fetch
		except:
			return []

if __name__ == "__main__":
	db = MessangrPostsData()
	#print db.addPost("lolcopter","a.jpg","how is messangr doing today !!!!!!!!")
	print db.getPosts(offset=2,amount=3)
	#print db.addComment("bigdaddy","",":)))))))))))) absolutely god damn fucking amazing.","ed6dd9a5-5416-4b72-a2c2-eb55a035bf15")
	#print db.addComment("suicidial fag","test.jpg","brb going to kill myself","ed6dd9a5-5416-4b72-a2c2-eb55a035bf15")
	#print db.getPostComments("ed6dd9a5-5416-4b72-a2c2-eb55a035bf15")
	pass