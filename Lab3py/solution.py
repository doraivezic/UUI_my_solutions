import sys
import math
from queue import PriorityQueue


class Node:
    def __init__(self):
        self.value = None
        self.prediction = None
        self.children = []
        self.next = None


class ID3:
    def __init__(self):
        self.header = None #prva linija iz .csv
        self.train_max_depth = None
        self.train_values = None
        self.node = None
        self.vrste_cilja = None
        self.dictionary_orig_values = None


    def print_tree(self, node, depth, ispis):

        if node.prediction:
            print(node.prediction)

        for child in node.children:
            tmp_ispis = str(depth) + ':' + node.value + '=' + child.value + ' '
            if child.prediction:
                print(ispis + tmp_ispis + child.prediction)
            else:
                self.print_tree(child.next, depth+1, ispis + tmp_ispis)

        return


    def fit(self,header, values, depth, vrste_cilja):
        self.header = header
        self.train_values = values
        self.train_max_depth = depth
        self.vrste_cilja = vrste_cilja

        if self.train_max_depth == 0:
            self.node = Node()
            predict = [0]*len(self.vrste_cilja)
            for val in values:
                predict [self.vrste_cilja.index(val[-1])] += 1
            
            max_pred = max(predict)
            for a in range(len(predict)-1,-1,-1):
                if predict[a] == max_pred:
                    self.node.prediction = self.vrste_cilja[a]
            
        
        else:
            self.node = self.id3(1, self.header[:-1], None, self.train_values)

        print("[BRANCHES]:")
        self.print_tree(self.node, 1, "")
        
        return

        
    
    def entropy(self,lista):

        if sum(lista)==0:
            return 0.0

        e = 0.0
        for el in lista:
            if el == 0:
                continue
            el = float(el)
            s = float(sum(lista))
            #e -= ( (el/s) * math.log(el/s) / math.log(2.0) )
            e -= ( (el/s) * math.log(el/s, 2) )
        return e
    
    def id3(self, depth, header, node, values):
        
        #slazem ih po stupcima
        all_categories = []
        for i in range(len(header)):
            tmp_categories = []
            for j in range(len(values)):
                tmp_categories.append(values[j][i])
            all_categories.append(tmp_categories)  # [[suncano,suncano,oblacno],[jak,jak,slab]..]

        dictionary = {} #{vrijeme: [[9,5], {suncano:[2,3], oblacno:[4,0], kisno:[3,2]}]}
        

        if not node:
            node = Node()

        
        for h in range(len(header)):
            
            entropija_znacajke = 0
            #sveukupni broj da , sveukupni broj ne
            lista_value = []
            for el in self.vrste_cilja:
                c = 0
                for v in values:
                    if v[-1] == el:
                        c += 1
                lista_value.append(c)
            dictionary[header[h]] = [lista_value]

        z_count = 0
        for z in all_categories:
            small_dict = {}
            for c in range(len(z)):
                if z[c] not in small_dict:
                    small_list = [0]* len(self.vrste_cilja)
                    small_list[self.vrste_cilja.index(values[c][-1])] +=1
                    small_dict[z[c]] = small_list
                else:
                    small_dict[z[c]][self.vrste_cilja.index(values[c][-1])] +=1
            dictionary[header[z_count]].append(small_dict)
            z_count +=1

        if not self.dictionary_orig_values:
            self.dictionary_orig_values = {**dictionary}
            #print(self.dictionary_orig_values)

        

        ig_znacajki = PriorityQueue()
        ig_znacajki2 = PriorityQueue()
        for znacajka in dictionary:
            ig = self.entropy(dictionary[znacajka][0]) #jos moram minus pojedinacne
            for categ in dictionary[znacajka][1]:
                ig -= (float(sum(dictionary[znacajka][1][categ]))/float(sum(dictionary[znacajka][0]))) * self.entropy(dictionary[znacajka][1][categ])
            #print("IG(%s)=%.4f" %(znacajka, ig))
            ig_znacajki.put((ig,znacajka))
            ig_znacajki2.put((ig,znacajka))
        
        #uzimamo max ig
        while ig_znacajki.qsize()!=0:
            ig, znacajka_koju_umecemo = ig_znacajki.get()  #ali ovo nam za C i D uzima D umjesto C

        while ig_znacajki2.qsize()!=0:
            ig2, znacajka_koju_umecemo = ig_znacajki2.get()
            if ig2 == ig:  #uzimamo C, a ne D
                break
        #print("Odabirem: ", znacajka_koju_umecemo, ig) #u stablo

    
        index_koji_gledamo = header.index(znacajka_koju_umecemo)
        header.remove(znacajka_koju_umecemo)
        node.value = znacajka_koju_umecemo

        # if znacajka_koju_umecemo=="age":
        #     print(dictionary[znacajka_koju_umecemo][1])
        # print(dictionary)

        obradene_kategorije = []
        #uzimamo SVE kategorije koje izlaze iz te nase znacajke
        for categ in dictionary[znacajka_koju_umecemo][1]:
            child = Node()
            child.value = categ  # add a branch from the node to each feature value in our feature
            node.children.append(child)  # append new child node to current node


            #ako je depth dosao do postavljenog deptha
            if depth == self.train_max_depth:
                #trazimo prediction za taj child - najzastupljeniji cilj
                #uzmemo sve valuese za npr vrijeme=suncano i gledamo cilj i uzmemo onaj naj zastupljeniji
                novi_values = []
                valu = []
                for el in values:
                    small_valu = []
                    for e in el:
                        small_valu.append(e)
                    valu.append(small_valu)
                for v in valu:
                    if v[index_koji_gledamo] == categ:
                        del v[index_koji_gledamo]
                        novi_values.append(v)
                predict = [0]*len(self.vrste_cilja)
                for val in novi_values:
                    predict [self.vrste_cilja.index(val[-1])] += 1
                
                max_pred = max(predict)
                for a in range(len(predict)-1,-1,-1):
                    if predict[a] == max_pred:
                        child.prediction = self.vrste_cilja[a]



            #je li znamo prediction ili moramo produbit stablo
            elif 0 in dictionary[znacajka_koju_umecemo][1][categ]:
                max_pred = max(dictionary[znacajka_koju_umecemo][1][categ])
                for a in range(len(dictionary[znacajka_koju_umecemo][1][categ])-1,-1,-1):
                    if dictionary[znacajka_koju_umecemo][1][categ][a] == max_pred:
                        child.prediction = self.vrste_cilja[a]
                        
            #napravi rekurziju samo ako header ima 1 ili vise elemenata
            elif len(header)==0:
                max_pred = max(dictionary[znacajka_koju_umecemo][1][categ])
                for a in range(len(dictionary[znacajka_koju_umecemo][1][categ])-1,-1,-1):
                    if dictionary[znacajka_koju_umecemo][1][categ][a] == max_pred:
                        child.prediction = self.vrste_cilja[a]

            else:  #onda ponovi postupak bez trenutnog tj produbi stablo
                #pazi da tu ne poremetis neki values ili header ili njihove odnose
                novi_values = []
                valu = []
                for el in values:
                    small_valu = []
                    for e in el:
                        small_valu.append(e)
                    valu.append(small_valu)
                for v in valu:
                    if v[index_koji_gledamo] == categ:
                        del v[index_koji_gledamo]
                        novi_values.append(v)
                child.next = self.id3(depth+1, header[:], None, novi_values[:])
        

            obradene_kategorije.append(categ) 
        #uzmi najcesci prediction tog cvora, tj uzmi onaj veci iz prve liste
        veci_index = max(dictionary[znacajka_koju_umecemo][0])
        max_index = 0
        for el in range(len(dictionary[znacajka_koju_umecemo][0])):
            if dictionary[znacajka_koju_umecemo][0][el] == veci_index:
                max_index = el
                break
        pred = self.vrste_cilja[max_index]
        for categ in self.dictionary_orig_values[znacajka_koju_umecemo][1]:
            if categ not in obradene_kategorije:
                child = Node()
                child.value = categ  
                node.children.append(child)
                child.prediction = pred
                   

        return node

        

    def find_prediction(self, v):
        node = self.node
        while True:
            if node.prediction:
                return node.prediction
            index_of_v = self.header.index(node.value)
            found = False
            for child in node.children:
                if child.value == v[index_of_v]:
                    found = True
                    if child.prediction:
                        return child.prediction
                    else:
                        node = child.next
                        break
            if not found:
                return self.vrste_cilja[0]


    def predict(self, values):

        ispis = "[PREDICTIONS]:"
        correct = 0

        broj = len(self.vrste_cilja)
        confusion_matrix = [[0 for j in range(broj)]for i in range(broj)]
        
        for v in values:
            prediction = self.find_prediction(v)
            ispis += " " + prediction
            if prediction == v[-1]:
                correct += 1
            
                index_cilja = self.vrste_cilja.index(prediction)
                confusion_matrix[index_cilja][index_cilja] += 1
            else:
                index_real = self.vrste_cilja.index(v[-1])
                index_prediction = self.vrste_cilja.index(prediction)
                confusion_matrix[index_real][index_prediction] += 1
        
        print(ispis)

        result = float(correct)/float(len(values))
        print("[ACCURACY]: %.5f" % result)

        print("[CONFUSION_MATRIX]:")
        conf_m_ispis = ""
        for red in confusion_matrix:
            for stupac in red:
                conf_m_ispis += str(stupac) + " "
            conf_m_ispis = conf_m_ispis[:-1] + '\n'
        print(conf_m_ispis[:-1])


        return





if __name__ == "__main__":
    

    if len(sys.argv)<2:
        sys.exit(0)

    train_dataset = sys.argv[1]
    test_dataset = sys.argv[2]

    if len(sys.argv)>3:
        depth = int(sys.argv[3])
    else:
        depth = None


    #fitting the model
    o = open(train_dataset, 'r')
    lines = o.readlines()
    o.close()

    if len(lines)==0:
        sys.exit()

    values = []
    for i in range(len(lines)):
        if i==0:
            header = lines[i].rstrip().split(",")
        else:
            values.append(lines[i].rstrip().split(","))
        
    vrste_cilja = set()
    for v in values:
        vrste_cilja.add(v[-1])
    vrste_cilja = sorted(list(vrste_cilja))
    
    model = ID3()
    
    model.fit(header, values, depth, vrste_cilja)


    #predicting using the model
    o = open(test_dataset, 'r')
    lines = o.readlines()
    o.close()

    values = []
    for i in range(len(lines)):
        if i!=0:
            values.append(lines[i].rstrip().split(","))
        
    predictions = model.predict(values)
