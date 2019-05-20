def handle_file(file, outfile):
    with open(file, 'r') as in_file:
        for line in in_file:
            if 'from .' in line:
                continue
            else:
                outfile.write(line)
        outfile.write('\n')


with open('./script.py', 'w') as outfile:
    models = ['position', 'cell', 'unit', 'building', 'map', 'environment']
    for model in models:
        handle_file('model/' + model + '.py', outfile)

    agents = ['random_agent', 'wood_2_agent']
    for agent in agents:
        handle_file('agents/' + agent + '.py', outfile)

    handle_file('./a_code_of_ice_and_fire.py', outfile)
