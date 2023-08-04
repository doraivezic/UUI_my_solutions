import sys
from queue import PriorityQueue

def astar(pocetno, ciljno, prijelazi, heuristike):
    found_solution = "no"
    path_length = 0
    path = []

    gradovi= {}
    grad_index = 0
    for key in prijelazi:
        gradovi[key] = grad_index
        grad_index += 1
        
    lista_open = PriorityQueue()
    lista_open.put((0, 0, pocetno, path))
    #lista_open = [(0, 0, pocetno, path)]  #heur+prava_cijena, prava cijena, ime, put
    closed = {}
    #closed_set = set([]) #set

    while lista_open.qsize()!=0:
        heuristic_length, cost, state, path = lista_open.get()

        if state not in closed:
            closed[state] = cost
        # else:
        #     if closed[state] > cost:
        #         closed[state] = cost
        #     else:

        #print(state)
        if state in ciljno:
            found_solution = "yes"
            path_length = len(path)+1 #+ciljno
            break

        
        for el in prijelazi[state]:
            el_list = el.split(',')
            el = el_list[0]
            el_price = el_list[1]
            if el in closed:
                continue
                # if float(el_price) >= float(closed[el]):
                #     del closed[el]
                #     continue

            heur_el = float(heuristike[el])
            #nova_stanja.append((cost+int(el_price)+heur_el, cost+int(el_price), el, path + [gradovi[state]]))
            lista_open.put((cost+float(el_price)+heur_el, cost+float(el_price), el, path + [gradovi[state]]))


        # nova_stanja.sort(reverse = False)
        # lista_open.extend(nova_stanja)
        # lista_open.sort(reverse=False)

        #print(lista_open)

        
        
        
    final_path = []
    for el in path:
        final_path.append(list(gradovi.keys())[list(gradovi.values()).index(el)])
    final_path.append(state)

    

    print("[FOUND_SOLUTION]: %s" % found_solution)
    if found_solution == "yes":
        print("[STATES_VISITED]: %d" % len(closed))
        print("[PATH_LENGTH]: %d" % path_length)
        print("[TOTAL_COST]: %.1f" % cost)
        print("[PATH]: %s" % " => ".join(final_path))
    return



def bfs(pocetno, ciljno, prijelazi):
    found_solution = "no"
    path_length = 0
    path = []

    gradovi= {}
    grad_index = 0
    for key in prijelazi:
        gradovi[key] = grad_index
        grad_index += 1
    #print(gradovi)
        

    lista_open = [(pocetno, path, 0)]  #lista puna tupli
    closed = set([]) #set
    
    while len(lista_open)!=0:
        state, path, cost = lista_open[0]
        closed.add(state)
        lista_open.pop(0)

        if state in ciljno:
            found_solution = "yes"
            path_length = len(path)+1 #+ciljno
            break

        nova_stanja = []
        
        for el in prijelazi[state]:
            el_cost = el.split(',')[1]
            el = el.split(',')[0]
            if el in closed:
                continue
            nova_stanja.append((el, path + [gradovi[state]], cost+float(el_cost)))

        #print(state, nova_stanja)
        nova_stanja.sort(reverse = False)
        lista_open.extend(nova_stanja)
        #lista_open.sort(reverse = False)

        

        
        
    final_path = []
    for el in path:
        final_path.append(list(gradovi.keys())[list(gradovi.values()).index(el)])
    final_path.append(state)
    
    print("[FOUND_SOLUTION]: %s" % found_solution)
    if found_solution == "yes":
        print("[STATES_VISITED]: %d" % len(closed))
        print("[PATH_LENGTH]: %d" % path_length)
        print("[TOTAL_COST]: %.1f" % cost)
        print("[PATH]: %s" % " => ".join(final_path))
    return





