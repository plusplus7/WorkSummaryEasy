# -*- coding: utf-8 -*- 
import re
import json
from datetime import date
import sys;
reload(sys);
sys.setdefaultencoding("utf8")

ErrorCodeDict={
    7200 : "Success",
    7401 : "User Exit",
    7402 : "Process Failed",
    7403 : "Format Error",
    7404 : "Not Exist",
    7405 : "Important parameter missed",
    7500 : "Interal Error",

}
g_summary_style = {}
g_contents=[]

def show_info(message):
    sys.stdout.write(message)
def get_user_confirm(info):
    show_info(info)
    strs=raw_input()
    return len(strs) > 0 and (strs[0] == 'y' or strs[0] == 'Y')

def load_summary_style():
    global g_summary_style
    
    fp=0
    try:
        fp = open("summary_style_conf.json", "r")
    except:
        return 7404
    
    style_text = fp.read()
    try:
        g_summary_style = json.loads(style_text)
    except:
        return 7403

    if g_summary_style.has_key("Configure") == False or\
       g_summary_style.has_key("Content") == False or\
       g_summary_style.has_key("Filename") == False:
       show_info("No `Content` or `Configure` or `Filename` found in summary_style_conf.json\n")
       return 7403

    return 7200

def get_user_date():
    year=0
    month=0
    day=0
   
    show_info("Input year:")
    try:
        year=int(raw_input())
    except:
        return 7403

    show_info("Input month:")
    try:
        month=int(raw_input())
    except:
        return 7403
    
    show_info("Input day:")
    try:
        day=int(raw_input())
    except:
        return 7403
    
    return date(year, month, day)

def get_contents(contents):
    strs=""
    for i in contents:
        strs=strs+i+"\n\n"
    return strs

def show_preview():
    show_info("\033[1000A"+get_contents(g_contents))

def clean_screen():
    show_info("\033[2J")
def main():
    global g_summary_style

    status = load_summary_style()
    if status != 7200:
        show_info("Load summary style file failed: %s\n" % ErrorCodeDict[status])
        return -1

    summary_date=date.today()
    if get_user_confirm("Need to set the date of summary?[y/n]") == True:
        summary_date=get_user_date()

    if summary_date == 7403:
        show_info("Wrong date: %s\n" % ErrorCodeDict[summary_date])
        return -1

    configure=g_summary_style["Configure"]
    for k in g_summary_style["Content"]:
        data_name=k.keys()[0]
        
        if k[data_name].has_key("Format") == False:
            show_info("No `Format` element found in `%s`\n" % data_name)
            return -1

        data_format=k[data_name]["Format"]
        if "%" in data_format:
            data_format=summary_date.strftime(data_format)
        data_content=""
        if configure.has_key("PrefixSpecialChar"):
            for psc_key in configure["PrefixSpecialChar"].keys():
                if k[data_name].has_key(psc_key) == True:
                    for i in range(k[data_name][psc_key]):
                        data_content=data_content+configure["PrefixSpecialChar"][psc_key]
                    data_content=data_content+" "
        while True:
            clean_screen()
            show_preview()
            if "$" in data_format:
                p=re.compile("(\$[a-z0-9A-Z_]*\$)")
                m_groups=p.findall(data_format)
                t_data_format=data_format
                
                for i in m_groups:
                    show_info("Input content of parameter `%s`:\n" % i[1:-1])
                    input=raw_input()
                    t_data_format=t_data_format.replace(i,input)
                print data_content
                g_contents.append(data_content+"%s" % t_data_format)

            else:
                g_contents.append(data_content+"%s" % data_format)
                break

            if k[data_name].has_key("IsPlural"):
                if get_user_confirm("Add one more?[y/n]") == True:
                    continue
                else:
                    break
    clean_screen()
    show_preview()
    if get_user_confirm("Save it?[y/n]") == True:
        fp=open(summary_date.strftime(g_summary_style["Filename"]["Format"]), "w")
        fp.write(get_contents(g_contents))
        fp.close()

if __name__ == "__main__":
    main()
