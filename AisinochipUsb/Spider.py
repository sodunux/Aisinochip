from AisinochipUsb import AisinochipUsb

class Spider():
	def __init__(self):
		self.dev=AisinochipUsb()
		self.OK = 0x00
		self.ERROR= 0x01

	def __del__(self):
		pass

	def Flag(self,str):
		print "******* "+str+" ********"

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

	def SaveStr2File(self,filename,tempstr):
		Flag("SaveStr2File")
		fp=open(filename,"a")
		fp.write(tempstr)
		fp.close()

	def ReadStrFromFile(filename):
		Flag("ReadStrFromFile")
		fp=open(filename,'r')
		filestr=fp.read()
		fp.close()
		return filestr

	def CheckRet(self,tempstr):
		if tempstr[6:8] == "00":
			print "CMD OK"
			return self.OK
		else :
			print "CMD ERROR"
			return self.ERROR


	def Cmd_SelfTest(self,sel="00"):
		self.Flag("Cmd_SelfTest")
		retstr=''
		if sel == "00":
			retstr=self.dev.SendCmd("AAC70055")
		else:
			retstr=self.dev.SendCmd("AAC7"+sel+"55")
		self.CheckRet(retstr)


	def Cmd_SecurityWord(self):
		self.Flag("Cmd_SecurityWord")
		retstr=self.dev.SendCmd("AACC0055")
		self.CheckRet(retstr)


	def Cmd_ChipErase(self):
		self.Flag("Cmd_ChipErase")
		retstr=self.dev.SendCmd("AAD30055")
		self.CheckRet(retstr)

	def Cmd_PageErase(self,baseaddr):
		#70000000
		tempaddr=baseaddr[6:8]+baseaddr[4:6]+baseaddr[2:4]+baseaddr[0:2]
		self.Flag("Cmd_PageErase: "+baseaddr)
		retstr=self.dev.SendCmd("AAD309"+tempaddr+"1A2BE5D455")
		self.CheckRet(retstr)

	def Cmd_DownLoadFlash(self,baseaddr,dat):
		tempaddr=baseaddr[6:8]+baseaddr[4:6]+baseaddr[2:4]+baseaddr[0:2]
		self.Flag("Cmd_DownLoadFlash: "+baseaddr)
		datlen= len(dat)
		if datalen < 16:
			lenstr = '0'+hex(datalen)[2:]
		else :
			lenstr = hex(datalen)[2:]

		if (datalen%2) :
			print "Wrong Data Length!"
		else :
			retstr=self.dev.SendCmd("AAD7"+lenstr+tempaddr+dat+"55")
		self.CheckRet(retstr)

	def Cmd_CheckCrcCode(self):
		self.Flag("Cmd_CheckCrcCode")
		retstr = self.dev.SendCmd("AAD80055")
		self.CheckRet(retstr)

	def Cmd_RunApp(self):
		self.Flag("Cmd_RunApp")
		retstr = self.dev.SendCmd("AAE30055")
		self.CheckRet(retstr)

	def Cmd_ReadSn(self):
		self.Flag("Cmd_ReadSn")
		retstr = self.dev.SendCmd("AAA00055")		
		if retstr[4:6]=="10":
			print "SN: "+retstr[6:-2]
		else:
			print "CMD ERROR"
		return retstr[6:-2]

	def Cmd_ReadVersion(self):
		self.Flag("Cmd_ReadVersion")
		retstr=self.dev.SendCmd("AAA10055")
		if retstr[4:6]=="10":
			print "Verision: "+retstr[6:-2]
		else:
			print "CMD ERROR"
		return retstr[6:-2]

	def Cmd_WrirtePara(self,baseaddr,dat):
		self.Flag("Cmd_WrirtePara")
		tempaddr=baseaddr[6:8]+baseaddr[4:6]+baseaddr[2:4]+baseaddr[0:2]
		datalen = len(dat)
		if datalen < 16:
			lenstr = '0'+hex(datalen)[2:]
		else :
			lenstr = hex(datalen)[2:]

		if (datalen%2) :
			print "Wrong Data Length!"
		else :
			retstr=self.dev.SendCmd("AAD2"+lenstr+tempaddr+dat+"55")
		self.CheckRet(retstr)
	
	def Cmd_Standby(self):
		self.Flag("Cmd_Standby")
		retstr=self.SendCmd("AAA3010055")
		self.CheckRet(retstr)

	def Cmd_Poweroff(self):
		self.Flag("Cmd_Poweroff")
		retstr=self.SendCmd("AAA301BB55")
		self.CheckRet(retstr)

	def Cmd_EnableEncrypt(self):
		self.Flag("Cmd_EnableEncrypt")
		retstr=self.SendCmd("AAA7014B55")
		self.CheckRet(retstr)	

	def Cmd_DisableEncrypt(self):
		self.Flag("Cmd_DisableEncrypt")
		retstr=self.SendCmd("AAA7010055")
		self.CheckRet(retstr)	

	def Cmd_CheckCrcRom(self,lenstr,crcstr):
		self.Flag("Cmd_CheckCrcRom")
		templenstr=lenstr[6:8]+lenstr[4:6]+lenstr[2:4]+lenstr[0:2]
		tempcrcstr=crcstr[2:4]+crcstr[0:2]
		tempcrcstr=hex(0xf-int(tempcrcstr[0:1],16))[2:]
		tempcrcstr=hex(0xf-int(tempcrcstr[1:2],16))[2:]
		tempcrcstr=hex(0xf-int(tempcrcstr[2:3],16))[2:]
		tempcrcstr=hex(0xf-int(tempcrcstr[3:4],16))[2:]
		retstr=self.SendCmd("AAA806"+templenstr+tempcrcstr)
		self.CheckRet(retstr)

	def Cmd_CheckKey(self,keystr="3032313837363037"):
		self.Flag("Cmd_CheckKey")
		retstr = self.dev.SendCmd("AAB008"+keystr+"55")
		self.CheckRet(retstr)

	def Cmd_SetKey(self,keystr="3032313837363037"):
		self.Flag("Cmd_SetKey")
		retstr = self.dev.SendCmd("AAB108"+keystr+"55")
		self.CheckRet(retstr)		

	def Cmd_EnableOther(self):
		self.Flag("Cmd_EnableOther")
		retstr = self.dev.SendCmd("AAAF0500FFFF000055")
		self.CheckRet(retstr)			

	def Cmd_OtherUnlockOTP(self,nvrsel):
		self.Flag("Cmd_OtherUnlockOTP")
		retstr = self.dev.SendCmd("AAAF0101"+nvrsel+"55")
		self.CheckRet(retstr)		

	def Cmd_OtherWriteReg(self,baseaddr,dat):
		self.Flag("Cmd_OtherWriteReg")
		tempaddr=baseaddr[6:8]+baseaddr[4:6]+baseaddr[2:4]+baseaddr[0:2]
		tempdat=dat[6:8]+dat[4:6]+dat[2:4]+dat[0:2]
		retstr=self.dev.SendCmd("AAAF0902"+tempaddr+tempdat+"55")
		self.CheckRet(retstr)	

	def Cmd_OtherRead(self,baseaddr,lenstr):
		self.Flag("Cmd_OtherRead")
		tempaddr=baseaddr[6:8]+baseaddr[4:6]+baseaddr[2:4]+baseaddr[0:2]
		retstr=self.dev.SendCmd("AAAF0603"+tempaddr+lenstr+"55")
		print retstr[6:-2]	
		return retstr[6:-2]			

	def Cmd_GetChallenge(self,lenstr):
		self.Flag("Cmd_GetChallenge")
		retstr=self.dev.SendCmd("AA8401"+lenstr+"55")
		print retstr[6:-2]
		return retstr[6:-2]




if __name__=="__main__":
	sp = Spider()
	sp.Cmd_CheckKey()
	sp.Cmd_ReadVersion()
	sp.Cmd_SelfTest()
	sp.Cmd_GetChallenge("20")
	sp.Cmd_ReadSn()
	sp.Cmd_SetKey("1122334455667788")
	sp.Cmd_CheckKey()
	sp.Cmd_CheckCrcCode()
	sp.Cmd_EnableOther()
	sp.Cmd_OtherRead("00000000","10")

	#sp.Cmd_CheckKey()

