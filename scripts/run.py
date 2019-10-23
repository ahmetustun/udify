import os

def getTrainDevTest(path):
    train = ''
    dev = ''
    test = ''
    for conlFile in os.listdir(path):
        if conlFile.endswith('conllu'):
            if 'train' in conlFile:
                train = path + '/' + conlFile
            if 'dev' in conlFile:
                dev = path + '/' + conlFile
            if 'test' in conlFile:
                test = path + '/' + conlFile
    return train, dev, test

#Potentially dangerous, does not take structure into accoutn
# Simply replace first occurence of the key, you can circumvent some of this
# by also matching with the previous value
def setVal(configPath, key, newVal, oldVal=''):
    found = False
    lines = open(configPath).readlines()
    for lineIdx in range(len(lines)):
        if key in lines[lineIdx]:
            tok = lines[lineIdx][:-1].split('"')

            # extract old value
            if len(tok) == 5:
                valIdx = 3
                val = tok[3]
            elif len(tok) == 3:
                val = tok[2].replace(',', '').replace(':', '').strip()
            
            # only replace when the oldvalue is equal to the setting
            if oldVal != '' and oldVal != val:
                continue

            # place new value in the string            
            if len(tok) == 5:
                tok[3] = newVal
            elif len(tok) == 3:
                tok[2] = ': ' + newVal + ','
            lines[lineIdx] = '"'.join(tok) + '\n'
            found = True
            break
    if not found:
        print('ERR: ' + key + ' not found in ' + configPath + ' ' + oldVal)
    outFile = open(configPath, 'w')
    for line in lines:
        outFile.write(line)
    outFile.close()


warmup = {'UD_Arabic-PADT':380, 'UD_Basque-BDT':340, 'UD_Chinese-GSD':250, 'UD_English-EWT':785, 'UD_Finnish-TDT':765, 'UD_Hebrew-HTB':330, 'UD_Hindi-HDTB':835, 'UD_Italian-ISDT':825, 'UD_Japanese-GSD':450, 'UD_Korean-GSD':275, 'UD_Russian-SynTagRus':3055, 'UD_Swedish-Talbanken':270, 'UD_Turkish-IMST':230}

counter = 0
for dataDir in os.listdir('data'):
    if not dataDir.startswith('UD'):
        continue
    train, dev, test = getTrainDevTest('data/' + dataDir)
    #for setting in ['base', 'bert', 'base_w_bert']:
    for setting in ['bert_full_config']:#base', 'bert', 'base_w_bert']:
        configPath = 'config/multi-team/' + setting + '.' + dataDir + '.json'
        
        cmd = 'cp config/multi-team/' + setting + '.json ' + configPath
        os.system(cmd)

        setVal(configPath, 'train_data_path', train)
        setVal(configPath, 'validation_data_path', dev)
        setVal(configPath, 'test_data_path', test)

        # nice deep path, as code required to write to a directory called vocabulary?
        setVal(configPath, 'directory_path', 'data/vocab/' + dataDir + '.' + setting + '/vocabulary' )

        # used in original udify code
        setVal(configPath, 'warmup_steps', str(warmup[dataDir]))
        setVal(configPath, 'start_step', str(warmup[dataDir]))

        if setting == 'base' or setting == 'base_w_bert':
            lang = train.split('/')[-1][:2]
            if not os.path.isfile('data/polyglot/' + lang + '.txt'):
                print('No embeddings for: ' , lang, train)
            setVal(configPath, 'pretrained_file', 'data/polyglot/' + lang + '.txt')
            # set the embeddings size to polyglot sized embeddings
            setVal(configPath, 'embedding_dim', '64', oldVal='100')
            # also adjust input_size accordingly
            if setting == 'base':
                setVal(configPath, 'input_size', '320', oldVal='356')
            elif setting == 'base_w_bert':
                setVal(configPath, 'input_size', '1088', oldVal='1124')

        for depConv in ['1','2','3']:
            if counter < 20:
                cmd = 'python3 train.py --device 1 --base_config ' + configPath + ' --depConv ' + depConv
            else:
                cmd = 'python3 train.py --device 0 --base_config ' + configPath + ' --depConv ' + depConv
            cmd += ' --name ' + setting + '.' + dataDir
            print(cmd)
            counter += 1

