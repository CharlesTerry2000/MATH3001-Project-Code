from music21 import pitch
from math import cosh
import matplotlib.pyplot as plt
from statistics import mean, stdev

def Default_slide_position(n):
    
    #Each list presented in the code below contains note numbers that correspond to the same default slide position.
    #The returned number is the default slide position.
    #This function will be used in the note traversal function.
    
    for a in [0,12,19]:    
        if n == a:
            return 7
    
    for a in [1,13,20]:
        if n == a:
            return 6
        
    for a in [2,14,21,26]:
        if n == a:
            return 5
        
    for a in [3,15,22,27,31]:
        if n == a:
            return 4
        
    for a in [4,16,23,28,32,35,40]:
        if n == a:
            return 3
        
    for a in [38]:
        if n == a:
            return 2.5
    
    for a in [5,17,24,29,33,36,41,43,45]:
        if n == a:
            return 2
        
    for a in [39]:
        if n == a:
            return 1.5
        
    for a in [6,18,25,30,34,37,42,44,46]:
        if n == a:
            return 1
    
    for a in [7,8,9,10,11]:
        if n == a:
            return "N/A"
    if n > 46:
        return "Above Considered Range"


def I_note_traversal(x1,s1,x2,s2,t,l,slur):
    #I in the function is an abbreviation of 'inconvenience'.
    
    n1 = pitch.Pitch(x1)
    n2 = pitch.Pitch(x2)
    
    #Each note has it's own midi number. 
    #Given that I have assigned numbers to notes in the trombone's range, by subtracting 28 from the midi numbers, I will obtain the numbers I have assigned to each note. 
    p1 = n1.midi -28
    p2 = n2.midi -28
    
    #The following lines allow choice for whether the default slide position is inputted or if an alternate position is inputted.
    if s1 == 'd':
        sl1 = Default_slide_position(p1)
    else:
        sl1 = s1
    
    if s2 == 'd':
        sl2 = Default_slide_position(p2)
    else:
        sl2 = s2
    
    #Since we are only considering notes within a certain range.
    if p1 < 0 or 6 < p1 < 12 or p2 < 0 or 6 < p2 < 12:
        return "Not Possible"
    elif p1 > 46 or p2 > 46:
        return "Above Considered Range"
    
    #Applying the formula for the Euclidean Distance.
    dist = ((p1 - p2)**2 + (sl1 - sl2)**2)**(1/2)
    
    tm = t/(60*l)
    
    #Taking into account slurring alongside the tempo.
    if tm <= 1 and slur == 'n':
        fm = 1
    elif tm > 1 and slur == 'n':
        fm = tm
    elif tm <=1 and slur == 'y':
        fm = 1.5
    elif tm > 1 and slur == 'y':
        fm = t/(40*l)
    
    #We obtain the final inconvenience score by taking the product of the distance and the multiplier.    
    return dist*fm
          
    
def I_note_production(x,d,l,t):
    n = pitch.Pitch(x)
    p = n.midi - 28
    
    if p < 0 or 6 < p < 12:
        return "Not Possible"
    elif p > 46:
        return "Above Considered Range"
    
    #The following is applied if the note lies in the pedal range.
    #There are 5 cases for the 5 different dynamics being considered.
    if 0 <= p <= 6:
        if d == 'pp':
            I = 3.437*(0.709)**p + 6.563
        elif d == 'p':
            I = 3.134*(0.649)**p + 6.366
        elif d == 'mp' or d == 'mf':
            I = 5.184*(0.730)**p + 3.816
        elif d == 'f':
            I = -17.039*(1.047)**p + 27.039
        elif d == 'ff':
            I = 13.609*(0.927)**p - 2.609
    
    #The following is applied if the note lies in the standard range.
    elif 12 <= p <= 46:
        if d == 'pp':
            I = 1.4*cosh(0.165*(p-26))
        elif d == 'p':
            I = 1.2*cosh(0.169*(p-26))
        elif d == 'mp' or d == 'mf':
            I = cosh(0.157*(p-26))
        elif d == 'f':
            I = 1.1*cosh(0.155*(p-26))
        elif d == 'ff':
            I = 1.3*cosh(0.165*(p-26))
            
    ls = l*t/60
    if ls > 1:
        m = 1 + (ls-1)/3
    elif ls < 1:
        m = 1
    
    #Similarly to note traversal, we obtain the final inconvenience score by taking the product of the initial inconvenience (produced by the function) and the multiplier.
    return I*m



