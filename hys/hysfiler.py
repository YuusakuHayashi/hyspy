#HTML_HEADER = './config/template_html_header'

def writeHtmlHeader(CONF_FILE):
    with open(CONF_FILE, 'r', encoding='utf-8') as conf_file:
        return conf_file.read()

class HysFiler:
    def __init__(self, my_file, open_type='utf-8'):
        self.type = open_type
        #self.file = open(my_file, encoding=self.type)
        self.file = my_file

    def copy_file(self, reigion, out_file="copy"):
        inf = self.file
        with open(out_file, 'w') as otf: 
            line_cnt = 1
            for line in inf:
                if line_cnt >= reigion[0] and line_cnt <= reigion[1]:
                    otf.write(line)
                line_cnt += 1
            inf.close()

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
    

    #def __del__(self):
    #    self.file.close()
