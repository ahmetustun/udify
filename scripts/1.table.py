import os
import json

warmup = {'UD_Arabic-PADT':380, 'UD_Basque-BDT':340, 'UD_Chinese-GSD':250, 'UD_English-EWT':785, 'UD_Finnish-TDT':765, 'UD_Hebrew-HTB':330, 'UD_Hindi-HDTB':835, 'UD_Italian-ISDT':825, 'UD_Japanese-GSD':450, 'UD_Korean-GSD':275, 'UD_Russian-SynTagRus':3055, 'UD_Swedish-Talbanken':270, 'UD_Turkish-IMST':230}

def json2scores(path):
    if not os.path.isfile(path):
        print('not found: ' + path)
        return [0.0,0.0,0.0,0.0]
    data = json.load(open(path, 'r'))
    return [data['UPOS']['f1'], data['UFeats']['f1'], data['Lemmas']['f1'], data['LAS']['f1']]
    
def getSetting(path):
    data = json.load(open(path, 'r'))
    return str(data['dataset_reader']['depConvStrategy'])

def convDataname(dataset):
    for conlFile in os.listdir('data/' + dataset):
        if conlFile.endswith('.conllu'):
            return conlFile[:conlFile.find('-')]
    return ''

def findScores(dataset, setting):
    if setting == 'old':
        dataDir = 'logs/baseline/udify.single.' + convDataname(dataset) + '/'
        for folder in os.listdir(dataDir):
            if os.path.isfile(dataDir + folder + '/dev_results.json'):
                return json2scores(dataDir + folder + '/dev_results.json')
        return [0.0,0.0,0.0,0.0]     
    dataDir = 'logs/bert_full_config.' + dataset + '/'
    for folder in os.listdir(dataDir):
        if os.path.isfile(dataDir + folder + '/dev.conllu'):
            if getSetting(dataDir + folder + '/config.json') == setting:
                return json2scores(dataDir + folder + '/dev_results.json')
    return [0.0,0.0,0.0,0.0]

settings = ['old', '1', '2', '3']
allResults = {}
for dataset in warmup:
    results = []
    for setting in settings:
        results.append(findScores(dataset, setting))
    allResults[dataset] = results
    #print(' & '.join([dataset] + results) + '\\\\')
    
tasks = ['UPOS', 'MorphFeats', 'Lemmas', 'LAS']
for settingIdx, setting in enumerate(settings):
    print(setting, '\\\\')
    print('\\begin{tabular}{l r r r r}')
    for dataset in sorted(allResults):
        newList = [dataset.replace('_', '\\_')]
        for item in allResults[dataset][settingIdx]:
            #TODO fix
            newList.append(str(item*100)[:5])
        print(' & '.join( newList) + '\\\\')
    print('\\end{tabular}\n')
    