def note_traversal_list(n,t,l,slur):
    #This function will input the following:
    #A list of notes from the excerpt in order.
    #The tempo throughout the excerpt (since the tempo in the sight reading excerpts being analysed is mostly constant with the acception of one small negligable rall).
    #The length in crotchet beats from one note to the next (including rests in between)
    #For each interval whether there is a slur or not. 
    
    x = []
    n1 = []
    n2 = []
    i = 0
    j = 1
    
    #The following two loops take the list of notes and produces two sublists.
    #One sublist omits the last value and the other sublist omits the first value.
    #This means the notes in the same position in the list are neighbouring notes and their inconvenience can be calculated and added to list 'x'.
    while i < len(n)-1:
        n1.append(n[i])
        i = i+1
    
    while j < len(n):
        n2.append(n[j])
        j = j+1
    
    #The following loop forms a list of the inconvenience of every interval.
    k = 0
    while k < len(n1):
        a = I_note_traversal(n1[k], 'd', n2[k], 'd', t, l[k], slur[k])
        x.append(a)
        k = k+1
        
    return x


def note_production_list(n,d,l,t):
    
    #The following loop forms a list of the inconvenience of every note produced.
    x = []
    i = 0
    while i < len(n):
        a = I_note_production(n[i], d[i], l[i], t)
        x.append(a)
        i = i+1
        
    return x

    
#Grade 1
#Note traversal
#Below is the list of notes, tempo, list of lengths between two notes, and list of slurs between two notes.
n_1 = ['D3','F3','D3','B-2','E-3','F3','D3','F3','E-3','D3','F3','B-2']
t_1 = 108
lt_1 = [1,1,1,1,2,2,1,1,1,1,2]
slur_1 = ['n','n','n','n','n','n','n','n','n','n','n']
nt_1 = note_traversal_list(n_1, t_1, lt_1, slur_1)

#We are simply plotting the list of inconvenience scores against a list of ascending integars of equal length.
#By doing this, we can see how the inconveniece of the piece varies with progress through the piece.    
plt.figure('Grade 1 Note Traversal')
plt.plot(list(range(1,len(n_1))), nt_1)            
plt.title("Grade 1 Note Traversal")
plt.xlabel('Progress through Piece')
plt.ylabel('Inconvenience')
#The following two lines hide the x-axis values since visually the x-axis values are not required in order to understand the progress through the excerpt.
ax = plt.gca()
ax.axes.xaxis.set_ticks([])
print("Grade 1 Note Traversal")
print("min = %s"%min(nt_1))
print("max = %s"%max(nt_1))
print("mean = %s"%mean(nt_1))
print("standard deviation = %s"%stdev(nt_1))
print()

#Note production    
d_1 = ['mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf']
lp_1 = [1,1,1,1,2,2,1,1,1,1,2,2]
np_1 = note_production_list(n_1, d_1, lp_1, t_1)

plt.figure('Grade 1 Note Production')
plt.plot(list(range(1,len(n_1)+1)), np_1)            
plt.title("Grade 1 Note Production")
plt.xlabel('Progress through Piece')
plt.ylabel('Inconvenience')
ax = plt.gca()
ax.axes.xaxis.set_ticks([])
print("Grade 1 Note Production")
print("min = %s"%min(np_1))
print("max = %s"%max(np_1))
print("mean = %s"%mean(np_1))
print("standard deviation = %s"%stdev(np_1))
print()
print()

#The above code for grade 1 will be repeated for each grade.

#Grade 2
#Note traversal
n_2 = ['B-2','D3','D3','E-3','E-3','F3','G3','F3','F3','D3','F3','G3','F3','D3','F3','E-3','C3','F3','E-3','E-3','C3','B-2']
t_2 = 112
lt_2 = [3,1,1,1,1,1,1,1,1,1,4,1,1,2,1,1,2,1,1,1,1]
slur_2 = ['n','n','y','n','y','n','y','n','n','n','n','n','n','n','n','n','n','y','n','n','n']
nt_2 = note_traversal_list(n_2, t_2, lt_2, slur_2)
    
plt.figure('Grade 2 Note Traversal')
plt.plot(list(range(1,len(n_2))), nt_2)            
plt.title("Grade 2 Note Traversal")
plt.xlabel('Progress through Piece')
plt.ylabel('Inconvenience')
ax = plt.gca()
ax.axes.xaxis.set_ticks([])
print("Grade 2 Note Traversal")
print("min = %s"%min(nt_2))
print("max = %s"%max(nt_2))
print("mean = %s"%mean(nt_2))
print("standard deviation = %s"%stdev(nt_2))
print()

