import sys

#provjera konzistentnosti
#provjeri svaku klauzulu dal su njoj stavke u redu
#ne smije imati duplice
#ne smije imati npr a i ~a

#negacija cilja
#strategija brisanja f A (fvg) = f
#backtrack

#svaki put kad nema necega iz onoga_sto_se_trazi
#onda nema rjesenja

def resolution(ulaz):

    o = open(ulaz, 'r')
    lines = o.readlines()
    o.close()

    conclusion_ispis = "[CONCLUSION]: %s" % lines[-1].lower().rstrip()
    
    klauzule = []
    pocetne_klauzule_stringovi = []
    literali = set()
    for line in lines[:-1]:
        if line.rstrip()[0] == "#":
            continue
        else:
            nova_klauzula = line.lower().rstrip().split(" v ")
            obavljeno = False
            #ne zelimo 2 iste klauzule
            for el in klauzule:
                if all(elem in el  for elem in nova_klauzula): #ako stara klauzula sadrzi sve elemente nove liste
                    klauzule.remove(el)
                    klauzule.append(nova_klauzula)
                    literali.update(nova_klauzula)
                    pocetne_klauzule_stringovi.append(line.lower().rstrip())
                    obavljeno = True
            if not obavljeno:
                klauzule.append(nova_klauzula)
                literali.update(nova_klauzula)
                pocetne_klauzule_stringovi.append(line.lower().rstrip())

    #za svaki literal reci u kojim se klauzulama nalazi
    backtrack = {}
    for literal in literali:
        indexi = []  #gdje se sve literal nalazi
        for klauzula in klauzule:
            for k in klauzula:
                if k==literal:
                    indexi.append(klauzule.index(klauzula))
                    break
        if len(indexi)!=0:
            backtrack[literal] = indexi
    
    ciljne_klauzule = lines[-1].lower().rstrip().split(" v ")

    #provjeri konzistentnost cilja (extra korak)
    cilj = []
    for c in ciljne_klauzule:
        if ("~"+c in cilj) or (c[1:] in cilj):
            print("Nekonzistentan ulaz!!!")  #ali svejedno provedi sve
            conclusion_ispis += " is unknown"
            #ne nego treba sve ispisat
            for koristena in pocetne_klauzule_stringovi: #od 0 do len-1
                ispis = str(i+1) + ". "
                i += 1
                ispis += koristena
                konacan_ispis_pocetne_klauzule += ispis + "\n"
            konacan_ispis += str(i+1) + ". " + c + "\n" + "===========" + "\n"
            zavrsni_ispis = konacan_ispis_pocetne_klauzule + konacan_ispis[:-1]
            return zavrsni_ispis, conclusion_ispis
        elif c not in cilj:
            cilj.append(c)
    ciljne_klauzule = cilj

    # print(klauzule)
    # print(backtrack)
    # print(ciljne_klauzule)
    

    #pocinjemo od zadnje koja je unutra (to je ciljna) i nju negiramo
    #negacija cilja
    ostale_ciljne = []
    for i in range(0,len(ciljne_klauzule)):
        if ciljne_klauzule[i][0] == '~':
            tmp_el = ciljne_klauzule[i][1:]
            ostale_ciljne.append([tmp_el])
        else:
            tmp_el = "~" + ciljne_klauzule[i]
            ostale_ciljne.append([tmp_el])

    #print(ostale_ciljne) #to ne mora biti liste u listi ali ajde ok
    

    #bez ciljnih
    #sluzi da znamo svaki put kad idemo provjeravat novi cilj 
    #koje su pocetne
    #jer mijenjamo listu klauzule- u nju stavljamo sve sto provjeravamo
    pocetne_klauzule = klauzule

    for trenutna_ciljna in ostale_ciljne:
        #konacan_ispis_ostalo = ""
        obavljeno = False
        klauzule = pocetne_klauzule
        klauzule_koje_me_ne_zanimaju = []
        
        for el in klauzule:
            if all(elem in el  for elem in trenutna_ciljna): #ako stara klauzula sadrzi sve elemente nove liste
                klauzule_koje_me_ne_zanimaju.append(klauzule.index(el))  #kad ovo imam onda gubim poredak klauzula
                #klauzule.append(trenutna_ciljna)
                obavljeno = True
            # elif all(elem in trenutna_ciljna  for elem in el): #ako nova sadrži sve iz stare
            #     #preskoči novu
        #if not obavljeno:
        klauzule.append(trenutna_ciljna)

        

        ono_sto_trazimo = [] #trazimo negaciju onoga sto imamo
        if klauzule[-1][0][0] == '~':
            ono_sto_trazimo.append(trenutna_ciljna[0][1:])
        else:
            ono_sto_trazimo.append("~" + trenutna_ciljna[0])
        ono_sto_trazimo_copy = []
        ono_sto_trazimo_copy = ono_sto_trazimo.copy()
        
        
        #index_od_kud_backtrackam = 0
        lista_backtrack = []
        #index_od_kud_backtrackam_iskoristen = False
        backtrackaj = False
        indexi_backtrack = []
        j=0

        while len(ono_sto_trazimo) != 0:
            nasla = False
            
            #print("loop ", ono_sto_trazimo)

            if backtrackaj:
                if len(indexi_backtrack)==j:
                    backtrackaj = False
                    j = 0
                else:
                    index_od_kud_backtrackam = indexi_backtrack[j]
                    #print(indexi_backtrack)
                    j+=1
            else:
                index_od_kud_backtrackam = 0
            
            #print(lista_backtrack, indexi_backtrack)
            # print("ono ", ono_sto_trazimo)
            # if j == 3:
            #     break

            for k in range(index_od_kud_backtrackam,len(klauzule)-1):
                if nasla:
                    break
                if k in klauzule_koje_me_ne_zanimaju:
                    continue


                tmp = ""
                #print("klauzule ",klauzule)
                for l in range(len(klauzule[k])):
                    #print(klauzule[k], ono_sto_trazimo)
                    if klauzule[k][l] == ono_sto_trazimo[0]:

                        if (klauzule[k][l], k) not in lista_backtrack:
                            lista_backtrack.append((klauzule[k][l], k))  #dodaj taj literal i index klauzule
                        
                        nasla = True
                        ono_sto_trazimo.pop(0)
                        
                        
                        #jos treba u tmp dodat ostale koje nismo pregledali
                        if l<len(klauzule[k])-1:
                            for li in range(l+1,len(klauzule[k])) :
                                if len(tmp)==0:
                                    tmp += klauzule[k][li]
                                else:
                                    tmp += " v " + klauzule[k][li]
                        
                        #NIL
                        if len(tmp) == 0 and len(ono_sto_trazimo)==0:
                            ono_sto_trazimo.clear()
                            break
                            


                        elif not len(tmp)==0:    #ako nema samo prazan string
                            t = tmp.split(" v ")
                            #zelimo traziti kontra od toga
                            for kontra in t:
                                if kontra[0] == '~':
                                    ono_sto_trazimo.insert(0,kontra[1:])
                                else:
                                    ono_sto_trazimo.insert(0,"~" + kontra)
                        
                           
                        break

                    if l>0:
                        tmp += " v " + klauzule[k][l]
                    else:
                        tmp += klauzule[k][l]

            # if index_od_kud_backtrackam_iskoristen:
            #     index_od_kud_backtrackam = 0
            #     index_od_kud_backtrackam_iskoristen = False

            # print("1 ",lista_backtrack)
            # # print("2 ",nasla)
            # print("2 ",ono_sto_trazimo)

            if not nasla:
                # #probaj_s_negativnom
                # if not probano_s_negativnim: 
                # negativno_ono_sto_trazim = ono_sto_trazimo[0]
                # if negativno_ono_sto_trazim[0]=="~":
                #     negativno_ono_sto_trazim = negativno_ono_sto_trazim[1:]
                # else:
                #     negativno_ono_sto_trazim = "~" + negativno_ono_sto_trazim
                # ono_sto_trazimo[0] = negativno_ono_sto_trazim
                

                #BACKTRACK
                #ako nema za backtrackat onda break
                ima_za_backtrack = False
                i=0
                index_od_kud_backtrackam = 0
                for el in reversed(lista_backtrack):
                    literal, index = el
                    koje_moram_isprobat = backtrack[literal]
                    koje_moram_isprobat.sort()
                    
                    del lista_backtrack[-1]
                    for ind in koje_moram_isprobat:
                        if ind>index:
                            #lista_backtrack = lista_backtrack[:len(lista_backtrack)-(i+1)]
                            #del lista_backtrack[:-(i+1)]
                            ima_za_backtrack = True
                            #print(ono_sto_trazimo,literal)
                            #ono_sto_trazimo.pop(0)  #BESKONACNA PETLJA ZBOG ono_sto_trazimo
                            # ono_sto_trazimo.clear() #to nije skroz tocno
                            # ono_sto_trazimo.insert(0,literal)
                            #print(ono_sto_trazimo)
                            lista_backtrack.append((literal,ind))
                            #print("LISTA_BACKTRACK ",lista_backtrack)
                            j = 0
                            indexi_backtrack.clear()
                            for e in lista_backtrack:
                                a,ind = e
                                indexi_backtrack.append(ind)
                            ono_sto_trazimo.clear()
                            ono_sto_trazimo.extend(ono_sto_trazimo_copy)
                            #index_od_kud_backtrackam = ind
                            #index_od_kud_backtrackam_iskoristen = True
                            backtrackaj = True
                            #print(ono_sto_trazimo)
                            break
                    if ima_za_backtrack:
                        break
                    i=i+1

              
                if not ima_za_backtrack:
                    break


        if nasla:
            break




    konacan_ispis_pocetne_klauzule = ""
    konacan_ispis = ""

    if not nasla:
        conclusion_ispis += " is unknown"
        #ne nego treba sve ispisat
        i=0
        for koristena in pocetne_klauzule_stringovi: #od 0 do len-1
            ispis = str(i+1) + ". "
            i += 1
            ispis += koristena
            konacan_ispis_pocetne_klauzule += ispis + "\n"
        konacan_ispis += str(i+1) + ". " + trenutna_ciljna[0] + "\n" + "===========" + "\n"
        zavrsni_ispis = konacan_ispis_pocetne_klauzule + konacan_ispis[:-1]
        return zavrsni_ispis, conclusion_ispis


    #ispis pocetnih klauzula, bez ciljne
    i=0
    novi_poredak_klauzula = {}  #key: stari_index; value: nova_vrijednost
    for literal,koristena in lista_backtrack: #od 0 do len-1
        #if koristena in pocetne_klauzule_stringovi: 
        ispis = str(i+1) + ". "
        i += 1
        ispis += pocetne_klauzule_stringovi[koristena]
        konacan_ispis_pocetne_klauzule += ispis + "\n"
        novi_poredak_klauzula[koristena] = i


    konacan_ispis += str(i+1) + ". " + trenutna_ciljna[0] + "\n" + "===========" + "\n"
    i += 1

    

    stare_klauzule = []
    for literal,index in lista_backtrack:
        ispis = str(i+1) + ". "
        i += 1
        ispis_l = ""

        neg_literal = literal
        if neg_literal[0]=="~":
            neg_literal = neg_literal[1:]
        else:
            neg_literal = "~"+neg_literal
        if neg_literal in stare_klauzule:
            stare_klauzule.remove(neg_literal)

        for l in stare_klauzule:
            if l!=literal:
                if len(ispis_l)==0:
                    ispis_l+= l
                else:
                    ispis_l += " v " + l
        for l in klauzule[index]:
            if l!=literal:
                if len(ispis_l)==0:
                    ispis_l+= l
                else:
                    ispis_l += " v " + l
                stare_klauzule.append(l)
        
        if ispis_l =="":
            ispis_l = "NIL"
        ispis += ispis_l + " (" + str(novi_poredak_klauzula[index]) + "," + str(i-1) + ")"
        konacan_ispis += ispis + "\n"

    konacan_ispis =  konacan_ispis[:-1] + "\n==========="
    
    if nasla:
        conclusion_ispis += " is true"
        zavrsni_ispis = konacan_ispis_pocetne_klauzule + konacan_ispis
    
    return zavrsni_ispis, conclusion_ispis



