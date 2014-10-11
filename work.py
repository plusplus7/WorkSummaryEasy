import json
from datetime import date

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

def show_info(message):
    print message,

def get_user_confirm():
    strs=raw_input()
    return strs[0] == 'y' or strs[0] == 'Y'

def load_summary_style():
    global g_summary_style
    
    fp=0
    try:
        fp = open("summary_style.conf", "r")
    except:
        return 7404
    
    style_text = fp.read()
    try:
        g_summary_style = json.loads(style_text)
    except:
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

def main():
    global g_summary_style

    status = load_summary_style()
    if status != 7200:
        show_info("Load summary style file failed: %s" % ErrorCodeDict[status])
        return -1

    show_info("Need to set the date of summary?[y/n]")
    summary_date=date.today()
    if get_user_confirm() == True:
        summary_date=get_user_date()

    if summary_date == 7403:
        show_info("Wrong date: %s" % ErrorCodeDict[summary_date])
        return -1
    for k in g_summary_style["content"]:
        print k

if __name__ == "__main__":
    main()
