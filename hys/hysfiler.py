#HTML_HEADER = './config/template_html_header'

def writeHtmlHeader(CONF_FILE):
    with open(CONF_FILE, 'r', encoding='utf-8') as conf_file:
        return conf_file.read()
