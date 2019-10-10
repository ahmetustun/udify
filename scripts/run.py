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

counter = 0
for dataDir in os.listdir('data'):
    if not dataDir.startswith('UD'):
        continue
    train, dev, test = getTrainDevTest('data/' + dataDir)
    for setting in ['base', 'bert']:
        configPath = 'config/multi-team/' + setting + '.' + dataDir + '.json'
        
        cmd = 'cp config/multi-team/' + setting + '.json ' + configPath
        os.system(cmd)

        cmd = 'sed -i \'s;.*train_data_path.*;  "train_data_path": "' + train + '",;g\' ' + configPath
        os.system(cmd)

        cmd = 'sed -i \'s;.*validation_data_path.*;  "validation_data_path": "' + dev + '",;g\' ' + configPath
        os.system(cmd)

        cmd = 'sed -i \'s;.*test_data_path.*;  "test_data_path": "' + test + '",;g\' ' + configPath
        os.system(cmd)

        if counter < 13:
            cmd = 'python3 train.py --device 1 --base_config ' + configPath
        else:
            cmd = 'python3 train.py --device 0 --base_config ' + configPath
        print(cmd)
        counter += 1
