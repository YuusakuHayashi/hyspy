import re
import sys 


USING_STATEMENT_TEXT            = "------ [HYS-COBOL-PARSE]\n"
PATTERN_ASTERISK                = "*"
PATTERN_DATA_ITEM               = "^\s*[0-4][0-9]\s+[A-Z]+"
PATTERN_PERIOD                  = "\.\s*$"
PATTERN_USING_STATEMENT         = "(\s{8}[0-9]{6}|[0-9]{6})\s*PROCEDURE\s*DIVISION\s*USING"
PATTERN_IDENTIFICATION_DIVISION = "(\s{8}[0-9]{6}|[0-9]{6})\s*IDENTIFICATION\s*DIVISION.*\n"
PATTERN_ENVIRONMENT_DIVISION    = "(\s{8}[0-9]{6}|[0-9]{6})\s*ENVIRONMENT\s*DIVISION.*\n"
PATTERN_DATA_DIVISION           = "(\s{8}[0-9]{6}|[0-9]{6})\s*DATA\s*DIVISION.*\n"
PATTERN_PROCEDURE_DIVISION      = "(\s{8}[0-9]{6}|[0-9]{6})\s*PROCEDURE\s*DIVISION.*\n"

class HysCoboler:
    __reigion_lineno__   = slice(0, 6)
    __reigion_mark__     = slice(6, 7)
    __reigion_a__        = slice(7, 11)
    __reigion_b__        = slice(11, 72)
    __reigion_headline__ = slice(72, 80)
    __reigion_ab__       = slice(7, 72)
    
    __identification_division__ = 0
    __environment_division__    = 1 
    __data_division__           = 2
    __procedure_division__      = 3

    parse_using_statement_flag     = True
    parse_delimited_statement_flag = True

    parse_identification_division_flag = True
    parse_environment_division_flag    = True
    parse_data_division_flag           = True
    parse_procedure_division_flag      = True

    __start_identification_division__ = "0" 
    __end_identification_division__   = "0" 
    __start_environment_division__    = "0" 
    __end_environment_division__      = "0" 
    __start_data_division__           = "0" 
    __end_data_division__             = "0" 
    __start_procedure_division__      = "0" 
    #__end_procedure_division__        = "0" 

    __pattern_data_item__        = "^\s*[0-4][0-9]\s+[A-Z]+"
    __pattern_file_description__ = "^FD\s\s$"
    __pattern_block_contains__   = "^\s*BLOCK\s+CONTAINS\s+[0-9]+\s+RECORDS\s*$"
    __pattern_file_value_of__    = "(^\s*VALUE\s+OF)?\s*((AREASIZE\s+|AREAS\s+|SAVEFACTOR\s+)IS\s+[0-9]+|TITLE\s+[A-Z])"
    __pattern_data_01__          = "^01\s\s$"
    __pattern_data_item_level__  = "^\s*([0-4][0-9])"
    __pattern_data_item_type1__  = "\s+PIC\s+([9X])\s*\([0-9]+\)"
    __pattern_data_item_size1__  = "\s+PIC\s+[9X]\s*\(([0-9]+)\)\."
    __pattern_data_item_size2__  = "\s+PIC\s+(99+|[9-]+[9Z]+)\."
    __pattern_data_item_size3__  = "\s+PIC\s+[9X]\s*\(([0-9]+)\)\s+OCCURS\s+[0-9]+\."
    __pattern_data_item_name__   = "\s+([0-9A-Z-]+)\.?\s+"
    __pattern_data_item_occurs__  = "\s+OCCURS +([0-9]+).*\."
    __pattern_data_item_pic__    = "\s+PIC\s+\(([0-9]+)\)\s+"

    def __init__(self, cobol):
        self.cobol = cobol 
        self.__parse_div__()

    def __parse_div__(self):
        pre_lineno = "" 
        with open(self.cobol, 'r') as cbl:
            for line in cbl:
                if self.parse(PATTERN_IDENTIFICATION_DIVISION, line):
                    self.__start_identification_division__ = line[self.__reigion_lineno__]
                if self.parse(PATTERN_ENVIRONMENT_DIVISION, line):
                    self.__end_identification_division__   = pre_lineno 
                    self.__start_environment_division__    = line[self.__reigion_lineno__]
                if self.parse(PATTERN_DATA_DIVISION, line):
                    self.__end_environment_division__      = pre_lineno 
                    self.__start_data_division__           = line[self.__reigion_lineno__]
                if self.parse(PATTERN_PROCEDURE_DIVISION, line):
                    self.__end_data_division__             = pre_lineno 
                    self.__start_procedure_division__      = line[self.__reigion_lineno__]
                pre_lineno = line[self.__reigion_lineno__]

    def __current_division__(self, lineno):
        if int(lineno) < int(self.__start_environment_division__):
            return self.__identification_division__ 
        elif int(lineno) < int(self.__start_data_division__):
            return self.__environment_division__ 
        elif int(lineno) < int(self.__start_procedure_division__):
            return self.__data_division__ 
        else:
            return self.__procedure_division__ 

    def simple_layout(self, html_file="layout.html", css_file="layout.css"):
        i = 0
        j = 0
        #html_main = ""
        html_resv = ""
        html_scal = ""
        data_level = 0
        #repeat = []
        repeat = 0 
        parent_level = 0
        #parent_level = [] 
        occurs_flag = False
        div_id = 0
        div_part = 0
        html_main = [[]] 
        html_values = {}
        el_class = 0
        el_size = 0 
        el_name = ""
        el_size_sum = 0
        with open(css_file, 'w') as css:
            css.write("body{font-family:monospace;}\n")
            css.write(".cls1{display:flex;width:max-content;border-top:solid thin;border-bottom:solid thin;word-wrap:break-word;margin-top:10px;}\n")
            css.write(".cls2{text-align:center;border-left:solid thin;}\n")
            css.write(".cls3{display:inline-block;border-left:solid thin;text-align:center;width:9px;}\n")
            with open(html_file, 'w') as html:
                with open(self.cobol, 'r') as cbl:
                    for line in cbl:
                        mark = line[self.__reigion_mark__]
                        rgna = line[self.__reigion_a__]
                        rgnb = line[self.__reigion_b__]
                        if mark == " ":
                            if self.parse(self.__pattern_file_description__, rgna):
                                file_name = rgnb.strip()
                                html.write("<title>" + file_name + "</title>")
                                html.write("<link rel='stylesheet' href='layout.css'></link>")
                                html.write(file_name)
                            if self.parse(self.__pattern_block_contains__, rgnb):
                                html.write("<br />" + rgnb + "<br />")
                            if self.parse(self.__pattern_file_value_of__, rgnb):
                                html.write(rgnb + "<br />")
                            if self.parse(self.__pattern_data_01__, rgna):
                                html.write("<div>" + rgnb + "</div>\n")
                                #html_scal = "<div>\n"
                                el_level = 1
                            el_class = 2
                            el_level = 0
                            el_size  = 0
                            match = self.parseII(self.__pattern_data_item_level__, rgnb)
                            if match:
                                el_level = int(match.group(1))
                                #{{{
                                #if occurs_flag:
                                #    if data_level <= parent_level[0]:
                                #        i = 0
                                #        while i < repeat:
                                #            for item in html_resv:
                                #            #fot item in reversed(html_resv):
                                #                html_main.append(item)
                                #            i+=1
                                #        occurs_flag = False 
                                #else:
                                #    html_resv = [[]]
                                #}}}
                                match2 = self.parseII(self.__pattern_data_item_name__, rgnb.lstrip()[2:])
                                if match2:
                                    el_name = match2.group(1)
                                    match5 = self.parseII(self.__pattern_data_item_occurs__, rgnb)
                                    if match5:      #OCCURS
                                        occurs_flag = True
                                        parent_level = int(match.group(1))
                                        #parent_level.append(int(match.group(1)))
                                        repeat = int(match5.group(1))
                                        html_main.append([1, 0, el_name, el_level, repeat])
                                        repeat = 0
                                    match6 = self.parseII(self.__pattern_data_item_size3__, rgnb)
                                    if match6:
                                        el_size = int(match6.group(1))
                                        html_main.append([el_class, el_size, el_name, el_level, repeat])
                                        #i = 0
                                        item_type = self.parseII(self.__pattern_data_item_type1__, rgnb).group(1)
                                        #while i < repeat+1:
                                        #    html_main.append([el_class, el_size, el_name, el_level, parent_level, repeat])
                                            #html_main.append([el_class, el_size, el_name])
                                        #    i+=1
                                        html_scal += (("<div class='cls3'>" + item_type + "</div>")*el_size)*(repeat+1)
                                        occurs_flag = False
                                        continue
                                    match3 = self.parseII(self.__pattern_data_item_size1__, rgnb)
                                    if match3:
                                        el_size = int(match3.group(1))
                                        item_type = self.parseII(self.__pattern_data_item_type1__, rgnb).group(1)
                                        html_main.append([el_class, el_size, el_name, el_level, repeat])
                                        #html_main.append([el_class, el_size, el_name])
                                        #html_resv.append([el_class, el_size, el_name, el_level])
                                        html_scal += ("<div class='cls3'>" + item_type + "</div>")*el_size
                                        continue
                                    match4 = self.parseII(self.__pattern_data_item_size2__, rgnb)
                                    if match4:
                                        el_size = len(match4.group(1))
                                        html_main.append([el_class, el_size, el_name, el_level, repeat])
                                        #html_main.append([el_class, el_size, el_name])
                                        #html_resv.append([el_class, el_size, el_name])
                                        for char in match4.group(1):
                                            html_scal += "<div class='cls3'>" + char + "</div>"
                                        continue

                repeat_arr = [[99,99]]
                for item in html_main:
                    if item:
                        if item[4]:
                            repeat_arr.append([item[3], item[4]])
                            continue
                        if item[3] =< repeat_arr[-1][0]:
                            html_sub.
                        else:
                            html_sub.append(item)
                            tmp.append(item)

                #html.write("<div class='cls1'>\n")
                #for item in html_main:
                #    print(item)
                    #if item:
                    #    if item[1] > 0:
                    #        while True:
                    #            if item[1] + el_size_sum > 100:
                    #                el_size_right = 100 - el_size_sum
                    #                el_size_left  = item[1] - el_size_right
                    #                html.write("<div " + "class='cls" + str(item[0]) + "' style='width:" + str(el_size_right*10-1) + "px;'>" + item[2] + "</div>\n")
                    #                html.write("</div>\n")
                    #                html.write("<div class='cls1'>\n")
                    #                el_size_sum = 0
                    #                item[1]  = item[1] - el_size_right
                    #            elif item[1] + el_size_sum == 100:
                    #                html.write("<div " + "class='cls" + str(item[0]) + "' style='width:" + str(item[1]*10) + "px;'>" + item[2] + "</div>\n")
                    #                html.write("</div>\n")
                    #                html.write("<div class='cls1'>\n")
                    #                el_size_sum = 0
                    #                break
                    #            else:
                    #                html.write("<div " + "class='cls" + str(item[0]) + "' style='width:" + str(item[1]*10-1) + "px;'>" + item[2] + "</div>\n")
                    #                el_size_sum += item[1]
                    #                break
                html.write("</div>\n")
                                
    def format(self, indent_level=1, out_file="format.cbl"):
        indent = 0
        with open(out_file, 'w') as outf:
            with open(self.cobol, 'r') as cbl:
                for line in cbl:
                    if line[self.__reigion_mark__] == " ":
                        #コメントはインデントしない
                        if line[self.__reigion_a__] == "    ":
                        #A領域からの文はインデントしない
                            lstriped = line[self.__reigion_b__].lstrip()
                            if self.__current_division__(line[self.__reigion_lineno__]) == self.__data_division__:
                                if self.parse(PATTERN_DATA_ITEM, line[self.__reigion_b__]):
                                #データ項目でのインデント
                                    indent = int(lstriped[:2]) - 2
                            indented = " "*indent + lstriped 
                            if len(indented.rstrip().encode('utf-8')) < 61:
                            #インデント込みで80文字オーバするのを回避
                                byte_length = len(indented.encode('utf-8'))
                                margin = 61 - byte_length
                                if margin > 0:
                                #80文字になるよう調整
                                    margin_trimed = "{0:<61}".format(indented)
                                else:
                                    margin_trimed = indented[:61]
                                outf.write(
                                    line[self.__reigion_lineno__] 
                                    + line[self.__reigion_mark__] 
                                    + line[self.__reigion_a__] 
                                    + margin_trimed 
                                    + line[self.__reigion_headline__] 
                                    + "\n"
                                )
                                if self.parse(PATTERN_PERIOD, line[self.__reigion_ab__]): 
                                #IF文等によるインデントの後判定
                                    indent = 0
                                else:
                                    indent = indent + indent_level
                            continue
                    outf.write(line)


    def split(self, mode, out_file="split.txt"):
        write_flag = False 
        with open(out_file, 'w') as outf:
            with open(self.cobol, 'r') as cbl:
                for line in cbl:
                    if mode == self.__identification_division__:
                        if self.parse(PATTERN_IDENTIFICATION_DIVISION, line):
                            write_flag = True
                        if self.parse(PATTERN_ENVIRONMENT_DIVISION, line):
                            break
                    if mode == self.__environment_division__:
                        if self.parse(PATTERN_ENVIRONMENT_DIVISION, line):
                            write_flag = True
                        if self.parse(PATTERN_DATA_DIVISION, line):
                            break
                    if mode == self.__data_division__:
                        if self.parse(PATTERN_DATA_DIVISION, line):
                            write_flag = True
                        if self.parse(PATTERN_PROCEDURE_DIVISION, line):
                            break
                    if mode == self.__procedure_division__:
                        if self.parse(PATTERN_PROCEDURE_DIVISION, line):
                            write_flag = True
                    if write_flag:
                        outf.write(line)

    def parse(self, pattern, string):
        pattern = re.compile(pattern)
        if re.search(pattern, string):
            return True
        return False

    def parseII(self, pattern, string):
        pattern = re.compile(pattern)
        match = re.search(pattern, string)
        if match:
            return match
        return False
