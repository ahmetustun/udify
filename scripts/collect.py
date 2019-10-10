import os

cmd = 'curl https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-2988/ud-treebanks-v2.4.tgz  | tar xvz'

os.system(cmd)

for dataset in ["UD_Arabic-PADT" ,"UD_Basque-BDT" ,"UD_Chinese-GSD" ,"UD_English-EWT" ,"UD_Finnish-TDT" ,"UD_Hebrew-HTB" ,"UD_Hindi-HDTB" ,"UD_Italian-ISDT" ,"UD_Japanese-GSD" ,"UD_Korean-GSD" ,"UD_Russian-SynTagRus" ,"UD_Swedish-Talbanken" ,"UD_Turkish-IMST"]:
    cmd = 'mv ud-treebanks-v2.4/' + dataset + ' data/'
    os.system(cmd)

