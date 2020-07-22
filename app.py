#!/usr/bin/env python3
import xxhash

import os
from flask import Flask, redirect
from flask import request
from flask import jsonify
#print(xxhash.xxh64('xxhash').hexdigest())
#print(xxhash.xxh64('xxhash', seed=20141025).hexdigest())

app = Flask(__name__)

key = "default"
split = 4
numMaxT = 10000000
version = "1.0"

def intKey():
    global key
    return int(xxhash.xxh64('xxhash').intdigest() / 40000000)
#print(intKey())
def final(comp):
    return int( (int(comp) - int(intKey())) )
def finalReverse(comp):
    return int(comp) + int(intKey())
def sep(pro):
    global key
    pro2 = pro + len(key)
    return str(pro2*3) + str(pro*24) + str(pro*4)
def numfind(targ):
    global key
    i = 0#30386530
    done = False
    while done == False:
        has = xxhash.xxh64(key, seed=i).intdigest()
    #    print(has)
        if(str(has)[:].startswith(str(targ))):
#            print(str(has))
            has2 = str(has).replace("\\","").replace("'","")[:]
#            print(has2)
#            print(i)
            done = True
            return i
        elif i > numMaxT:
            done = True
            return 0
        i = i + 1
def find(targ):
    global key
    i = 0#30386530
    done = False
    while done == False:
        has = xxhash.xxh64(key, seed=i).digest()
    #    print(has)
        if(str(has)[2:].startswith(str(targ))):
#            print(str(has))
            has2 = str(has).replace("\\","").replace("","")[2:]
#            print(has2)
#            print(i)
            done = True
            return i
        elif i > numMaxT:
            done = True
            return i
        i = i + 1
def decode(seedA, place):
    global key
    return str(xxhash.xxh64(key, seed= int(seedA/place) ).digest()).replace("\\","").replace("","")[2:]
def percentage(part, whole):
  return 100 * float(part)/float(whole)
def progress(a, p, cust="                       "):
    per = int(percentage(p, a) / 10)
    nf = "_"*(10-per)
    f = "|"*per
    d = " " + str(p) + " / " + str(a) + ", " + str(percentage(p, a)) + "%"
    print(f + nf + d + cust,end="\r")
def numprocess(inp):
    global split
    line = inp.replace(" ", "<").replace("'",">").replace("?","_").replace("…","...").replace("'","|")
    n = split
    ns = int(n/2)
    code = ""#sep(1)
    i = 1
    parts = [line[i:i+n] for i in range(0, len(line), n)]
    for part in parts:
#        if len(part) < 2
#        print(part)
        sepa = sep(i)
        f = str(numfind(part))
        if len(f) < n:
            code = code + f + "-"
        elif f[-1] != "0":
            f1 = str(numfind(f[ns:]))
            f2 = str(numfind(f[:ns]))
            print(f1)
            print(f2)
            code = code + f1 + "_" + f2 + "-"
        else:
            code = code + f + "-"
        progress(len(parts), i)
        i = i + 1
    print()
#    print(code)
    print("Raw: " + str(code) )
    return str(code)
def process(inp):
    line = inp.replace(" ", "<").replace("'",">").replace("?","_").replace("…","...").replace("'","|")
    n = 2
    code = ""#sep(1)
    i = 1
    parts = [line[i:i+n] for i in range(0, len(line), n)]
    for part in parts:
#        if len(part) < 2
#        print(part)
        sepa = sep(i)
        code = code + str(find(part)*i) + sepa
        progress(len(parts), i)
        i = i + 1
    print()
#    print(code)
    print("Raw: " + str(code) )
#    print("Compressed: " + str(numprocess(code)) )
    return str(final(code))
def deProcess(inp):
    whole = ""
    i = 1
    done = False
    p = str(int(finalReverse(inp)))
    while done == False:
        sepa = sep(i)
#        print("Left: " + p)
#        print(sepa + ": ",end="")
        v = p.replace(sepa,"")
        if v != p:
            orig = p.split(sepa)[0]
            v = orig.replace(sepa, "")