#Note production    
d_2 = ['mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf']
lp_2 = [3,1,1,1,1,1,1,1,1,1,4,1,1,2,1,1,2,1,1,1,1,4]
np_2 = note_production_list(n_2, d_2, lp_2, t_2)

plt.figure('Grade 2 Note Production')
plt.plot(list(range(1,len(n_2)+1)), np_2)            
plt.title("Grade 2 Note Production")
plt.xlabel('Progress through Piece')
plt.ylabel('Inconvenience')
ax = plt.gca()
ax.axes.xaxis.set_ticks([])
print("Grade 2 Note Production")
print("min = %s"%min(np_2))
print("max = %s"%max(np_2))
print("mean = %s"%mean(np_2))
print("standard deviation = %s"%stdev(np_2))
print()
print()


#Grade 3
#Note traversal
n_3 = ['G3','E-3','D3','C3','G3','F3','E-3','F3','G3','C4','G3','E-3','A-3','G3','D3','E-3','F3','G3','E-3','C3']
t_3 = 76
lt_3 = [1,2,1,2,1,4,1,1,1,1,1,1,1,1,0.5,0.5,0.5,0.5,1]
slur_3 = ['n','n','n','n','n','n','n','n','n','n','n','n','n','n','y','n','n','n','n']
nt_3 = note_traversal_list(n_3, t_3, lt_3, slur_3)
    
plt.figure('Grade 3 Note Traversal')
plt.plot(list(range(1,len(n_3))), nt_3)            
plt.title("Grade 3 Note Traversal")
plt.xlabel('Progress through Piece')
plt.ylabel('Inconvenience')
ax = plt.gca()
ax.axes.xaxis.set_ticks([])
print("Grade 3 Note Traversal")
print("min = %s"%min(nt_3))
print("max = %s"%max(nt_3))
print("mean = %s"%mean(nt_3))
print("standard deviation = %s"%stdev(nt_3))
print()

#Note production    
d_3 = ['p','p','p','p','p','p','p','p','p','p','p','p','p','p','p','p','p','p','p','p']
lp_3 = [1,2,1,2,1,3,1,1,1,1,1,1,1,1,0.5,0.5,0.5,0.5,1,2]
np_3 = note_production_list(n_3, d_3, lp_3, t_3)

plt.figure('Grade 3 Note Production')
plt.plot(list(range(1,len(n_3)+1)), np_3)            
plt.title("Grade 3 Note Production")
plt.xlabel('Progress through Piece')
plt.ylabel('Inconvenience')
ax = plt.gca()
ax.axes.xaxis.set_ticks([])
print("Grade 3 Note Production")
print("min = %s"%min(np_3))
print("max = %s"%max(np_3))
print("mean = %s"%mean(np_3))
print("standard deviation = %s"%stdev(np_3))
print()
print()


#Grade 4
#Note traversal
n_4 = ['F3','A3','C4','B-3','A3','G3','F3','E3','B-3','G3','E3','F3','C3','F3','G3','A3','D3','G3','E3','G3','C4','B-3','A3','F3','G3','A3','D3','G3','E3','C3','E3','F3']
t_4 = 112
lt_4 = [1,1,1,0.5,0.5,0.5,0.5,1,1,1,1,2,1,1,1,1,1,2,0.5,0.5,1,1,3,1,1,1,2,1,1,1,1]
slur_4 = ['n','n','n','y','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n',]
nt_4 = note_traversal_list(n_4, t_4, lt_4, slur_4)
    
plt.figure('Grade 4 Note Traversal')
plt.plot(list(range(1,len(n_4))), nt_4)            
plt.title("Grade 4 Note Traversal")
plt.xlabel('Progress through Piece')
plt.ylabel('Inconvenience')
ax = plt.gca()
ax.axes.xaxis.set_ticks([])
print("Grade 4 Note Traversal")
print("min = %s"%min(nt_4))
print("max = %s"%max(nt_4))
print("mean = %s"%mean(nt_4))
print("standard deviation = %s"%stdev(nt_4))
print()

#Note production    
d_4 = ['mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','f','f','f','f','f','f','f','f','f']
lp_4 = [1,1,1,0.5,0.5,0.5,0.5,1,1,1,1,2,1,1,1,1,1,2,0.5,0.5,1,1,3,1,1,1,2,1,1,1,1,3]
np_4 = note_production_list(n_4, d_4, lp_4, t_4)

