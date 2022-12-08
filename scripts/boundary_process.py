import os, glob

if __name__ == '__main__':
    txt_list = glob.glob("/mnt/e/new/labels/*/*.txt")
    for txt_item in txt_list:
        with open(txt_item) as f:
            lines = f.readlines()
        with open(txt_item, 'w') as f:
            for line in lines:
                line_split = line.strip().split()
                
                len_list = len(line_split)
                i = 1
                splitstr = line_split[0]
                while i < len_list:
                    if float(line_split[i]) > 1.0:
                        line_split[i] = '1.0'
                    elif float(line_split[i]) < 0.0:
                        line_split[i] = '0.0'
                    splitstr = splitstr  + ' ' + line_split[i]

                    i += 1
                
                f.write(splitstr + '\n')
        pass

