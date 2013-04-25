import random
import epdb 

SEARCHNUM=7
POOLSIZE=150
ACSUM=13
CCSUM=17
PNSUM=19
SEVENS=2
ZEROES=0
FIRSTNUM=7
SIXTHNUM=4
THIRDNUM=5
FOURTHNUM=6
GENERATIONS=2000
TC=0 
MUTATIONRATE=0.120

def number_count(searchnum,phone):
	count=0
	phone=str(phone)
	for letter in phone:
		if str(searchnum)==str(letter):
			count+=1
	return count
def check_place(place,number):
	number=str(number)
	RETCODE=0
	if place==3 and number[2]==THIRDNUM:
		RETCODE=0
	elif place==4 and number[3]==FOURTHNUM:
		RETCODE=0
	elif place==1 and number[0]==FIRSTNUM:
		RETCODE=0
	elif place==6 and number[5]==SIXTHNUM:
		RETCODE=0
	else:
		RETCODE=1

	return RETCODE
def sum(numb,type):
	numb=str(numb)
#	print numb
	asum=0
	try:
		if type=='AC':
			asum=int(numb[0])+int(numb[1])+int(numb[2])
			DISTANCE=abs(asum-ACSUM)
		elif type=='CC':
			asum=int(numb[3])+int(numb[4])+int(numb[5])
			DISTANCE=abs(asum-CCSUM)
		elif type=='PN':
			asum=int(numb[6])+int(numb[7])+int(numb[8])+int(numb[9])
			DISTANCE=abs(asum-PNSUM)
	except IndexError:
		DISTANCE=999		
	except ValueError:
		DISTANCE=999			
	return DISTANCE

def perform_xbreed(NUMLIST,FIRST_VALUE,SECOND_VALUE):
	NEW_VALUE=[]
	FIRST_VALUE=str(FIRST_VALUE)
	SECOND_VALUE=str(SECOND_VALUE)
	XOVERSPOT=random.randint(0,9)
	HEADER=str(FIRST_VALUE[0:XOVERSPOT])
	FOOTER=str(SECOND_VALUE[XOVERSPOT:11]).zfill(11-XOVERSPOT)
	return str(HEADER)+str(FOOTER)

def finalize_dchanges(NUMLIST,NEWVALUES,OLDVALUES):
	for val in OLDVALUES:
		try:
			del(NUMLIST[val])
		except KeyError:
			pass
	for val in NEWVALUES:
		NUMLIST[val]=0

	return NUMLIST

def crossbreed(MINDIST,NUMLIST,MATCHLIST):
	DONE=0
	FIRST_VALUE_SET=False
	SECOND_VALUE_SET=False
	NEWVALUES=[]
	OLDVALUES=[]
	MINDIST,COUNT,MATCHLIST=find_best(NUMLIST,MINDIST,MATCHLIST)
	for row in NUMLIST:
		try:
			SDEX=random.randint(0,len(MATCHLIST)-1)
		except ValueError:
			SDEX=0
		if NUMLIST[row] > (MINDIST+1):
			if  random.random() < MUTATIONRATE:
				NEWVAL=mutate(NUMLIST,MATCHLIST)
				if len(NEWVAL)< 10:
					epdb.st()
					NEWVALUES.append(NEWVAL) 
			elif random.randint(0,1)==0:
				NEWVALUES.append(perform_xbreed(NUMLIST,MATCHLIST[SDEX],row))
			else:
				NEWVALUES.append(perform_xbreed(NUMLIST,row,MATCHLIST[SDEX]))
				
			OLDVALUES.append(row)
		if len(str(row)) < 10:
			OLDVALUES.append(row)
	SECOND_VALUE_SET=False
	FIRST_VALUE_SET=False
	#print NEWVALUES
	#Now do actual list replacements
	NUMLIST=finalize_dchanges(NUMLIST,NEWVALUES,OLDVALUES)

	return NUMLIST,MATCHLIST

def mutate(NUMLIST,MATCHLIST):
	SEED=random.randint(0,len(MATCHLIST)-1)
	FIRST_VALUE=str(MATCHLIST[SEED])
	MUTATESPOT=random.randint(1,8)
	NEWSPOT=MUTATESPOT+1
	NEWVAL=random.randint(0,9)
	HEADER=FIRST_VALUE[0:MUTATESPOT]
	FOOTER=FIRST_VALUE[NEWSPOT:10]
	if NEWVAL==10:
		NEWVAL=9
	
	return HEADER+str(NEWVAL)+FOOTER