plt.figure('Grade 4 Note Production')
plt.plot(list(range(1,len(n_4)+1)), np_4)            
plt.title("Grade 4 Note Production")
plt.xlabel('Progress through Piece')
plt.ylabel('Inconvenience')
ax = plt.gca()
ax.axes.xaxis.set_ticks([])
print("Grade 4 Note Production")
print("min = %s"%min(np_4))
print("max = %s"%max(np_4))
print("mean = %s"%mean(np_4))
print("standard deviation = %s"%stdev(np_4))
print()
print()


#Grade 5
#Note traversal
n_5 = ['G3','A3','F#3','G3','E-3','D3','D3','D3','E-3','E-3','F#3','F#3','G3','A3','C4','B-3','B-3','A3','B-3','A3','G3','F#3','D3','D3','E-3','E-3','F#3','F#3','G3','F#3','E-3','D3','D3','C3','D3','F#3','D3','D3','D3','C3','D3','E-3','F#3','E-3','D3']
t_5 = 76
lt_5 = [0.5,0.5,1,0.5,0.5,1.5,0.25,0.25,0.25,0.25,0.25,0.25,0.5,0.5,0.5,1,0.5,0.5,0.5,0.5,0.5,1.5,0.25,0.25,0.25,0.25,0.25,0.25,0.5,0.5,0.5,1,0.5,0.5,0.5,0.5,0.5,1.5,0.5,0.5,0.5,0.25,0.25,0.5]
slur_5 = ['y','n','n','y','n','n','n','n','n','n','n','n','y','n','y','n','n','n','n','y','n','n','n','n','n', 'n','n','n','y','n','y','n','n','n','n','y','n','n','n','n','n','y','y','n']
nt_5 = note_traversal_list(n_5, t_5, lt_5, slur_5)
    
plt.figure('Grade 5 Note Traversal')
plt.plot(list(range(1,len(n_5))), nt_5)            
plt.title("Grade 5 Note Traversal")
plt.xlabel('Progress through Piece')
plt.ylabel('Inconvenience')
ax = plt.gca()
ax.axes.xaxis.set_ticks([])
print("Grade 5 Note Traversal")
print("min = %s"%min(nt_5))
print("max = %s"%max(nt_5))
print("mean = %s"%mean(nt_5))
print("standard deviation = %s"%stdev(nt_5))
print()

#Note production    
d_5 = ['mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','p']
lp_5 = [0.5,0.5,1,0.5,0.5,1,0.25,0.25,0.25,0.25,0.25,0.25,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,1,0.25,0.25,0.25,0.25,0.25,0.25,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,1,0.5,0.5,0.5,0.25,0.25,0.5,1]
np_5 = note_production_list(n_5, d_5, lp_5, t_5)

plt.figure('Grade 5 Note Production')
plt.plot(list(range(1,len(n_5)+1)), np_5)            
plt.title("Grade 5 Note Production")
plt.xlabel('Progress through Piece')
plt.ylabel('Inconvenience')
ax = plt.gca()
ax.axes.xaxis.set_ticks([])
print("Grade 5 Note Production")
print("min = %s"%min(np_5))
print("max = %s"%max(np_5))
print("mean = %s"%mean(np_5))
print("standard deviation = %s"%stdev(np_5))
print()
print()


#Grade 6
#Note traversal
n_6 = ['D3','D4','C4','A3','G3','A-3','G3','F3','G3','F3','D3','C3','D3','D4','C4','A3','F4','E4','D4','C4','D4','C4','A-3','F3','D3','D4','C4','A3','G3','A-3','G3','F3','G3','F3','A3','C4','D4','A3','G3','F3','D3','C3','D3','G3','F3','C3','D3','D4','C4','A3','G3','A-3','G3','F3','G3','F3','D3','C3','D3','D4','F4','E4','D4','D4']
t_6 = 108
lt_6 = [1,1,0.5,1,1,0.5,0.5,0.5,0.5,0.5,0.5,0.5,1,1,0.5,1,1,0.5,0.5,0.5,0.5,0.5,0.5,0.5,1,1,0.5,1,1,0.5,0.5,0.5,0.5,0.5,0.5,0.5,1,1,0.5,1,2,0.5,0.5,0.5,0.5,0.5,1,1,0.5,1,1,0.5,0.5,0.5,0.5,0.5,0.5,0.5,1,1,0.5,1,2.5]
slur_6 = ['n','n','n','n','n','n','n','n','y','n','n','n','n','n','n','n','n','n','y','n','y','n','n','n','n','n','n','n','n','n','n','n','y' ,'n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','y','n','n','n','n','n','n','n','n']
nt_6 = note_traversal_list(n_6, t_6, lt_6, slur_6)
    
