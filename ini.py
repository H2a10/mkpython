import configparser as c,sys,os,shutil as s,json,sets
__all__=["mkmkf"]
def read(file):
    cp=c.ConfigParser()#interpolation=c.ExtendedInterpolation)
    cp.read(file,encoding="utf-8")
    l={}
    for section in cp:
        #print(section)
        try:
            l[section]=cp[section]["depends"].split(" ")
        except:
            pass
    
    return l,dict(cp["PROJCONF"])
def mkmkfemb(lc):
    l=lc[0]
    c=lc[1]
    inc=sets.include
    link=sets.libemb
    out=f"""#autogen by ini.py mode emb
CXO=clang++ -c {inc}
CCO=clang -c {inc}
C=clang {link}
CXX=clang++ {link}
SHELL="/bin/bash"
    """
    for x in l:
        #print(x)
        if x.endswith(".c"):
            out+=("\n"+os.path.splitext(x)[0]+".o")
            out+=(f": {x} {' '.join(l[x])}")
            out+=("\n\t${CCO} "+x)
        if x.endswith(".cpp"):
            out+=("\n"+os.path.splitext(x)[0]+".o")
            out+=(f": {x} {' '.join(l[x])}")
            out+=("\n\t${CXO} "+x)
    a=[os.path.splitext(x)[0]+".o" for x in l]
    out+=("\nmain: "+" ".join(a))
    out+="\n\t${CXX}"+f" -o {c['name']} "+" ".join(a)
    out+="\n.DEFAULT_GOAL := main\n.PHONY: main"
    #print(out)
    return out
def mkmkfext(lc):
    l=lc[0]
    c=lc[1]
    inc=sets.include
    link=""
    out=f"""#autogen by ini.py mode ext
CXO=clang++ -c {inc}
CCO=clang -c {inc}
C=clang -bundle -undefined dynamic_lookup {link}
CXX=clang++ -bundle -undefined dynamic_lookup {link}
SHELL="/bin/bash"
    """
    for x in l:
        #print(x)
        if x.endswith(".c"):
            out+=("\n"+os.path.splitext(x)[0]+".o")
            out+=(f": {x} {' '.join(l[x])}")
            out+=("\n\t${CCO} "+x)
        if x.endswith(".cpp"):
            out+=("\n"+os.path.splitext(x)[0]+".o")
            out+=(f": {x} {' '.join(l[x])}")
            out+=("\n\t${CXO} "+x)
    a=[os.path.splitext(x)[0]+".o" for x in l]
    out+=("\nmain: "+" ".join(a))
    out+="\n\t${CXX}"+f" -o {c['name']}.so "+" ".join(a)
    out+="\n.DEFAULT_GOAL := main\n.PHONY: main"
    #print(out)
    return out
def mkmkf(filename,dest,name):
    r=read(filename)
    if r[1]["type"] not in ["ext","emb"]:
        raise ValueError("invalid data")
    if r[1]["type"]=="ext":
        mkf=mkmkfext(r)
    else:
        mkf=mkmkfemb(r)
    try:
        os.mkdir(dest:=os.path.expanduser(dest))
    except:
        pass
    os.mkdir(proj_dir:=os.path.join(dest,name))
    with open(os.path.join(proj_dir,"Makefile"),"w") as m:
        m.write(mkf)
    dt=f"""{
    "git.ignoreLimitWarning": true,
    "C_Cpp.default.intelliSenseMode": "clang-x64",
    "C_Cpp.default.includePath": [
        "{sets.includeD}"
    ],
    "outname":"NAME"
}"""
    s.copy(filename,os.path.join(proj_dir,filename))
    for x in r[0]:
        s.copy(x,os.path.join(proj_dir,x))
        for y in r[0][x]:
            if not y:
                continue
            #print(y,os.path.join(proj_dir,y))
    os.mkdir(vs:=os.path.join(proj_dir,".vsocde"))
    with open(os.path.join(vs,"settings.json"),"w") as m:
        m.write(dt.replace("NAME",r[1]["name"]))
    