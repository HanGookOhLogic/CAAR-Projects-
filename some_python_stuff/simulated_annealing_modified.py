import math
from math import sqrt as s
import random
import copy
import pairs_helper  

def f(x):
	b = s(1-x**2)+s(1-x**2/4)-0.02
	n = s(1-x**2)-0.01
	print(n,b-n,x/2)

# calculates the cost of an assignment, i.e. the number of pairs of monochromatic adjacent pixels
def total_cost(pairs, assignment, r, c):
    total_cost = 0
    for i in range(r):
        for j in range(c):
            neighboring_pixels = pairs[i][j]
            current_color = assignment[i][j]
            for pixel in neighboring_pixels:
                if current_color == assignment[pixel[0]][pixel[1]]:
                    total_cost += 1
    return total_cost / 2
	
# calculates the change in cost of an assignment where pixel 'new_pixel' is changed to color 'new_color'
# if input includes old_cost, the cost of the assignment before the change, cost will return the total new cost
def relative_cost(pairs, assignment, r, c, new_pixel, new_color, old_cost=0):
    prev_cost = 0
    new_cost = 0
    old_color = assignment[new_pixel[0]][new_pixel[1]]
    neighboring_pixels = pairs[new_pixel[0]][new_pixel[1]]
    for pixel in neighboring_pixels:
        current_color = assignment[pixel[0]][pixel[1]]
        if current_color == new_color:
            new_cost += 1
        if current_color == old_color:
            prev_cost += 1
    return old_cost + (new_cost - prev_cost)
  
# generates a random assignment of colors to pixels
def random_assignment(k, r, c):
    return [[random.randrange(k) for i in range(c)] for j in range(r)]
  
# given an assignment, it finds a neighboring assignment by randomly flipping the color of one pixel
# returns new assignment, coordinates of changed pixel, and its old color
def neighboring_solution(assignment, r, c, k):
    random_pixel = (random.randrange(r), random.randrange(c))
    old_color = assignment[random_pixel[0]][random_pixel[1]]
    new_color = random.choice(range(old_color) + range(old_color + 1, k))
    return random_pixel, new_color
  
# changes the color of pixel in assignment to color
def change_pixel(assignment, pixel, color):
    assignment[pixel[0]][pixel[1]] = color
  
# Simulated annealing algorithm to find a coloring of an nxn grid of pixels with side length s and number of colors k with a globally minimum number of pairs of same colored pixels that are distance 1 from each other. 
# T_initial - the starting temperature
# cooling_rate - Each iteration, the temperature is multiplied by (1-cooling_rate). The bigger the cooling rate, the faster T converges to 0.
# final_temp - the temperature T must decrease to before algorithm terminates
# length_initial - number of repetitions for temperature T_initial
# length_increase - the number of repetitions for each temperature is multiplied by length_increase each time we decrease the temperature. So if length_increase is higher, the algorithm will take longer but try more options.
def simulated_annealing(w, h, r, c, k, wrapping=True, T_initial=10, cooling_rate=0.15, final_temp=0.05, length_initial=100, length_increase=1.2):
    pairs = pairs_helper.rect_pixel_pairs(w, h, r, c, wrapping)
    current_assignment = random_assignment(k, r, c)
    current_cost = total_cost(pairs, current_assignment, r, c)
    T = T_initial
    length = length_initial
    while T > final_temp and current_cost > 0:
        iter = 0
        while iter < length:
            new_pixel, new_color = neighboring_solution(current_assignment, r, c, k)
            change_in_cost = relative_cost(pairs, current_assignment, r, c, new_pixel, new_color)
            if change_in_cost <= 0:
                change_pixel(current_assignment, new_pixel, new_color)
                current_cost += change_in_cost
            else:
                Metropolis_probability = math.exp(-1*change_in_cost/T)
                if Metropolis_probability > random.uniform(0,1):
                    change_pixel(current_assignment, new_pixel, new_color)
                    current_cost += change_in_cost
            iter += 1
        T = T*(1-cooling_rate)
        length *= length_increase
    return current_assignment, current_cost