plt.figure('Grade 6 Note Traversal')
plt.plot(list(range(1,len(n_6))), nt_6)            
plt.title("Grade 6 Note Traversal")
plt.xlabel('Progress through Piece')
plt.ylabel('Inconvenience')
ax = plt.gca()
ax.axes.xaxis.set_ticks([])
print("Grade 6 Note Traversal")
print("min = %s"%min(nt_6))
print("max = %s"%max(nt_6))
print("mean = %s"%mean(nt_6))
print("standard deviation = %s"%stdev(nt_6))
print()

#Note production    
d_6 = ['mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','f','f','f','f','f','f','f','f','f','f','f','f','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','f','f','f','f','f','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','f','f','f','f','f','f']
lp_6 = [1,1,0.5,0.5,1,0.5,0.5,0.5,0.5,0.5,0.5,0.5,1,1,0.5,0.5,1,0.5,0.5,0.5,0.5,0.5,0.5,0.5,1,1,0.5,0.5,1,0.5,0.5,0.5,0.5,0.5,0.5,0.5,1,1,0.5,0.5,1.5,0.5,0.5,0.5,0.5,0.5,1,1,0.5,0.5,1,0.5,0.5,0.5,0.5,0.5,0.5,0.5,1,1,0.5,1,1.5,1]
np_6 = note_production_list(n_6, d_6, lp_6, t_6)

plt.figure('Grade 6 Note Production')
plt.plot(list(range(1,len(n_6)+1)), np_6)            
plt.title("Grade 6 Note Production")
plt.xlabel('Progress through Piece')
plt.ylabel('Inconvenience')
ax = plt.gca()
ax.axes.xaxis.set_ticks([])
print("Grade 6 Note Production")
print("min = %s"%min(np_6))
print("max = %s"%max(np_6))
print("mean = %s"%mean(np_6))
print("standard deviation = %s"%stdev(np_6))
print()
print()


#Grade 7
#Note traversal
n_7 = ['G3','F#3','G3','A3','B3','A3','B3','C4','D4','B3','E4','C4','A3','D4','B3','G3','D3','G3','F#3','G3','A3','B3','A3','B3','C4','D4','C4','D4','E4','F#4','E4','D4','C4','B3','C4','D4','C4','B3','A3','B3','A3','F#3','D3','D3','D3','D3','F#3','D3','A3','F#3','C4','A3','F#3','C4','A3','E4','C4','A3','E4','D4','C4','A3','G3','F#3','E3','D3','G3','F#3','G3','A3','B3','A3','B3','C4','D4','B3','E4','C4','A3','G3','A3','B3','C4','B3','C4','D4','E4','D4','C4','D4','E4','D4','E4','F#4','G4']
t_7 = 112
lt_7 = [0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.5,0.5,1,0.5,0.5,1,0.5,0.5,1,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.5,0.25,0.25,0.5,0.5,0.5,0.5,0.5,0.5,2.75,0.25,0.75,0.25,0.5,0.5,0.5,0.5,2,0.5,0.5,0.5,0.5,2,0.5,0.5,0.5,0.25,0.25,1.75,0.25,1.75,0.25,2,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.5,0.5,0.5,0.5,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25]
slur_7 = ['y','n','n','n','y','n','n','n','n','n','n','n','n','n','n','n','n','y','n','n','n','y','n','n','n','y','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','y','n','n','n','y','n','n','n','n','n','n','n','y','n','n','n','y','n','n','n','y','n','n','n','n','n','n','n']
nt_7 = note_traversal_list(n_7, t_7, lt_7, slur_7)
    
plt.figure('Grade 7 Note Traversal')
plt.plot(list(range(1,len(n_7))), nt_7)            
plt.title("Grade 7 Note Traversal")
plt.xlabel('Progress through Piece')
plt.ylabel('Inconvenience')
ax = plt.gca()
ax.axes.xaxis.set_ticks([])
print("Grade 7 Note Traversal")
print("min = %s"%min(nt_7))
print("max = %s"%max(nt_7))
print("mean = %s"%mean(nt_7))
print("standard deviation = %s"%stdev(nt_7))
print()