def calc_distances(NUMLIST):
	TOTDISTANCE=0
	DISTANCE=0
	for item in NUMLIST:
		NUMLIST[item]=0
	for phone in NUMLIST:
		DISTANCE=0
		if len(phone)>9:
			DISTANCE=sum(phone,'AC')
			DISTANCE+=sum(phone,'CC')
			DISTANCE+=sum(phone,'PN')
			DISTANCE+=number_count(7,phone)
			DISTANCE+=number_count(0,phone)
			DISTANCE+=check_place(3,phone)
			DISTANCE+=check_place(4,phone)
			DISTANCE+=check_place(1,phone)
			DISTANCE+=check_place(6,phone)
			NUMLIST[phone]=DISTANCE
			TOTDISTANCE+=DISTANCE
			if NUMLIST[phone]==0:
				print "possible match! "+str(phone)
		else:
			DISTANCE=999
	return NUMLIST,TOTDISTANCE

def find_best(NUMLIST,MINDIST,MATCHLIST):
	COUNT=0
	TCOUNT=0
	for row in NUMLIST:
		TCOUNT+=1
		if len(row)==10:
			COUNT+=1
			if NUMLIST[row] < MINDIST:
				MATCHLIST=[]
				MINDIST=NUMLIST[row]
				MATCHLIST.append(row)
				COUNT=1
			elif NUMLIST[row] == MINDIST:
				MATCHLIST.append(row)
				MINDIST=NUMLIST[row]
				COUNT+=1
#	print str(COUNT)+" / "+str(TCOUNT)
	return MINDIST,COUNT,MATCHLIST
	
def gen_initial_numbers(TC):
	for a in range(0,POOLSIZE+5):
		number=str(random.randint(1000000000,9999999999))
		ac="%03d" % (random.randint(100,999),)
		cc="%03d" % (random.randint(100,999),)
		nc="%04d" % (random.randint(0,9999),)
		TC+=1
		NUMLIST[str(ac)+str(cc)+str(nc)]=0

	return NUMLIST
def gen_new_members(NUMLIST,POOLSIZE,CURSIZE,MATCHLIST):
	TOTAL=0
	ml_LENGTH=len(MATCHLIST)
	ml_SPOT=random.randint(0,9)
	for a in range(CURSIZE,POOLSIZE+1):
		ml_SPOT=random.randint(0,9)
		ac="%03d" % (random.randint(100,999),)
		cc="%03d" % (random.randint(100,999),)
		pn="%04d" % (random.randint(0,9999),)
		number=str(ac)+str(cc)+str(pn)
		NUMLIST[number]=0
		TOTAL+=1
	return NUMLIST,TOTAL
def print_matches(NUMLIST,MINDIST):
	for row in NUMLIST:
		if NUMLIST[row]==MINDIST:
			print row+'\n'

	return


NUMLIST={}
NUMLIST=gen_initial_numbers(TC)
NUMLIST,TOTDISTANCE=calc_distances(NUMLIST)
MINDIST=100
MATCHLIST=[]
CHANGETOTAL=0
MINDIST,COUNT,MATCHLIST=find_best(NUMLIST,MINDIST,MATCHLIST)
print "Initially "+str(len(MATCHLIST))+" matches in MATCHLIST"
print MINDIST,COUNT
print NUMLIST
for generation in range(0,GENERATIONS):
	NUMLIST,MATCHLIST=crossbreed(MINDIST,NUMLIST,MATCHLIST)
	NUMLIST,TOTDISTANCE=calc_distances(NUMLIST)
	MINDIST,COUNT,MATCHLIST=find_best(NUMLIST,MINDIST,MATCHLIST)
	if len(NUMLIST) < POOLSIZE:
		NUMLIST,CHANGETOTAL=gen_new_members(NUMLIST,POOLSIZE,len(NUMLIST),MATCHLIST)
	if (generation % 200)==0:
		print "Generation "+str(generation)+" completed, average distance of "+str(TOTDISTANCE)+", MINDIST= "+str(MINDIST)+", Changes:"+str(CHANGETOTAL)
	

NUMLIST,TOTDISTANCE=calc_distances(NUMLIST)
print NUMLIST
	


print "The best distance is "+str(MINDIST)+". "+str(COUNT)+" of these records exist."
print MATCHLIST
