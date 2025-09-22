thinks_of_chain = '''
TIER DETERMINATION							
							
Determine the Step 1 Factor:							
"Determine AA value in Matrix AA using Tenure with the Company and Number of Eligible-to-be-Rated Drivers. 
Determine AB value in Matrix AB using Total Novo Claim Count and Total Novo Violation Count. 
Determine AC value in Matrix AC using Matrix AA Value and Matrix AB Value.
Determine AD value in Matrix AD using Matrix AC Value and Risk Group.
Determine AE value in Matrix AE using Non-Novo AAF Count and Novo DWI Count. 
Determine AF value in Matrix AF using Non-Novo DWI Count and Novo MIN Count. 
Determine AG value in Matrix AG using Matrix AE Value and Matrix AF Value.
Look up the factor in the Step 1a Factor Table using Matrix AD Value and Matrix AG Value."							
"Determine AH value in Matrix AH using Non-Novo MAJ Count and Novo AAF Count.
Determine AI value in Matrix AI using Non-Novo SPD Count and Permissive Use At-Fault Accidents Count. 
Determine AJ value in Matrix AJ using Matrix AH Value and Matrix AI Value.
Look up the factor in the Step 1b Factor Table using Matrix AD Value and Matrix AJ Value."							
"Determine AK value in Matrix AK using Non-Novo MIN Count and Permissive Use Not-At-Fault Accidents Count. 
Determine AL value in Matrix AL using Novo SPD Count and Novo MAJ Count.
Determine AM value in Matrix AM using Matrix AK Value and Matrix AL Value.
Look up the factor in the Step 1c Factor Table using Matrix AD Value and Matrix AM Value."							
"Determine AN value in Matrix AN using Non-Novo NAF Count and Non-Novo CMU Count. 
Determine AO value in Matrix AO using Non-Novo CMP Count and Novo NAF Count.
Determine AP value in Matrix AP using Matrix AN Value and Matrix AO Value.
Look up the factor in the Step 1d Factor Table using Matrix AD Value and Matrix AP Value."							
"Determine AQ value in Matrix AQ using Novo Theft or Vandalism CMP Claims Count and Prior Insurance Classification. 
Determine AR value in Matrix AR using Novo CMU Count and Novo CMP Count.
Determine AS value in Matrix AS using Matrix AQ Value and Matrix AR Value.
Look up the factor in the Step 1e Factor Table using Matrix AD Value and Matrix AS Value."							
Calculate the Step 1 Factor by taking the product of the Step 1a through Step 1e factors. Round to 2 decimals.							
							
Determine the Step 2 Factor:							
"Determine BA value in Matrix BA using Prior Insurance Classification and Rewrite Reason.
Determine BB value in Matrix BB using Risk Group and Number of Eligible-to-be-Rated Drivers.
Determine BC value in Matrix BC using Matrix BA Value and Matrix BB Value.
Determine BD value in Matrix BD using Matrix BC Value and Number of Vehicles.
Determine BE value in Matrix BE using Tenure with the Company and Number of Vehicle Endorsements.
Determine BF value in Matrix BF using Non-Payment Cancels Count and Non-Payment Reinstates Count.
Determine BG value in Matrix BG using Matrix BE Value and Matrix BF Value.
Look up the factor in the Step 2a Factor Table using Matrix BD Value and Matrix BG Value.

Determine BH value in Matrix BH using Three-Year Safe Driving Discount and Company Tenure Prior to Current Policy. 
Determine BI value in Matrix BI using New Business Five-Year Accident Free Discount and Prior Insurance BI Limit.
Determine BJ value in Matrix BJ using Matrix BH Value and Matrix BI Value.
Look up the factor in the Step 2b Factor Table using Matrix BD Value and Matrix BJ Value."							
"Determine BK value in Matrix BK using Silver Continuous Insurance Discount at Current Policy and Excess Resident Classification.
Determine BL value in Matrix BL using Number of Recent Non-Novo Claims and Omitted Incident Count.
Determine BM value in Matrix BM using Matrix BK Value and Matrix BL Value.
Look up the factor in the Step 2c Factor Table using Matrix BD Value and Matrix BM Value.

Determine BN value in Matrix BN using Prior Insurance Activity Tier and Prior Insurance BI Limit.
Look up the factor in the Step 2d Factor Table using Matrix BD Value and Matrix BN Value."							
Calculate the Step 2 Factor by taking the product of the Step 2a through Step 2d factors. Round to 2 decimals.							
							
							
"Calculate the Final Value:
Multiply the Step 1 Factor, the Step 2 Factor, and the Step 3 Factor together. Multiply the result by 9,234, the base value. Round to 0 decimal places."							
"Multiply the Step 1 Factor and the Step 2 Factor together.
Multiply the result by 10,000, the base value. Round to 0 decimal places."
''' 						

check_the_risk_attribute_subject = '''

before inference, check the risk attribute subject, if the risk attribute subject (driver ,vehicle ,policy).
If the risk attribut subject is driver/vehicle level, we should check the risk attribute value on each entity.

'''