#Note production    
d_7 = ['mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','f','f','f','f','f','f','f','f','f','f','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','f','f','f','f','f','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','mf','f']
lp_7 = [0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.5,0.5,1,0.5,0.5,1,0.5,0.5,1,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.5,0.25,0.25,0.5,0.5,0.5,0.5,0.5,0.5,2,0.25,0.75,0.25,0.5,0.5,0.5,0.5,1,0.5,0.5,0.5,0.5,1,0.5,0.5,0.5,0.25,0.25,1.75,0.25,1.75,0.25,2,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.5,0.5,0.5,0.5,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,2]
np_7 = note_production_list(n_7, d_7, lp_7, t_7)

plt.figure('Grade 7 Note Production')
plt.plot(list(range(1,len(n_7)+1)), np_7)            
plt.title("Grade 7 Note Production")
plt.xlabel('Progress through Piece')
plt.ylabel('Inconvenience')
ax = plt.gca()
ax.axes.xaxis.set_ticks([])
print("Grade 7 Note Production")
print("min = %s"%min(np_7))
print("max = %s"%max(np_7))
print("mean = %s"%mean(np_7))
print("standard deviation = %s"%stdev(np_7))
print()
print()


#Grade 8
#Note traversal
n_8 = ['F3','C4','D4','E-4','C4','A-3','F3','D-4','C-4','F3','G3','A-3','F3','A-3','B-3','C-4','A-3','B-3','C4','D4','E-4','F4','G4','E-4','B3','C4','G3','G3','D3','E-3','B2','C3','B2','C3','F3','G3','A-3','F3','G3','C4','D4','E-4','C4','F4','B-3','C4','D4','B-3','E-4','E-3','F3','G3','E-3','B-3','B-2','C3','D3','B-2','C3','F3','G3','A-3','F3','C4','E3','F3','G3','A-3','G3','A-3','B-3','E3','F3','E3','F3','E3','F3','E3','F3','E3','D3','E3','F3']
t_8 = 216
lt_8 = [2,1.5,0.5,1,1,1,1,2,5,0.5,0.5,0.5,0.5,0.5,0.5,3,0.5,0.5,0.5,0.5,0.5,0.5,2.5,0.5,0.5,0.5,2.5,0.5,0.5,0.5,1,2,1,2.5,0.25,0.25,0.5,0.5,0.5,0.25,0.25,0.5,0.5,0.5,0.25,0.25,0.5,0.5,0.5,0.25,0.25,0.5,0.5,0.5,0.25,0.25,0.5,0.5,0.5,0.25,0.25,0.5,0.5,2.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,1,0.5,0.5]
slur_8 = ['n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n','n']
nt_8 = note_traversal_list(n_8, t_8, lt_8, slur_8)
    
plt.figure('Grade 8 Note Traversal')
plt.plot(list(range(1,len(n_8))), nt_8)            
plt.title("Grade 8 Note Traversal")
plt.xlabel('Progress through Piece')
plt.ylabel('Inconvenience')
ax = plt.gca()
ax.axes.xaxis.set_ticks([])
print("Grade 8 Note Traversal")
print("min = %s"%min(nt_8))
print("max = %s"%max(nt_8))
print("mean = %s"%mean(nt_8))
print("standard deviation = %s"%stdev(nt_8))
print()

#Note production    
d_8 = ['mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp', 'mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp', 'mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp', 'mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp','mp']
lp_8 = [2,1,0.5,1,1,1,1,2,2,0.5,0.5,0.5,0.5,0.5,0.5,2,0.5,0.5,0.5,0.5,0.5,0.5,2,0.5,0.5,0.5,2,0.5,0.5,0.5,1,2,1,2,0.25,0.25,0.5,0.5,0.5,0.25,0.25,0.5,0.5,0.5,0.25,0.25,0.5,0.5,0.5,0.25,0.25,0.5,0.5,0.5,0.25,0.25,0.5,0.5,0.5,0.25,0.25,0.5,0.5,2.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,1,0.5,0.5,4] 
np_8 = note_production_list(n_8, d_8, lp_8, t_8)

plt.figure('Grade 8 Note Production')
plt.plot(list(range(1,len(n_8)+1)), np_8)            
plt.title("Grade 8 Note Production")
plt.xlabel('Progress through Piece')
plt.ylabel('Inconvenience')
ax = plt.gca()
ax.axes.xaxis.set_ticks([])
print("Grade 8 Note Production")
print("min = %s"%min(np_8))
print("max = %s"%max(np_8))
print("mean = %s"%mean(np_8))
print("standard deviation = %s"%stdev(np_8))