import usb.core
import usb.util

class AisinochipUsb:
	def __init__(self):
		self.GetDev()
		self.GetBulkOutEp()
		self.GetBulkInEp()
		pass
	def __del__(self):
		pass
	def GetDevByID(self):
		self.dev = usb.core.find(idVendor=0x1234,idProduct=0xabcd)
		if self.dev == None:
			print "No Aisinochip Device!"
		else :
			self.dev.set_configuration()
			print "Get Aisinochip Device Success!"

	def GetDev(self):
		self.dev = usb.core.find()
		if self.dev == None:
			print "No Aisinochip Device!"
		else:
			self.dev.set_configuration()
			print "Get Aisinochip Device Success!"

	def GetBulkOutEp(self):
		self.cfg  = self.dev.get_active_configuration()
		self.intf = self.cfg[(0,0)]
		self.BulkOutEp = usb.util.find_descriptor(
		    self.intf,
		    # match the first OUT endpoint
		    custom_match = \
		    lambda e: \
		        usb.util.endpoint_direction(e.bEndpointAddress) == \
		        usb.util.ENDPOINT_OUT)
		#print self.BulkOutEp	

	def GetBulkInEp(self):
		self.cfg  = self.dev.get_active_configuration()
		self.intf = self.cfg[(0,0)]
		self.BulkInEp = usb.util.find_descriptor(
		    self.intf,
		    # match the first OUT endpoint
		    custom_match = \
		    lambda e: \
		        usb.util.endpoint_direction(e.bEndpointAddress) == \
		        usb.util.ENDPOINT_IN)
		#print self.BulkInEp
		
	def Write(self,cmdstr):
		tempstr=cmdstr.replace(" ","")
		tempstr=self.Str2Hex(tempstr)
		self.BulkOutEp.write(tempstr)

	def Read(self):
		retlist=self.BulkInEp.read(256,100).tolist()
		return self.List2Str(retlist)

	def SendCmd(self,cmdstr):
		self.Write(cmdstr)
		retstr = self.Read()
		cmdstr= cmdstr.upper()
		retstr= retstr.upper()
		print cmdstr + " --> " + retstr
		return retstr

	def List2Str(self,templist):
		retstr=''
		for i in templist:
			if i<16:
				retstr += "0"+ hex(i)[2:]
			else :
				retstr += hex(i)[2:]
		return retstr

	def Str2Hex(self,tempstr):
		#"AABB"->"\xaa\xbb"
		strlen=len(tempstr)
		retstr=''
		if strlen%2 != 0 :
			print "Str length error!"
		else :
			for i in range(strlen/2):
				c = tempstr[i*2:2*i+2]
				t = int(c,16)
				retstr += chr(t)
		return retstr

	def Hex2Str(self,tempstr):
		#'ab'->'6566'
		strlen = len(tempstr)
		retstr = ''
		for i in range(strlen):
			c = tempstr[i:i+1]
			t = ord(c)
			if t <16:           
				retstr +='0'+hex(t)[2:]
			else :
				retstr += hex(t)[2:]
		return retstr



if __name__ == "__main__":
	Adev = AisinochipUsb()
	Adev.SendCmd("AAB008303231383736303755")
	Adev.SendCmd("AAA10055")
	#Adev.Write("AAB008303231383736303755")
	#print Adev.Read()
	#Adev.Write("AAA10055")
	#print Adev.Read()


