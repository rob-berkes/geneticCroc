import random
import epdb 
import sys

MAXMATCHSIZE=100
GENERATIONS=1000
MUTATIONRATE=0.250
TABURATE=0.25
POOLSIZE=1000
APPENDS=POOLSIZE
NUMRUNS=100

PHONENUM="6084444496"
ACSUM=14
CCSUM=12
PNSUM=23
SEVENS=0
EIGHTS=1
NINES=1
ONES=0
TWOS=0
FIVES=0
ZEROES=1

FIRSTNUM=6
SECONDNUM=0
THIRDNUM=8
FOURTHNUM=4
FIFTHNUM=4
SIXTHNUM=4
EIGHTHNUM=4
TENTHNUM=6
TC=0
 
MINDIST=100
MATCHLIST={}

CROSSLIMIT=3


def number_count(searchnum,phone,numcount):
	count=0
	phone=str(phone)
	for letter in phone:
		if str(searchnum)==str(letter):
			count+=1
	return abs(numcount-count)
def check_places(number):
	number=str(number)
	RETCODE=0
#	epdb.st()
	if number[2]!=str(THIRDNUM):
		RETCODE+=1
	if number[1]!=str(SECONDNUM):
		RETCODE+=1
#	if number[3]!=str(FOURTHNUM):
#		RETCODE+=1
	if number[0]!=str(FIRSTNUM):
		RETCODE+=1
	if number[5]!=str(SIXTHNUM):
		RETCODE+=1
	if number[4]!=str(FIFTHNUM):
		RETCODE+=1
	if number[7]!=str(EIGHTHNUM):
		RETCODE+=1
	if number[9]!=str(TENTHNUM):
		RETCODE+=1

	return RETCODE
def sum(numb,type):
	numb=str(numb)
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
	FIRST_VALUE=str(FIRST_VALUE)
	SECOND_VALUE=str(SECOND_VALUE)
	XOVERSPOT=random.randint(0,9)
	HEADER=str(FIRST_VALUE[0:XOVERSPOT])
	FOOTER=str(SECOND_VALUE[XOVERSPOT+1:10]).zfill(10-XOVERSPOT)
	return str(HEADER)+str(FOOTER)

def zero_numlist(NUMLIST):
	for a in NUMLIST:
		NUMLIST[a]=0
	return NUMLIST

def finalize_dchanges(NUMLIST,NEWVALUES,OLDVALUES):
	for val in OLDVALUES:
		try:
			del(NUMLIST[val])
		except KeyError:
			pass
#DON'T REMOVE BELOW FOR LOOP IF YOURE GETTING THAT IDEA! 
	for a in NEWVALUES:
		NUMLIST[a]=0
	NUMLIST=zero_numlist(NUMLIST)
	return NUMLIST
def tabu_swap(NUMLIST,row1,row2):
	#OFILE=open("/tmp/tabu.log","a")
	#crossbreed one child all times, using all pivots
	#calculate scores, take best
	RESULT=""
	BESTSCORE=100
	for a in range(1,9):
		RESULT1=str(row1[0:a])
		RESULT2=str(row2[a:10])
		NEWRES=RESULT1+RESULT2	
		NEWSCORE=calc_score(NEWRES)
		#OFILE.write(str(NEWSCORE)+" , "+str(NEWRES)+"\n")
		if NEWSCORE < BESTSCORE:
			RESULT=NEWRES
			BESTSCORE=NEWSCORE
	#OFILE.write("Best: "+str(BESTSCORE)+", for "+str(NEWRES)+"\n")
	#OFILE.close()
	return RESULT,BESTSCORE

def choose_swap_method(NUMLIST,MATCHLIST,row,APPENDS,NEWVALUES):
	try:
		SDEX=random.randint(0,int(len(MATCHLIST)-1))
	except :
		SDEX=0
	NEWSEED=SDEX
	if len(MATCHLIST) > 1:
		MUTATE=random.random()
		if MUTATE < MUTATIONRATE:
			NEWVALUES.append(mutate(NUMLIST,MATCHLIST,row))
			APPENDS+=1
		elif random.random() < TABURATE:
			SDEX=random.randint(0,int(len(MATCHLIST)-1))
			NEWVAL,BESTSCORE=tabu_swap(NUMLIST,row,MATCHLIST[SDEX])
		else:
			while NEWSEED==SDEX:
				NEWSEED=random.randint(0,int(len(MATCHLIST))-1)
			NERO=random.randint(0,1)
			if NERO==1:
				NEWVALUES.append(perform_xbreed(NUMLIST,row,MATCHLIST[NEWSEED]))
			else:
				NEWVALUES.append(mutate_threep(NUMLIST,MATCHLIST,row))
			APPENDS+=1
	else:
		NEWVALUES.append(perform_xbreed(NUMLIST,MATCHLIST[SDEX],row))
		APPENDS+=1
	return NEWVALUES,APPENDS

