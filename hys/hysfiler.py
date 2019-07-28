#HTML_HEADER = './config/template_html_header'

def writeHtmlHeader(CONF_FILE):
    with open(CONF_FILE, 'r', encoding='utf-8') as conf_file:
        return conf_file.read()

class HysFiler:
    def __init__(self,my_file,enc='utf-8'):
        self.enc=enc
        self.file = open(my_file, encoding=self.enc)

    #def copy_file(self, reigion, out_file="copy"):
    def simple_copy(self,out_file="copy"):
        inf = self.file
        with open(out_file, 'w') as otf: 
            for line in inf:
                otf.write(line)
                #if line_cnt >= reigion[0] and line_cnt <= reigion[1]:
                #    otf.write(line)
                #line_cnt += 1

    def lectangle_copy(self,lect,out_file="copy"):
        inf = self.file
        inf.seek(0,0)
        with open(out_file, 'w') as otf: 
            for line in inf:
                s = self.lfetch(self.rtrimer(line.strip(),lect[1],self.enc),lect[0],self.enc)
                otf.write(s + "\n")

    def read_user_cfg(self):
        with open(self.file, 'r') as inf:
            ln = 0
            dic = {}
            for line in inf:
                ln+=1
                if ln == 1:
                    dic["user"] = line.strip("\n")
                if ln == 2:
                    dic["email"] = line.strip("\n")
                if ln == 3:
                    dic["pass"] = line.strip("\n")
                    break
            return dic

    def rtrimer(self,s,b,e):
        #s...string
        #b...bytes
        #e...encoding
        while len(s.encode(e))>b:
            s=s[:-1]
        return s
    
    def ltrimer(self,s,b,e):
        #s...string
        #b...bytes
        #e...encoding
        while len(s.encode(e))>b:
            s=s[-1:]
        s.seek(0,0)
        return s
    
    def lfetch(self,s,b,e):
        #s...string
        #b...bytes
        #e...encoding
        while len(s.encode(e))<b:
            s+=s[:1]
        return s

    def __del__(self):
        self.file.close()
