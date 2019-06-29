import random
import statistics

# Death March points to kill a character
#DM_MAX = 13
DM_MAX = 10

# Lookup table for Age Points/Death March Levels
XP_TABLE = [1, 3, 6, 10, 15, 21, 28, 36, 45, 55, 66, 78, 91, 105, 120]

# Lifestyle descriptions and modifiers for [Impoverished, Poor, Comfortable, Prosperous, Rich, Extravagent]
LIFESTYLE_DESC  = ["Impoverished", "Poor", "Comfortable", "Prosperous", "Rich", "Extravagent"]
#27 JUNE DISCORD
LIFESTYLE_TABLE = [3, 1, 0, -1, -3, -5]
#Alpha rules
#LIFESTYLE_TABLE = [2, 1, 0, -1, -2, -3]
#test?
#LIFESTYLE_TABLE = [4, 2, 1, 0, -1, -3]

# Kith descriptions and age tables for [Adult, Middle Aged, Old, Venerable]
KITH_DESC = ["Anuma", "Dwarf", "Elf" , "Folk" , "Orlan"]
KITH = [[39,57,75,97], [61,95,121,151], [101,151,197,251], [33,49,65,81], [27,40,52,65]]

# Age Modifiers for [Adult, Middle Aged, Old, Venerable]
AGE_TABLE = [0, 2, 5, 8]

# Set number of runs per Race/Lifestyle combo
RUNS = 10000
print ("Runs:", RUNS)

# Run for each type of kith in range(a,b)
# 0 = Anuma , 1 = Dwarf , 2 = Elf , 3 = Folk , 4 = Orlan
for k in range(0, 5):
	print ("===================================")
	print (KITH_DESC[k])
	print ("-----------------------------------")
	
	# Set Kith age brackets 
	ADULT  = KITH[k][0]
	MIDDLE = KITH[k][1]
	OLD    = KITH[k][2]
	VEN    = KITH[k][3]

	# Run for each lifestyle type
	for l in range(0, 6):
		# Set lifestyle modifier
		LIFE_MOD = LIFESTYLE_TABLE[l]
		# Clear lifestyle stats
		AGE_STATS = []
		ROLL_STATS = []
		MALADY_STATS = []
		MALADY_SERIOUS_STATS = []
		MALADY_DEATH = 0
	
		# Simulate x runs
		for x in range(0, RUNS):
			# Reset run 
			DM = 0
			AGE_PTS = 0
			AGE_MOD = AGE_TABLE[0]
			# Set age prior to adult
			AGE = ADULT - 1
			AGE_APPARENT = AGE
			# Clear maladies
			MALADIES = [0,0,0,0,0]
			
			# Run until Death March hits limit
			while DM < DM_MAX:
				# Reset Age Point comparator
				POINTCHECK = AGE_PTS
				# Clear malady
				MALADY = False
				# Age the character
				AGE += 1
				# +1 year Apparent Aging
				AGE_APPARENT += 1
				
				# Check Age Modifier
				if   AGE >= VEN:	AGE_MOD = AGE_TABLE[3]
				elif AGE >= OLD:	AGE_MOD = AGE_TABLE[2]
				elif AGE >= MIDDLE:	AGE_MOD = AGE_TABLE[1]
					
				# Roll the dice
				# ROLL = 1d12 + Age Modifier + Lifestyle modifier
				ROLL = random.randint(1,12) + AGE_MOD + LIFE_MOD
				
				if ROLL <= 3:
					# No apparent aging
					AGE_APPARENT -= 1
				
				elif 10 <= ROLL <= 12:
					# 1 Aging Point in any Attribute
					AGE_PTS += 1
				
				elif ROLL == 13:
					# Advance Death March by 2
					# +2 years additional Apparent Aging
					# Set Aging Points per XP table
					# Assign a malady
					#DM += 2
					DM += 1
					AGE_APPARENT += 2
					AGE_PTS = XP_TABLE[DM - 1]
					MALADY = True
				
				elif 14 <= ROLL <= 19:
					# 2 Aging Points in a single Attribute			
					AGE_PTS += 2
				
				elif ROLL == 20:
					# Advance Death March by 2
					# +2 years additional Apparent Aging
					# Set Aging Points per XP table
					# Assign a malady
					#DM += 2
					DM += 1
					AGE_APPARENT += 2
					AGE_PTS = XP_TABLE[DM - 1]
					MALADY = True
				
				elif 21 <= ROLL <= 22:
					# 2 Aging Points in a three Attributes (6 total)
					# +1 year additional Apparent Aging
					AGE_PTS += 6
					AGE_APPARENT += 1
				
				elif ROLL >= 23:
					# 2 Aging Points in a six Attributes (12 total)
					# +1 year additional Apparent Aging				
					AGE_PTS += 12
					AGE_APPARENT += 1
	
				# Check if Age Points were incremented this year
				if AGE_PTS > POINTCHECK:
					# Lookup current Death March in XP Table
					for index,xp in enumerate(XP_TABLE):
						if AGE_PTS >= xp: DM = (index+1)
				
				# Resolve Malady
				if MALADY:
					# Roll for malady type
					# MAL_ROLL = 2d10 + Age Modifier + Death March
					MAL_ROLL = random.randint(1,10) + random.randint(1,10) + AGE_MOD + DM
					
					if   MAL_ROLL >= 26:
						#Critical Malady
						MALADIES[4] += 1
						SAVING_THROW = 21
						
					elif MAL_ROLL >= 23:
						#Serious Malady
						MALADIES[3] += 1	
						SAVING_THROW = 15

					elif MAL_ROLL >= 20:	
						#Minor Malady
						MALADIES[2] += 1	
						SAVING_THROW = 9
						
					elif MAL_ROLL >= 14:
						#1 Month Incapacitation	
						MALADIES[1] += 1
						SAVING_THROW = 0
						
					else:
						#1 Week Incapacitation 					
						MALADIES[0] += 1
						SAVING_THROW = 0
						
					# Roll for recovery (if not outright killed by 13/20)
					# Recovery Roll = 2d10 + Herbalism + Surgery + Constitution	
					RECOVERY_ROLL = random.randint(1,10) + random.randint(1,10) + (5) + (5) + (3)
					if DM < 13 and RECOVERY_ROLL < SAVING_THROW: 
						DM = 20
						MALADY_DEATH += 1
					
				# DEBUG: STEP RUN BY YEAR
				#print ( AGE, AGE_APPARENT, DM, AGE_PTS, roll, AGE_MOD, LIFE_MOD, MALADIES[4], MALADIES[3], MALADIES[2], MALADIES[1], MALADIES[0])
			
			# Collect run stats
			AGE_STATS.append(AGE)
			ROLL_STATS.append(ROLL)
			MALADY_STATS.append(sum(MALADIES))
			MALADY_SERIOUS_STATS.append(MALADIES[4] + MALADIES[3])
		
		#Print Stats per Lifestyle
		REAPED = ROLL_STATS.count(13) + ROLL_STATS.count(20)
		print ( LIFESTYLE_DESC[l] , "| Average age:" , round(statistics.mean(AGE_STATS),1) , "| Stdev:", round(statistics.stdev(AGE_STATS),1) )
		print ( "    Reaping percentage:" , round((REAPED / RUNS * 100),1) , " | Average roll:" , round(statistics.mean(ROLL_STATS),1) )
		print ( "    Malady avg:", round(statistics.mean(MALADY_STATS),1) , "| Serious+:", round(statistics.mean(MALADY_SERIOUS_STATS),1) , "| Fatal Malady%:" , round(MALADY_DEATH / RUNS * 100, 1))
# End