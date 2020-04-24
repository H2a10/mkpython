import sysconfig as c
include=c.get_config_var("INCLUDEPY")
libemb=c.get_config_var("LIBDIR")
link=c.get_config_var("PYTHON_FOR_REGEN")
includeD=include
include="-I "+include
libemb="-L "+libemb
link="-l"+link
libemb+=" "
libemb+=link
del link

if __name__=="__main__":
    print(libemb)
