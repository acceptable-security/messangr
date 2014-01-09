from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from base64 import b64decode

class RSAEncryption():
	def __init__(self, bits=2048,generate=False):
		new_key = RSA.generate(bits, e=65537) 
		if generate:
			self.public_key = new_key.publickey() 
			self.private_key = new_key
	def encrypt(self, message):
		rsakey = PKCS1_OAEP.new(self.public_key)
		encrypted = rsakey.encrypt(message)
		return encrypted.encode('base64')
	def decrypt(self, message):
		rsakey = PKCS1_OAEP.new(self.private_key)
		decrypted = rsakey.decrypt(b64decode(message))
		return decrypted
	def publishKey(self):
		return self.public_key.exportKey("PEM")
	def sendMessage(self, key, message):
		rsakey = RSA.importKey(key)
		key = PKCS1_OAEP.new(rsakey)
		encrypted = key.encrypt(message)
		return encrypted.encode('base64')
	def savePrivate(self):
		private_key = self.private_key.exportKey("PEM")
		return private_key
	def loadPrivate(self, fileContents_private, fileContents_public):
		new_key = RSA.importKey(fileContents_private)
		new_key = PKCS1_OAEP.new(new_key)
		self.private_key = new_key
		_key = RSA.importKey(fileContents_public)
		_key = PKCS1_OAEP.new(_key)
		self.public_key = _key

if __name__ == "__main__":
	rsa = RSAEncryption()
	print rsa.savePrivate()