def crossbreed(MINDIST,NUMLIST,MATCHLIST,APPENDS):
	NEWVALUES=[]
	OLDVALUES=[]
	for row in NUMLIST:
		if len(str(row)) > 10:
			OLDVALUES.append(row)
			epdb.st()
		elif len(str(row)) < 9:
			OLDVALUES.append(row)
			epdb.st()
		try:
			SDEX=random.randint(0,int(len(MATCHLIST))-1)
		except ValueError:
			SDEX=0
		if NUMLIST[row] > (MINDIST+CROSSLIMIT) :
			NEWVALUES,APPENDS=choose_swap_method(NUMLIST,MATCHLIST,row,APPENDS,NEWVALUES)
			OLDVALUES.append(row)
			APPENDS+=1 
		else:
			if random.random()<MUTATIONRATE:
				if in_matchlist(MATCHLIST,row):
					pass
				else:
					OLDVALUES.append(row)
					NEWVAL=mutate(NUMLIST,MATCHLIST,row)
					NEWVALUES.append(NEWVAL)
					APPENDS+=1
	NUMLIST=finalize_dchanges(NUMLIST,NEWVALUES,OLDVALUES)
	return NUMLIST,APPENDS,len(NEWVALUES),len(OLDVALUES)

def mutate(NUMLIST,MATCHLIST,row):
	SEED=random.randint(0,len(MATCHLIST)-1)
	FIRST_VALUE=str(MATCHLIST[SEED])
	MUTATESPOT=random.randint(0,8)
	NEWSPOT=MUTATESPOT+1
	NEWVAL=random.randint(0,9)
	HEADER=FIRST_VALUE[0:MUTATESPOT]
	FOOTER=row[NEWSPOT:10].zfill(10-NEWSPOT)
	RETSTR=HEADER+str(NEWVAL)+FOOTER
			
	return RETSTR

def mutate_threep(NUMLIST,MATCHLIST,row):
	SEED=random.randint(0,len(MATCHLIST)-1)
	SEED2=random.randint(0,len(MATCHLIST)-1)
	while SEED2==SEED:
		SEED2=random.randint(0,len(MATCHLIST)-1)
	FIRST_VALUE=str(MATCHLIST[SEED])
	SECOND_VALUE=str(MATCHLIST[SEED2])
	MUTATESPOT1=random.randint(0,8)
	MUTATESPOT2=random.randint(MUTATESPOT1,len(row))
	HEADER=FIRST_VALUE[0:MUTATESPOT1]
	SECOND=SECOND_VALUE[MUTATESPOT1:MUTATESPOT2]
	FOOTER=row[MUTATESPOT2:10].zfill(10-MUTATESPOT2)
#	OFILE=open('mutate3p.log','a')
#	OFILE.write(HEADER+SECOND+FOOTER+"\n")
#	OFILE.close()
	RETSTR=HEADER+SECOND+FOOTER
			
	return RETSTR

def calc_score(row):
	TOTDISTANCE=0
	DISTANCE=0
	DISTANCE=0
	if len(row)>9:
		DISTANCE=sum(row,'PN')
		DISTANCE+=sum(row,'CC')
		DISTANCE+=sum(row,'AC')
		DISTANCE+=number_count(7,row,SEVENS)
		DISTANCE+=number_count(0,row,ZEROES)
		DISTANCE+=number_count(8,row,EIGHTS)
		DISTANCE+=number_count(5,row,FIVES)
		DISTANCE+=number_count(2,row,TWOS)
		DISTANCE+=number_count(1,row,ONES)
		DISTANCE+=number_count(9,row,NINES)
		DISTANCE+=check_places(row)
		TOTDISTANCE+=DISTANCE
	else:
		TOTDISTANCE=999
	return TOTDISTANCE
def calc_distances(NUMLIST):
	TOTDISTANCE=0
	DISTANCE=0
	NUMLIST=zero_numlist(NUMLIST)
	for phone in NUMLIST:
		DISTANCE=0
		if len(phone)>9:
			DISTANCE=sum(phone,'PN')
			DISTANCE+=sum(phone,'CC')
			DISTANCE+=sum(phone,'AC')
			DISTANCE+=number_count(7,phone,SEVENS)
			DISTANCE+=number_count(0,phone,ZEROES)
			DISTANCE+=number_count(8,phone,EIGHTS)
			DISTANCE+=number_count(5,phone,FIVES)
			DISTANCE+=number_count(2,phone,TWOS)
			DISTANCE+=number_count(1,phone,ONES)
			DISTANCE+=number_count(9,phone,NINES)
			DISTANCE+=check_places(phone)
			NUMLIST[phone]=DISTANCE
			TOTDISTANCE+=DISTANCE
		else:
			DISTANCE=999
	return NUMLIST,TOTDISTANCE