def color2(n):
    pairs = pairs_helper.list_of_pixel_pairs(8.660254,n,True)
    massignment = [[0 for i in range(n)] for j in range(n)]
    assignment = [[(int(float(i)/(n//10)))%2 for i in range(n)] for j in range(n)]
    a = total_cost(pairs,assignment,n,n)
    b = total_cost(pairs,massignment,n,n)
    print("n =",n)
    print("max:",int(a))
    print("part:",int(b))
    print("ratio:",round(a/b,3))

def color3(h1):
    h = h1*1.5
    w = h*s(3)
    f = open("hexagon tileblock.txt",'r')
    l = list(map(list,f.read().split("\n")))
    r = len(l)
    c = len(l[0])
    for i in range(len(l)):
        l[i] = list(map(int,l[i]))
    pairs = pairs_helper.rect_pixel_pairs(w,h,r,c,True)
    massignment = [[0 for i in range(c)] for j in range(r)]
    a = total_cost(pairs,l,r,c)
    b = total_cost(pairs,massignment,r,c)
    print(h/1.5, a/b)

def color3kruskal(r, bg, th):
    """r = width of red column, bg = width of bluegreen column, th = thickness
        of one blue or green chunk in the bluegreen column"""
    PW = 0.01
    
    redpix = int(r/PW)
    bgpix = int(bg/PW)
    thpix = int(th/PW)
    rows = 2*thpix
    cols = 2*(redpix+bgpix)

    brow = [0 for i in range(redpix)]
    [brow.extend([1 for i in range(bgpix)]),brow.extend([0 for i in range(redpix)]),brow.extend([2 for i in range(bgpix)])]
    grow = [0 for i in range(redpix)]
    [grow.extend([2 for i in range(bgpix)]),grow.extend([0 for i in range(redpix)]),grow.extend([1 for i in range(bgpix)])]
    assert len(brow)==len(grow)
    while len(brow) < 200:
        brow.extend(brow)
        grow.extend(grow)

    tot = [brow for i in range(thpix)]
    tot.extend([grow for i in range(thpix)])
    while len(tot)< 200:
        tot.extend(tot)

    #print("\n".join(["".join(list(map(str,l))) for l in tot]))

    monor = len(tot)
    monoc = len(tot[0])
    w = PW * len(tot[0])
    h = PW * len(tot)

    mono = [[0 for i in range(monoc)] for j in range(monor)]

    print("doin' them pairs")
    pairs = pairs_helper.rect_pixel_pairs(w, h, monor, monoc, True)

    print("gettin' that first coss")
    kruskost = total_cost(pairs,tot,monor,monoc)
    print("gettin' that nex coss")
    monocost = total_cost(pairs,mono,monor,monoc)

    ratio = kruskost/monocost

    #return ratio

    print("R:"+str(r),"BG:"+str(bg),"TH:"+str(th),"-->", ratio)

#print(color3kruskal(0.61,0.97,0.97))
color3kruskal(0.62,0.96,0.98)



##for i in range(25):
##    color3kruskal(random.random()/1.666666+0.4,random.random()/2.5+0.6,random.random())

#print(color3kruskal(0.6211743476512981,0.9865600965121694,0.9831678455861091))

























    
"""
Results for kruskal colorings:
R:0.1 BG:0.1 TH:0.1 --> 0.38222636815920397

R:0.6 BG:1.5 TH:0.6 --> 0.27531390665719024
R:0.6 BG:1.4 TH:0.6 --> 0.26745957711442786
R:0.6 BG:1.3 TH:0.6 --> 0.2587784760408484
R:0.6 BG:1.2 TH:0.6 --> 0.24913280818131564
R:0.6 BG:1.1 TH:0.6 --> 0.23835235586772022
R:0.6 BG:1   TH:0.6 --> 0.2262243470149254
R:0.6 BG:0.9 TH:0.6 --> 0.23166639027086788
R:0.6 BG:0.8 TH:0.6 --> 0.25376391850272445
R:0.6 BG:0.7 TH:0.6 --> 0.2891746396224008
R:0.6 BG:0.6 TH:0.6 --> 0.3402705223880597
R:0.6 BG:0.5 TH:0.6 --> 0.41147331524197195

R:0.6 BG:0.71 TH:0.71 --> 0.24868855379055693
R:0.7 BG:0.71 TH:0.71 --> 0.23922640319529115
R:0.71 BG:0.71 TH:0.71 --> 0.23906898753603537
R:0.8 BG:0.71 TH:0.71 --> 0.24384583007915372
R:0.9 BG:0.71 TH:0.71 --> 0.2615154478678256

R:0.5 BG:1 TH:0.6 --> 0.24508789386401328
R:0.7 BG:1 TH:0.6 --> 0.21838430397034436
R:0.6 BG:1 TH:0.5 --> 0.2893973880597015
R:0.6 BG:1 TH:0.7 --> 0.18119047619047618

R:0.8 BG:1 TH:0.6 --> 0.2214354155150175
R:0.9 BG:1 TH:0.6 --> 0.23627476651828577
R:0.6 BG:1 TH:0.8 --> 0.15021707866915424
R:0.6 BG:1 TH:0.9 --> 0.13259846600331676
R:0.6 BG:1 TH:1 --> 0.13101725746268655
R:0.6 BG:1 TH:1.1 --> 0.14549949118046132

R:0.5 BG:1 TH:1 --> 0.136636815920398
R:0.55 BG:1 TH:1 --> 0.13248515487080725
R:0.58 BG:1 TH:1 --> 0.13159299046170422
R:0.59 BG:1 TH:1 --> 0.13128455822155047
R:0.6 BG:1 TH:1 --> 0.13101725746268655
R:0.61 BG:1 TH:1 --> 0.13102530824140168
R:0.62 BG:1 TH:1 --> 0.13114351084085743
R:0.65 BG:1 TH:1 --> 0.13213297150610584
R:0.7 BG:1 TH:1 --> 0.13552604623939127

R:0.6 BG:0.98 TH:1 --> 0.12968229101391152
R:0.6 BG:1.02 TH:1 --> 0.13406612883510574
R:0.6 BG:1 TH:1.02 --> 0.1343944137060765
R:0.6 BG:1 TH:0.98 --> 0.12923759850474845
R:0.6 BG:0.96 TH:1 --> 0.12985275450621986
R:0.6 BG:1 TH:0.96 --> 0.12879280115511552
R:0.6 BG:0.94 TH:1 --> 0.1333311620635748
R:0.6 BG:1 TH:0.94 --> 0.13053029487731382
R:0.6 BG:0.92 TH:1 --> 0.1333311620635748
R:0.6 BG:1 TH:0.92 --> 0.13053029487731382

R:0.6 BG:0.98 TH:0.96 --> 0.12739887517232737

R:0.6 BG:0.96 TH:0.96 --> 0.12777804222729966
R:0.6 BG:0.94 TH:0.96 --> 0.13166851224596143
R:0.6 BG:0.98 TH:0.94 --> 0.129302053760687
R:0.6 BG:0.98 TH:0.92 --> 0.129302053760687
R:0.62 BG:0.98 TH:0.96 --> 0.12737533518976898
R:0.64 BG:0.98 TH:0.96 --> 0.12779802285784134
R:0.66 BG:0.98 TH:0.96 --> 0.12864558178378813
R:0.58 BG:0.98 TH:0.96 --> 0.128629157558613
R:0.56 BG:0.98 TH:0.96 --> 0.128629157558613
R:0.54 BG:0.98 TH:0.96 --> 0.12999459896647558

R:0.46794884145107196 BG:0.9783099540115038 TH:0.9158804754225764 --> 0.1469475820821519
R:0.5020122972534204 BG:0.831137664874172 TH:0.59541043549448 --> 0.2802670207388901
R:0.286695222948684 BG:0.9693555973924836 TH:0.38344048545688125 --> 0.31287506934055037
R:0.5545381385202416 BG:0.3641023984295071 TH:0.5671148385722812 --> 0.5512690554769762
R:0.7900326895827829 BG:0.2127954329935805 TH:0.7693657251587206 --> 0.6827854643681339
R:0.20709501804920005 BG:0.06526832504875779 TH:0.071926231362059 --> 0.6022467631378522
R:0.46055437213792194 BG:0.9558678691851236 TH:0.2910793667822429 --> 0.22112800565770863
R:0.5870543969777862 BG:0.826338250774654 TH:0.7127491752262349 --> 0.21045261669024046
R:0.2968199740843058 BG:0.4214008953326739 TH:0.7531023783003217 --> 0.37605030773347603
R:0.7384117522703789 BG:0.16405686414136245 TH:0.6588022833195448 --> 0.7241435081008101
R:0.8780350115557927 BG:0.5677932986950833 TH:0.4051442695809422 --> 0.3441674801282945
R:0.4225034192188519 BG:0.4385290670575339 TH:0.36926302607323314 --> 0.4258506207763634
R:0.15317584241820503 BG:0.23631003300607922 TH:0.07303758993851905 --> 0.2988632196552989
R:0.03340736483840212 BG:0.5210229065831258 TH:0.06750385472706033 --> 0.46549932771054886
R:0.633057147820083 BG:0.626327301744953 TH:0.5950380449416482 --> 0.3282204398649572
R:0.3525817904110662 BG:0.15401785028390824 TH:0.3239098155095772 --> 0.5827080754950495
R:0.18038347881214178 BG:0.39003921192751967 TH:0.685947200655817 --> 0.3663184333139196
R:0.7899578111367468 BG:0.4281032422494847 TH:0.1990891617989523 --> 0.43163733039970664
R:0.4948242472534392 BG:0.2510791835978631 TH:0.02201574945632856 --> 0.49491199119911994
R:0.6872379081654121 BG:0.5036360931571656 TH:0.7083389418605706 --> 0.3672332366408554
R:0.4750082025516694 BG:0.668003575013601 TH:0.206337758715342 --> 0.2942141089108911
R:0.6350428834693751 BG:0.9867460920580396 TH:0.18889705931100653 --> 0.20222084708470847
R:0.3301914660850055 BG:0.5116648491602975 TH:0.9125905190770913 --> 0.3854168343663635
R:0.800622985491616 BG:0.8279266594037266 TH:0.8421030171668066 --> 0.17996330056286053
R:0.6966988814538808 BG:0.8726897472925076 TH:0.5606470050058157 --> 0.24747308914564925
R:0.9896691736879211 BG:0.8187189223927065 TH:0.7119721888164571 --> 0.25534780604866264
R:0.6451289927516404 BG:0.6334228300330768 TH:0.217624444112959 --> 0.28056341348420555
R:0.9304916880930386 BG:0.7118729826919238 TH:0.33935974286941417 --> 0.25258411257792446
R:0.5655503542574887 BG:0.6439462883737371 TH:0.28128662691633166 --> 0.29668788307402166
R:0.7308907376806949 BG:0.7252912489318681 TH:0.8094565089898044 --> 0.21428252200220022
R:0.5606856739029261 BG:0.6991366535559466 TH:0.8426423351101179 --> 0.23707053885112014
R:0.8574505843594991 BG:0.7449735404783855 TH:0.7638858812954458 --> 0.22691225651545835
R:0.49646878492522417 BG:0.9503992224497344 TH:0.2403188336220855 --> 0.28935701668758423
R:0.7035042749269474 BG:0.8561690425941699 TH:0.5492371804792103 --> 0.2595747670005096
R:0.5220407497795819 BG:0.9410961090622583 TH:0.9412489682207509 --> 0.13502976645668063
R:0.7561944688841304 BG:0.918695409918896 TH:0.3268733046925477 --> 0.17951015757063513
R:0.8595803198029581 BG:0.9906644282777828 TH:0.7654595939735016 --> 0.17392658149562787
R:0.6213869242798263 BG:0.7110955412026593 TH:0.7030717513713557 --> 0.2514872915863015
R:0.47960126988201 BG:0.7756246661128923 TH:0.932827197936268 --> 0.20165945675109206
R:0.5308844186646418 BG:0.6424072682157703 TH:0.5390465447459333 --> 0.3683977849132114
R:0.7007424926226017 BG:0.7281492062010586 TH:0.6190511897346207 --> 0.26599497977966813
R:0.41880435998255083 BG:0.7864839665791494 TH:0.8388757392317053 --> 0.23671306775158707
R:0.7570988633179869 BG:0.9957790344531358 TH:0.1960530993397268 --> 0.20329649243994166
R:0.8172796843538657 BG:0.6975448508553236 TH:0.14191419264033678 --> 0.25193528040062696
R:0.5289975637864566 BG:0.6888329885474161 TH:0.8541970763009518 --> 0.2461830111582587
R:0.5433190003787332 BG:0.8160576970518515 TH:0.6257107226796452 --> 0.2561660715903078
R:0.922378977877014 BG:0.6676151579650715 TH:0.7552562534604284 --> 0.2816040755632183
R:0.9291917462907425 BG:0.789192534962283 TH:0.6269839922679524 --> 0.2626674432149097
R:0.6406336998747942 BG:0.9835002791002301 TH:0.3455756104395331 --> 0.1910200824003969
R:0.7592678511887136 BG:0.8720474175578861 TH:0.34513691731436835 --> 0.19891525917297612


R:0.6016548059436269 BG:0.9943515230361728 TH:1.015830500234796 --> 0.13087222549345895
R:0.6238416114033971 BG:1.0107740764945672 TH:0.938259409466782 --> 0.13127151824565547
R:0.6314595749313836 BG:0.9955400216559112 TH:1.0007223248418968 --> 0.1313591972795953
R:0.6530280246569717 BG:0.9793667912160247 TH:0.998617315436862 --> 0.1313991790618093
R:0.6714158069035988 BG:0.9782917004484939 TH:0.937792609627573 --> 0.1327881203302484
R:0.6980582682802874 BG:1.015323834628662 TH:0.9672977947450883 --> 0.1331685601012793
R:0.6016141855729604 BG:0.9510466088538778 TH:1.0128634067499536 --> 0.13348586834100443
R:0.6536357301892917 BG:0.9497270152330712 TH:1.014890014032166 --> 0.13394130744877014
R:0.6174176988547886 BG:1.0072564239825899 TH:0.9292753449929915 --> 0.13402093307049656
R:0.5865826621559909 BG:1.0299496141281312 TH:1.0110134249390117 --> 0.1340830154544601
R:0.5582180891661950 BG:0.92974358312599 TH:0.9833040544052812 --> 0.14060070740049752
R:0.5563228321435199 BG:1.0406149188639957 TH:0.9675747422075812 --> 0.13493828932261767
R:0.6560671346097654 BG:0.9598663837772053 TH:0.954065535231941 --> 0.13479130402577683
R:0.6039247060952139 BG:1.0092807567687565 TH:0.9967956749608556 --> 0.13087222549345895
R:0.6688226067279426 BG:1.0478034588133645 TH:1.0169501939673347 --> 0.13507341539057957
R:0.6312094207448394 BG:1.0390320815956404 TH:1.0072045573690203 --> 0.1339439167797377
R:0.6605693133720933 BG:0.9720804752498756 TH:1.046744666585981 --> 0.1357794361525705
R:0.6866807217862446 BG:0.9551584794420677 TH:0.9485115543224779 --> 0.135672822739619
R:0.5680333751771041 BG:1.086203085182692 TH:0.9108443079234939 --> 0.14641606780910263
R:0.6265901850009521 BG:1.053164522548715 TH:0.9597372396145537 --> 0.1370945857224143

R:0.62 BG:0.96 TH:0.98 --> 0.12854771608246549
"""

"""
Results for 2 color check:
n = 100
max: 920000
part: 295000
ratio: 0.321

n = 200
max: 2446000
part: 7520000
ratio: 0.325

n = 300
max: 7977000
part: 24840000
ratio: 0.321

n = 400
max: 19180000
part: 59520000
ratio: 0.322
"""

"""
Results for 3 color check:
n = 400 s = 18
part: 6749640
max: 28800000
ratio: 0.234

n = 400 s = 18.181818
part: 6283746
max: 28160000
ratio: 0.223

n = 400 s = 18.1
part: 6569085
max: 28800000
ratio: 0.228

n = 400 s = 18.2
part: 6102912
max: 27520000
ratio: 0.222

n = 400 s = 18.23
part: 6033881
max: 27520000
ratio: 0.219

n = 400 s = 18.26
part: 5912435
max: 27520000
ratio: 0.215

n = 400 s = 18.29
part: 5912435
max: 27520000
ratio: 0.215

n = 400 s = 18.32
part: 5855855
max: 27520000
ratio: 0.213

n = 400 s = 18.35
part: 5855855
max: 27520000
ratio: 0.213

n = 400 s = 18.380000000000003
part: 5855855
max: 27520000
ratio: 0.213

n = 400 s = 18.41
part: 5855855
max: 27520000
ratio: 0.213

n = 400 s = 18.44
part: 5855855
max: 27520000
ratio: 0.213

n = 400 s = 18.470000000000002
part: 5855855
max: 27520000
ratio: 0.213

n = 400 s = 18.5
part: 5790060
max: 27520000
ratio: 0.21

n = 400 s = 18.53
part: 5731789
max: 27520000
ratio: 0.208

n = 400 s = 18.560000000000002
part: 5731789
max: 27520000
ratio: 0.208

n = 400 s = 18.59
part: 5678184
max: 27520000
ratio: 0.206

n = 400 s = 19
part: 5157359
max: 27520000
ratio: 0.187

n = 400 s = 20
part: 3980626
max: 25600000
ratio: 0.155

n = 400 s = 21
part: 3383162
max: 24960000
ratio: 0.136

n = 400 s = 22
part: 3048473
max: 23680000
ratio: 0.129

n = 400 s = 23
part: 2916955
max: 22400000
ratio: 0.13

n = 400 s = 24
part: 2868091
max: 21120000
ratio: 0.136

n = 400 s = 25
part: 2956928
max: 19840000
ratio: 0.149

n = 400 s = 21.0
part: 3383162
max: 24960000
ratio: 0.136

n = 400 s = 21.1
part: 3172599
max: 23680000
ratio: 0.134

n = 400 s = 21.2
part: 3155034
max: 23680000
ratio: 0.133

n = 400 s = 21.3
part: 3141877
max: 23680000
ratio: 0.133

n = 400 s = 21.4
part: 3141877
max: 23680000
ratio: 0.133

n = 400 s = 21.5
part: 3124695
max: 23680000
ratio: 0.132

n = 400 s = 21.6
part: 3105531
max: 23680000
ratio: 0.131

n = 400 s = 21.7
part: 3074243
max: 23680000
ratio: 0.13

n = 400 s = 21.8
part: 3061157
max: 23680000
ratio: 0.129

n = 400 s = 21.9
part: 3061157
max: 23680000
ratio: 0.129

n = 400 s = 22.0
part: 3048473
max: 23680000
ratio: 0.129

n = 400 s = 22.1
part: 3039857
max: 23680000
ratio: 0.128

n = 400 s = 22.2
part: 2954902
max: 23040000
ratio: 0.128

n = 400 s = 22.3
part: 2885761
max: 22400000
ratio: 0.129

n = 400 s = 22.4
part: 2895128
max: 22400000
ratio: 0.129

n = 400 s = 22.5
part: 2891996
max: 22400000
ratio: 0.129

n = 400 s = 22.599999999999998
part: 2891283
max: 22400000
ratio: 0.129

n = 400 s = 22.7
part: 2888227
max: 22400000
ratio: 0.129

n = 400 s = 22.8
part: 2888227
max: 22400000
ratio: 0.129

n = 400 s = 22.9
part: 2905811
max: 22400000
ratio: 0.13

n = 400 s = 23.0
part: 2916955
max: 22400000
ratio: 0.13

n = 400 s = 23.099999999999998
part: 2916955
max: 22400000
ratio: 0.13

n = 400 s = 22.11
part: 3039857
max: 23680000
ratio: 0.12837233952702704

n = 400 s = 22.12
part: 3039857
max: 23680000
ratio: 0.12837233952702704

n = 400 s = 22.13
part: 3039857
max: 23680000
ratio: 0.12837233952702704

n = 400 s = 22.14
part: 3039857
max: 23680000
ratio: 0.12837233952702704

n = 400 s = 22.15
part: 3039857
max: 23680000
ratio: 0.12837233952702704

n = 400 s = 22.16
part: 3039857
max: 23680000
ratio: 0.12837233952702704

n = 400 s = 22.169999999999998
part: 3039857
max: 23680000
ratio: 0.12837233952702704

n = 400 s = 22.18
part: 3039857
max: 23680000
ratio: 0.12837233952702704

n = 400 s = 22.189999999999998
part: 2954902
max: 23040000
ratio: 0.1282509548611111

n = 400 s = 22.2
part: 2954902
max: 23040000
ratio: 0.1282509548611111

n = 400 s = 22.21
part: 2954902
max: 23040000
ratio: 0.1282509548611111

n = 400 s = 22.22
part: 2954902
max: 23040000
ratio: 0.1282509548611111

n = 400 s = 22.23
part: 2885761
max: 22400000
ratio: 0.12882861607142856

n = 400 s = 22.24
part: 2885761
max: 22400000
ratio: 0.12882861607142856

n = 400 s = 22.25
part: 2885761
max: 22400000
ratio: 0.12882861607142856

n = 400 s = 22.259999999999998
part: 2885761
max: 22400000
ratio: 0.12882861607142856

n = 400 s = 22.27
part: 2885761
max: 22400000
ratio: 0.12882861607142856

n = 400 s = 22.28
part: 2885761
max: 22400000
ratio: 0.12882861607142856

n = 400 s = 22.29
part: 2885761
max: 22400000
ratio: 0.12882861607142856

n = 400 s = 22.3
part: 2885761
max: 22400000
ratio: 0.12882861607142856
"""

"""
Results for improved 3 color check:
1.0 0.23111070106386736
1.21 0.12542570772864436
1.221 0.12330836127627572
1.23 0.1243721952231466
1.216 0.12454242008397653
1.226 0.12486700890990264
1.218 0.12423709310384279
1.224 0.12257119468265358
1.222 0.12276141297710058
1.223 0.12267690857953514
1.224 0.12257119468265358
1.225 0.12492224544081139

1.2241 0.12256202618375998
1.2242 0.12244269062450881
1.22425 0.12244058550876732
1.22425625 0.12244058550876732
1.2242625 0.12493795032207324
1.224275 0.12493795032207324
1.2243 0.12493795032207324

with updated hexagons
1.223 0.12246290329612322
1.224 0.1223541332329438
1.22425 0.12221459948732676
1.2245 0.12475068500996798
1.225 0.1247335944038889
"""