#            print(v)
            if v != "":
                whole = whole + (decode(int(v),i)[:2] ).replace("<"," ").replace(">","'").replace("_","?").replace("|","'")
#                p.replace(orig,"")
                p = p.split(orig + sepa)[1].replace(sepa,"")
                i = i + 1
            else:
                i = i + 1
                p = p.split(orig + sepa)[1].replace(sepa,"")
        else:
            done = False
            break
#    print(whole)
    print()
    return whole
#msg = "hi!"
#eProcess(process("Hello world!"))
#ida = find(msg)
#print(decode(ida)[:2])

def ask():
    global key
    k = input("Key (Press enter to skip): ")
    if k != "":
        key = k
    i = input("Decrypt or Encrypt? d/e: ")
    if i == "e":
        msg = input("Message: ")
        to = process(msg)
        print("Encoded: " + to)
        print("Will produce: " + deProcess(to))
    elif i == "d":
        msg = input("Encoded Message: ")
        print("Trying to un-encode...")
        print(deProcess(msg))
    elif i == "k":
        for i in range(10):
            print(sep(i))
    elif i == "n":
        numprocess(input("To find: "))
    elif i == "nt":
        sz = int(input("Max: "))
        ran = int(input("Iterations: "))
        avgl = 0
        s = 0
        from random import randint
        for i in range(ran):
            n = randint(1, int("9"*sz))
            r = 1000000000000
            r = numfind(n)
            if len(str(r)) > sz:
                m = int( len(str(r)) / 2)
                r2 = str(numfind(n))[1:]
                r1 = str(numfind(n))[:1]
                s = s + len(str(r1))
                avgl = avgl + 1
                s = s + len(str(r2))
                avgl = avgl + 1
            else:
#            print(r)
                s = s + len(str(r))
                avgl = avgl + 1
            progress(ran, i, " | avg: " + str(s/avgl) + "                ")
        print("Average with size of " + str(sz) + ": " + str(s/avgl) + " | avg. compression of " + str(sz-(s/avgl)) + " letters                              ")
    else:
        print("That's not a valid answer, let's try again.")
        ask()

#    ask()


#Flask code
@app.route('/')
def hello():
    view = "<title>Contemplation</title>"
    view = view + "<h3> Hash-Reversal encoder-decoder \"Contemplation\"</h3>"
    view = view + "<br \\>-----------------------------------------------------------------------<br \\>"
    view = view + "<h4>Encode</h4>"
    view = view + "<form action=\" " + "/enc" + "\" method=\"post\">"
    view = view + "<input type=\"text\" name=\"msg\">"
    view = view + "<input type=\"submit\">"
    view = view + "</form>"
    
    view = view + "<h4>Decode</h4>"
    view = view + "<form action=\" " + "/dec" + "\" method=\"post\">"
    view = view + "<input type=\"text\" name=\"msg\">"
    view = view + "<input type=\"submit\">"
    view = view + "</form>"

    view = view + "<br \\>-----------------------------------------------------------------------<br \\>"
    
    view = view + "<br \\><hr \\>"
    view = view + "Contemplation v. " + str(version) + " | <a href=\"https://raw.githubusercontent.com/jonnelafin/A-/master/LICENSE\">LICENSE</a>"
    return view
@app.route('/enc', methods=['POST'])
def handle_data():
    msg = request.form['msg']
    view = ""
    
    to = process(msg)
    print("Encoded: " + to)
    view = view + "<br \\>"
    view = view + "Encoded: " + "<br \\>" + to
    view = view + "<br \\>"
    by = deProcess(to)
    print("Will produce: " + by)
    view = view + "Will produce: " + "<br \\>" + by
    view = view + "<br \\>"
    return view
#    return redirect("/", code=302)
@app.route('/dec', methods=['POST'])
def handle_data2():
    msg = request.form['msg']
    view = ""
    
    by = deProcess(msg)
    print("Decoded: " + by)
    view = view + "Decoded: " + "<br \\>" + by
    view = view + "<br \\>"
    return view
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