def choose_to_add(MATCHLIST,row,COUNT):
	INLIST=False
	try:
		for a in MATCHLIST:
			if a == row:
				INLIST=True
	except TypeError:
		MATCHLIST=[]
	if INLIST:
		pass
	else:
		MATCHLIST.append(row)
		COUNT+=1

	return MATCHLIST,COUNT
def in_matchlist(MATCHLIST,row):
	found=False
	for a in MATCHLIST:
		if a==row:
			found=True
	return found

def trim_matchlist(NUMLIST,MATCHLIST,newlow):
	limit=newlow+2
	newlist=[]
	for a in MATCHLIST:
		try:
			if NUMLIST[a] < limit:
				newlist.append(a)			 
		except KeyError:
			pass
	return newlist
def find_best(NUMLIST,MINDIST,MATCHLIST,OLDLOW):
	COUNT=0
	for row in NUMLIST:
		if COUNT > MAXMATCHSIZE :
			break
		if len(row)==10:
			if NUMLIST[row] < MINDIST:
				MATCHLIST=trim_matchlist(NUMLIST,MATCHLIST,NUMLIST[row])
				OLDLOW=MINDIST
				MINDIST=NUMLIST[row]
				MATCHLIST.append(row)
				COUNT=1
			elif NUMLIST[row] <= MINDIST+1:
				MATCHLIST,COUNT=choose_to_add(MATCHLIST,row,COUNT)
	return MINDIST,COUNT,MATCHLIST,OLDLOW
	
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
		if ml_LENGTH>1:
			SDEX2=random.randint(0,len(MATCHLIST)-1)
			NEWVAL=mutate(NUMLIST,MATCHLIST,MATCHLIST[SDEX2])
			NUMLIST[NEWVAL]=0
			TOTAL+=1
		else:
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






OFILE=open("results.log","a")
for POOLSIZE in [1000,500]:
	for TABURATE in [0.25,0.05]:
		for RUNNUM in range(1,NUMRUNS):
			APPENDS=0
			FOUND=False
			NUMLIST={}
			MATCHLIST=[]
			MINDIST=100
			NUMLIST=gen_initial_numbers(TC)
			NUMLIST,TOTDISTANCE=calc_distances(NUMLIST)
			CHANGETOTAL=0
			OLDLOW=0
			random.seed()
			MINDIST,COUNT,MATCHLIST,OLDLOW=find_best(NUMLIST,MINDIST,MATCHLIST,OLDLOW)
			print "Initially "+str(len(MATCHLIST))+" matches, MINDIST "+str(MINDIST)
			for generation in range(0,GENERATIONS):
				NUMLIST,TOTDISTANCE=calc_distances(NUMLIST)
				MINDIST,COUNT,MATCHLIST,OLDLOW=find_best(NUMLIST,MINDIST,MATCHLIST,OLDLOW)
				NUMLIST,APPENDS,LENNEW,LENOLD=crossbreed(MINDIST,NUMLIST,MATCHLIST,APPENDS)
				if len(NUMLIST) < POOLSIZE:
					NUMLIST,CHANGETOTAL=gen_new_members(NUMLIST,POOLSIZE,len(NUMLIST),MATCHLIST)
				for a in MATCHLIST:
					if FOUND==True:
						break
					if str(a)==PHONENUM:
						FOUND=True
						OFILE.write(str(generation)+","+str(APPENDS)+","+str(MUTATIONRATE)+","+str(TABURATE)+","+str(POOLSIZE)+","+str(MAXMATCHSIZE)+"\n")
						print "MATCH! Generation "+str(generation)+", "+str(APPENDS)+" numbers ,NEWVALUES "+str(LENNEW)+" OLDVALUES "+str(LENOLD)+" length "+str(len(NUMLIST))+", matchlist of "+str(len(MATCHLIST))+", OLDLOW= "+str(OLDLOW)+" MINDIST= "+str(MINDIST)+", random children added:"+str(CHANGETOTAL)
			#	if (generation % 200)==0:
			#		print "Generation "+str(generation)+", "+str(APPENDS)+" numbers ,NEWVALUES "+str(LENNEW)+" OLDVALUES "+str(LENOLD)+" length "+str(len(NUMLIST))+", matchlist of "+str(len(MATCHLIST))+", OLDLOW= "+str(OLDLOW)+" MINDIST= "+str(MINDIST)+", random children added:"+str(CHANGETOTAL)
					#print "The best distance is "+str(MINDIST)+". "+str(len(MATCHLIST))+" of these records exist."
					#print MATCHLIST
				if FOUND==True:
					break
				elif generation>=(GENERATIONS-1):
					OFILE.write(str(generation)+",0,"+str(MUTATIONRATE)+","+str(TABURATE)+","+str(POOLSIZE)+","+str(MAXMATCHSIZE)+"\n")
	
		
			

OFILE.close()