def cooking(popis_klauzula, popis_naredbi):
    o = open(popis_klauzula, 'r')
    klauzule_stringovi = o.readlines()
    o.close()

    o = open(popis_naredbi, 'r')
    naredbe = o.readlines()
    o.close()

    #klauzule = []
    o = open("tmp_klauzule.txt", 'w')
    print("Constructed with knowledge:")
    for k in klauzule_stringovi:
        if k[0]!="#":
            o.write(k.lower())
            #klauzule.append(k.lower().rstrip())
            print(k.lower().rstrip())
    o.close()


    for naredba in naredbe:

        naredba = naredba.lower().rstrip()

        if ((not naredba[-1]=="?") and (naredba[-1]=="+") and (naredba[-1]=="-")) or naredba[0]=="#":
            continue

        print("\nUser's command: %s" %naredba)
            
        #provjera valjanosti
        if naredba[-1]=="?":
            o = open("tmp_klauzule.txt", 'a')
            o.write(naredba[:-2].lower())
            o.close()

            postupak, conclusion = resolution("tmp_klauzule.txt")
            if conclusion[-4:] == "true":
                print(postupak)
            print(conclusion)

            o = open("tmp_klauzule.txt", 'r')
            lines = o.readlines()[:-1]
            lines = "".join(lines)
            o.close()

            o = open("tmp_klauzule.txt", 'w')
            o.write(lines)
            o.close()
            
            
        #dodavanje znanja tj klauzula
        if naredba[-1]=="+":
            o = open("tmp_klauzule.txt", 'r')
            lines = o.readlines()
            lines.append(naredba[:-2].lower() + "\n")
            lines = "".join(lines)
            o.close()

            o = open("tmp_klauzule.txt", 'w')
            o.write(lines)
            o.close()

            print("Added %s" % naredba[:-2])
            

        #brisanje znanja
        elif naredba[-1]=="-":
            o = open("tmp_klauzule.txt", 'r')
            lines = o.readlines()
            if naredba[:-2].lower() + "\n" in lines:
                lines.remove(naredba[:-2].lower() + "\n")
            lines = "".join(lines)
            o.close()

            o = open("tmp_klauzule.txt", 'w')
            o.write(lines)
            o.close()

            print("Removed %s" % naredba[:-2])

    return



if __name__ == "__main__":
    

    if len(sys.argv)<2:
        sys.exit(0)

    if sys.argv[1]=="resolution" and len(sys.argv)==3:
        print1,print2 = resolution(sys.argv[2])
        print(print1)
        print(print2)
    elif sys.argv[1]=="cooking" and len(sys.argv)==4:
        cooking(sys.argv[2],sys.argv[3])
    