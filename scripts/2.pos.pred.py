import os
import json

warmup = {'UD_Arabic-PADT':380, 'UD_Basque-BDT':340, 'UD_Chinese-GSD':250, 'UD_English-EWT':785, 'UD_Finnish-TDT':765, 'UD_Hebrew-HTB':330, 'UD_Hindi-HDTB':835, 'UD_Italian-ISDT':825, 'UD_Japanese-GSD':450, 'UD_Korean-GSD':275, 'UD_Russian-SynTagRus':3055, 'UD_Swedish-Talbanken':270, 'UD_Turkish-IMST':230}

def getSetting(path):
    data = json.load(open(path, 'r'))
    return str(data['dataset_reader']['depConvStrategy'])

def getDev(dataset):
    for conlFile in os.listdir('data/' + dataset):
        if conlFile.endswith('dev.conllu'):
            return 'data/' + dataset + '/' + conlFile

def pred(path, dataset):
    cmd = 'python3 predict.py ' + path + '/model.tar.gz ' + getDev(dataset) + ' ' + path + '/dev.conllu --eval_file ' + path + '/dev_results.json'
    print(cmd)

for dataset in warmup:
    dataDir = 'logs/bert_full_config.' + dataset + '/'
    for folder in os.listdir(dataDir):
        if os.path.isfile(dataDir + folder + '/model.tar.gz'):
            if getSetting(dataDir + folder + '/config.json') == '3':
                pred(dataDir + folder, dataset)