def ucs(pocetno, ciljno, prijelazi):
    found_solution = "no"
    path = []


    gradovi= {}
    grad_index = 0
    for key in prijelazi:
        gradovi[key] = grad_index
        grad_index += 1
        

    lista_open = PriorityQueue()
    lista_open.put((0, pocetno, path))
    #lista_open = [(0, pocetno, path)]  #lista puna tupli
    closed = set([]) #set

    #while len(lista_open)!=0:
    while lista_open.qsize()!=0:
        cost, state, path = lista_open.get()
        closed.add(state)
        #lista_open.pop(0)

        if state in ciljno:
            found_solution = "yes"
            path_length = len(path)+1 #+ciljno
            break

        #nova_stanja = []
        
        for el in prijelazi[state]:
            el_list = el.split(',')
            el = el_list[0]
            el_price = el_list[1]
            if el in closed:
                continue
            #nova_stanja.append((cost+int(el_price), el, path + [gradovi[state]]))
            lista_open.put((cost+float(el_price), el, path + [gradovi[state]]))

        # nova_stanja.sort(reverse = False)
        # lista_open.extend(nova_stanja)
        # lista_open.sort(reverse = False)

        
        
        
    final_path = []
    for el in path:
        final_path.append(list(gradovi.keys())[list(gradovi.values()).index(el)])
    final_path.append(state)

    

    print("[FOUND_SOLUTION]: %s" % found_solution)
    if found_solution == "yes":
        print("[STATES_VISITED]: %d" % len(closed))
        print("[PATH_LENGTH]: %d" % path_length)
        print("[TOTAL_COST]: %.1f" % cost)
        print("[PATH]: %s" % " => ".join(final_path))
    return




def optimisticnost(pocetno, ciljna, prijelazi, heur):
    optimistic = True

    # gradovi= {}
    # grad_index = 0
    # for key in prijelazi:
    #     gradovi[key] = grad_index
    #     grad_index += 1

    obidena_stanja = []

    for key in prijelazi:
        # if key in ciljna:
        #     continue
        if key in obidena_stanja:
            continue

        pocetno = key
        
        lista_open = PriorityQueue()
        lista_open.put((0, pocetno, [pocetno], [0]))
        #lista_open = [(0, pocetno, path)]  #lista puna tupli
        closed = set([]) #set

        #while len(lista_open)!=0:
        while lista_open.qsize()!=0:
            cost, state, path, path_costs = lista_open.get()
            closed.add(state)
            #lista_open.pop(0)

            if state in ciljna:
                # found_solution = "yes"
                # path_length = len(path)+1 #+ciljno
                break

            #nova_stanja = []
            
            for el in prijelazi[state]:
                el_list = el.split(',')
                el = el_list[0]
                el_price = el_list[1]
                if el in closed:
                    continue
                #nova_stanja.append((cost+int(el_price), el, path + [gradovi[state]]))
                lista_open.put((cost+float(el_price), el, path + [el], path_costs + [cost+float(el_price)]))

        final_cost = cost
        

        for i in range(0,len(path)):
            pocetno = path[i]
            cost = path_costs[i]
            pocetno_cost = final_cost-cost
            
            if pocetno not in obidena_stanja:
                ispis = "[CONDITION]: "
                if pocetno_cost < float(heur[pocetno]):
                    ispis += "[ERR] h(%s) <= h*: %.1f <= %.1f" % (pocetno, float(heur[pocetno]), pocetno_cost)
                    optimistic = False
                else:
                    ispis += "[OK] h(%s) <= h*: %.1f <= %.1f" % (pocetno, float(heur[pocetno]), pocetno_cost)
                print(ispis)

            obidena_stanja.append(pocetno)


    ispis = "[CONCLUSION]: "
    if optimistic:
        ispis += "Heuristic is optimistic."
    else:
        ispis += "Heuristic is not optimistic."
    print(ispis)


    return




def konzistentnost(pocetno, ciljna, prijelazi, heur):
    consistent = True

    for key in prijelazi:
        pocetno = key
        
        #lista_open = [(pocetno, 0)]  #lista puna tupli

        for el in prijelazi[pocetno]:
            el_list = el.split(',')
            el = el_list[0]
            el_price = el_list[1]

            ispis = "[CONDITION]: "
            if float(el_price) + float(heur[el]) >= float(heur[pocetno]):
                ispis += "[OK] "
            else:
                ispis += "[ERR] "
                consistent = False
            ispis += "h(%s) <= h(%s) + c: %.1f <= %.1f + %.1f" % (pocetno, el, float(heur[pocetno]), float(heur[el]), float(el_price))
            print(ispis)

    ispis = "[CONCLUSION]: "
    if consistent:
        ispis += "Heuristic is consistent."
    else:
        ispis += "Heuristic is not consistent."
    print(ispis)
    
    return





def f(op_stanja, op_heur, alg, check):
    o = open(op_stanja, 'r')
    lines = o.readlines()
    o.close()

    count = 0
    f_prijelaza = {}
    for line in lines:
        if line.rstrip()[0] == "#":
            continue
        else:
            count+=1
            if count == 1:
                pocetno_stanje = line.rstrip()  #string
            elif count == 2:
                ciljna_stanja = line.rstrip().split()   #lista
                #ciljna_stanja = line.rstrip()
            else:
                lista_prijelaza = line.rstrip().split()

                #napravit mini dictionarye untura
                if len(lista_prijelaza) == 1:
                    f_prijelaza[lista_prijelaza[0][:-1]] = []
                for i in range(1,len(lista_prijelaza)):
                    #f_prijelaza.put(lista_prijelaza[0][:-1], lista_prijelaza[i])
                    #print(lista_prijelaza[0][:-1], lista_prijelaza[i])
                    if i==1:
                        f_prijelaza[lista_prijelaza[0][:-1]] = []
                    f_prijelaza[lista_prijelaza[0][:-1]].append(lista_prijelaza[i])
                


    if alg == "bfs":
        print("# BFS")
        bfs(pocetno_stanje, ciljna_stanja, f_prijelaza)
        return
    elif alg == "ucs":
        print("# UCS")
        ucs(pocetno_stanje, ciljna_stanja, f_prijelaza)
        return

    

    o = open(op_heur, 'r')
    lines = o.readlines()
    o.close()

    count = 0
    # f_prijelaza = PriorityQueue()
    f_heuristike = {}
    for line in lines:
        if line.rstrip()[0] == "#":
            continue
        else:
            l = line.rstrip().split()
            f_heuristike[l[0][:-1]] = l[1]

    if check == "o":
        print("# HEURISTIC-OPTIMISTIC %s" % op_heur)
        optimisticnost(pocetno_stanje, ciljna_stanja, f_prijelaza, f_heuristike)
        return

    if check == "k":  
        print("# HEURISTIC-CONSISTENT %s" % op_heur)
        konzistentnost(pocetno_stanje, ciljna_stanja, f_prijelaza, f_heuristike)
        return 

    if alg == "astar":
        print("# A-STAR %s" % op_heur)
        astar(pocetno_stanje, ciljna_stanja, f_prijelaza, f_heuristike)
    
    return



if __name__ == "__main__":

    # for ar in sys.argv:
    #     print(ar)

    args = [None] * (len(sys.argv)-1)

    count = 0
    for i in range(1,len(sys.argv)):    #za autograder stavit 0
        args[count] = sys.argv[i]
        count += 1


    if ("--h" in args) and ("--ss" in args) and ("--alg" in args):
        index_h = args.index("--h")
        index_ss = args.index("--ss")
        index_alg = args.index("--alg")
        f(args[index_ss+1], args[index_h+1], args[index_alg+1], None)

    elif ("--h" in args) and ("--ss" in args) and ("--check-optimistic" in args):
        index_h = args.index("--h")
        index_ss = args.index("--ss")
        f(args[index_ss+1], args[index_h+1], "astar", "o")

    elif ("--h" in args) and ("--ss" in args) and ("--check-consistent" in args):
        index_h = args.index("--h")
        index_ss = args.index("--ss")
        f(args[index_ss+1], args[index_h+1], "astar", "k")
        
    elif ("--alg" in args) and ("--ss" in args):
        index_ss = args.index("--ss")
        index_alg = args.index("--alg")
        f(args[index_ss+1], None, args[index_alg+1], None)
    
    