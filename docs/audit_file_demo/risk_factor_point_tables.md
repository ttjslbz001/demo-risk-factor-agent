# Risk Factors Reference Table

| # | Risk Factor/Point Name | Risk Category | Coverages |
|---|------------------------|---------------|-----------|
| **DRIVER FACTORS** |
| 1 | Driver_Age_Risk_Factor_BI_PD | Driver Age, BI/PD Points | BI, PD |
| 2 | Driver_Age_Risk_Factor_Coll | Driver Age, COLL Points | COLL, RENT |
| 3 | Driver_Age_Risk_Factor_Comp | Driver Age, COMP Points | COMP, LOAN |
| 4 | Driver_Age_Risk_Factor_Med | Driver Age, MED Points | MED, UM, UIM |
| 5 | Driver_Class_Risk_Factor | Gender, Marital Status, Driver Age, Months Since Last Birthday, Ratable Spouse | BI, PD, COMP, COLL, LOAN, MED, UM, UIM, RENT |
| 6 | Driver_License_Type_Risk_Factor | License Type Code, Driver Age | BI, PD, COMP, COLL, MED, UM, UIM |
| 7 | Driver_Training_Disc_Risk_Factor | Driver Age, Driver Training Discount | BI, PD, COMP, COLL, LOAN, MED, UM, UIM, RENT |
| 8 | Years_Licensed_Risk_Factor | Driver Age, Years Licensed | BI, PD, COMP, COLL, LOAN, MED, UM, UIM, RENT |
| 9 | Youthful_Driver_Disc_Risk_Factor | Driver Age, Clean Driver, Distant Student Discount, Good Student Discount, Teen Driver Discount, Driver Add Date Classification | BI, PD, COMP, COLL, LOAN, MED, UM, UIM, RENT |
| 10 | Financial_Resp_By_Clean_Risk_Factor | Financial Responsibility Tier, Clean Driver | BI, PD, COMP, COLL, LOAN, MED, UM, UIM, RENT |
| 11 | Financial_Resp_By_Num_Of_Drivers_Risk_Factor | Financial Responsibility Tier, Multiple Eligible to be Rated Drivers | BI, PD, COMP, COLL, LOAN, MED, UM, UIM |
| 12 | Occupation_Education_Risk_Factor | Prior Insurance Classification, Occupation Education Rank | BI, PD, COMP, COLL, LOAN, MED, UM, UIM |
| 13 | HH_Member_Risk_Factor (Table 1) | Vehicle Count, Household Member Count, Driver Age | BI, PD, COMP, COLL, LOAN, MED, UM, UIM, RENT |
| 14 | HH_Member_Risk_Factor (Table 2) | Vehicle Count, Household Member Count, Driver Age | BI, PD, COMP, COLL, LOAN, MED, UM, UIM, RENT |
| 15 | Driving_Record_Points_Risk_Point_BI_PD | BI/PD Points | BI, PD |
| 16 | Driving_Record_Points_Risk_Point_Coll | COLL Points | COLL, RENT |
| 17 | Driving_Record_Points_Risk_Point_Comp | COMP Points | COMP, LOAN |
| 18 | Driving_Record_Points_Risk_Point_Med | MED Points | MED, UM, UIM |
| 19 | Subtraction_Of_Unity_Risk_Point | x (placeholder) | BI, PD, COMP, COLL, LOAN, MED, UM, UIM, RENT, TOW |
| **VEHICLE FACTORS** |
| 20 | Vehicle_Age_Risk_Factor | Vehicle Risk Group Code at Initial Vehicle Evaluation, Vehicle Age at Add Date | BI, PD, COMP, COLL, LOAN, MED, UM, UIM, RENT |
| 21 | Vehicle_Age_Coverage_Risk_Factor | Vehicle Tenure, Vehicle Age at Add Date, Multi-Car, Full Coverage on Vehicle | BI, PD, COMP, COLL, LOAN, MED, UM, UIM, RENT |
| 22 | Veh_Symbol_Risk_Factor | Model Year, Make, Model, Style | BI, PD, COMP, COLL, LOAN, MED, UM, UIM |
| 23 | Aux_Symbol_Risk_Factor | Auxiliary Symbol | BI, PD, COMP, COLL, LOAN, MED, UM, UIM |
| 24 | Vehicle_Attributes_Rating_Risk_Factor | Multi-Car, Vehicle Type Code, Convertible Indicator, Vehicle Horsepower Code | BI, PD, COMP, COLL, LOAN, MED, UM, UIM |
| 25 | Vehicle_History_Rating_Risk_Factor | Title Issue Indicator, Junk Title Indicator, Theft Indicator, No Data Available on Valid VIN Indicator, Invalid VIN Indicator | BI, PD, COMP, COLL, LOAN, MED, UM, UIM, RENT |
| 26 | Luxury_Veh_Risk_Factor | PNI Age, Luxury Vehicle on Policy, Vehicle Count | BI, PD, COMP, COLL, LOAN, MED, UM, UIM |
| 27 | Annual_Miles_Risk_Factor | Annual Miles | BI, PD, COMP, COLL, MED, UM, UIM |
| 28 | Garaging_Location_Risk_Factor | Garaging ZIP Code | BI, PD, COMP, COLL, LOAN, MED, UM, UIM, RENT, ACPE |
| 29 | Length_Of_Veh_Ownership_Risk_Factor | Vehicle Tenure, Vehicle Age at Add Date, Length of Vehicle Ownership | BI, PD, COMP, COLL, LOAN, MED, UM, UIM, RENT |
| 30 | Excess_Veh_Risk_Factor | Excess Vehicle | BI, PD, COMP, COLL, LOAN, MED, UM, UIM |
| 31 | Business_Use_Surcharge_Risk_Factor | Business Use | BI, PD, COMP, COLL, LOAN, MED, UM, UIM, RENT, ACPE |
| 32 | Financial_Resp_Filing_Surcharge_Risk_Factor | Financial Responsibility Filing Surcharge | BI, PD, COMP, COLL, MED, UM, UIM |
| **HOUSEHOLD/POLICY FACTORS** |
| 33 | HH_Structure_Risk_Factor | Multi-Car, PNI Marital Status, PNI Youthful, Youthful Drivers, rated drivers, Eligible to be Rated Drivers, Rated Youthful Drivers, Rated Driver Gender | BI, PD, COMP, COLL, LOAN, MED, UM, UIM |
| 34 | Full_Cov_Risk_Factor | Prior BI Level, Full Coverage On Policy, Multi-Car | BI, PD, MED, UM, UIM |
| 35 | Late_Renewal_Risk_Factor | Prior BI Level, Number of Lapse Days 1..10, Number of Lapse Days 11..30, Number of Lapse Days 31..99999 | BI, PD, COMP, COLL, LOAN, MED, UM, UIM, RENT, ACPE |
| 36 | Advance_Quote_Risk_Factor | Prior Insurance Classification, Advance Shop Days, Advance Quote Discount | BI, PD, COMP, COLL, LOAN, MED, UM, UIM, RENT, ACPE |
| 37 | Risk_Group_Code_Risk_Factor | Risk Group Code | BI, PD, COMP, COLL, LOAN, MED, UM, UIM, RENT, ACPE |
| **DISCOUNT FACTORS** |
| 38 | Cont_Ins_Disc_Diamond | Prior Insurance Classification, Prior BI Limit Classification, Silver Continuous Insurance Discount at Current Policy Inception, Gold Continuous Insurance Discount at Current Policy Inception | BI, PD, COMP, COLL, LOAN, MED, UM, UIM, RENT |
| 39 | Cont_Ins_Disc_DiamondSelect | Prior Insurance Classification, Prior BI Limit Classification | BI, PD, COMP, COLL, LOAN, MED, UM, UIM, RENT |
| 40 | Cont_Ins_Disc_Platinum1Select | Prior Insurance Classification, Prior BI Limit Classification | BI, PD, COMP, COLL, LOAN, MED, UM, UIM, RENT |
| 41 | Cont_Ins_Disc_Platinum2Select | Prior Insurance Classification, Prior BI Limit Classification | BI, PD, COMP, COLL, LOAN, MED, UM, UIM, RENT |
| 42 | Cont_Ins_Disc_GoldSelect | Prior Insurance Classification, Prior BI Limit Classification | BI, PD, COMP, COLL, LOAN, MED, UM, UIM, RENT |
| 43 | Cont_Ins_Disc_SilverSelect | Prior Insurance Classification, Prior BI Limit Classification | BI, PD, COMP, COLL, LOAN, MED, UM, UIM, RENT |
| 44 | Cont_Ins_Disc_Platinum1 | Prior Insurance Classification, Prior BI Limit Classification, Silver Continuous Insurance Discount at Current Policy Inception, Gold Continuous Insurance Discount at Current Policy Inception | BI, PD, COMP, COLL, LOAN, MED, UM, UIM, RENT |
| 45 | Cont_Ins_Disc_Gold | Prior Insurance Classification, Prior BI Limit Classification | BI, PD, COMP, COLL, LOAN, MED, UM, UIM, RENT |
| 46 | Cont_Ins_Disc_Silver | Prior Insurance Classification, Prior BI Limit Classification | BI, PD, COMP, COLL, LOAN, MED, UM, UIM, RENT |
| 47 | Cont_Ins_Disc_NoDisc | Prior Insurance Classification, Prior BI Limit Classification | BI, PD, COMP, COLL, LOAN, MED, UM, UIM, RENT |
| 48 | Three_Year_Safe_Dr_Disc_Risk_Factor | Three Year Safe Driving Discount Eligibility, Prior BI Level, Multi-Car | BI, PD, COMP, COLL, LOAN, MED, UM, UIM, RENT, ACPE |
| 49 | NB_Five_Yr_Acc_Free_Claim_Free_Disc_Risk_Factor | New Business Five Year Accident Free Discount Eligibility, Five Year Claim Free Eligibility, Prior BI Level, Multi-Car, Current Policy Tenure | BI, PD, COMP, COLL, LOAN, MED, UM, UIM, RENT, ACPE |
| 50 | Home_MH_MC_Disc_Risk_Factor | Prior BI Level, Multi-Car, Homeowner, Mobile Home Owner | BI, PD, COMP, COLL, MED, UM, UIM, RENT |
| 51 | NB_NSP_Disc_Risk_Factor | NSP Participation Discount | BI, PD, COMP, COLL, LOAN, MED, UM, UIM, RENT, ACPE, ACQ-EXP, OPS-EXP |
| **TIER & RATE FACTORS** |
| 52 | UW_Tier_Percent_Risk_Factor | UW Tier | BI, PD, COMP, COLL, LOAN, MED, UM, UIM, RENT |
| 53 | FR_Tier_Risk_Factor | Financial Responsibility Tier, Prior Insurance Classification | BI, PD, COMP, COLL, LOAN, MED, UM, UIM, RENT |
| 54 | Base_Rates_Risk_Rate | x (placeholder) | BI, PD, COMP, COLL, LOAN, MED, UM, UIM, RENT, ACPE, ACQ-EXP, OPS-EXP |
| 55 | Monthly_Rate_Risk_Factor | Trend Months | BI, PD, COMP, COLL, LOAN, MED, UM, UIM, RENT, ACPE |
| 56 | Policy_Term_Risk_Factor | Policy Term | BI, PD, COMP, COLL, LOAN, MED, UM, UIM, RENT, ACPE, ACQ-EXP, OPS-EXP |
| **COVERAGE & LIMIT FACTORS** |
| 57 | Coverage_Selection_COLL_Risk_Factor | COLL Deductible at Initial Evaluation, COLL Deductible | BI, PD, COMP, COLL, LOAN, MED, UM, UIM, RENT, ACPE |
| 58 | Coverage_Selection_COMP_Risk_Factor | COMP Deductible at Initial Evaluation, Glass Coverage at Initial Evaluation, COMP Deductible, Glass Coverage | BI, PD, COMP, COLL, LOAN, MED, UM, UIM, RENT, ACPE |
| 59 | Limit_And_Ded_Risk_Factor_BI | Prior Insurance Indicator, BI Limit | BI |
| 60 | Limit_And_Ded_Risk_Factor_PD | PD Limit | PD |
| 61 | Limit_And_Ded_Risk_Factor_COMP | COMP Deductible, Glass Coverage | COMP |
| 62 | Limit_And_Ded_Risk_Factor_Coll | COLL Deductible | COLL |
| 63 | Limit_And_Ded_Risk_Factor_Med | Med Limit | MED |
| 64 | Limit_And_Ded_Risk_Factor_UM | UM Limit | UM |
| 65 | Limit_And_Ded_Risk_Factor_UIM | UIM Limit | UIM |
| 66 | Limit_And_Ded_Risk_Factor_Loan | LOAN Limit | LOAN |
| 67 | Limit_And_Ded_Risk_Factor_Rent | RENT Limit | RENT |
| 68 | Limit_And_Ded_Risk_Factor_ACPE | ACPE Limit | ACPE |
| **OPERATIONAL EXPENSE FACTORS** |
| 69 | OpEx1_Risk_Factor | Prior Insurance Classification, Financial Responsibility Tier | OPS-EXP |
| 70 | OpEx2_Risk_Factor | Eligible to be Rated Drivers, Vehicle Count | OPS-EXP |
| 71 | OpEx3_Risk_Factor | PNI Age | OPS-EXP |
| 72 | OpEx5_Risk_Factor | Vehicle Count, Number of Vehicle Addition Endorsements | OPS-EXP |
| 73 | OpEx6_Risk_Factor | Number of Non-Pay Cancels, Number of Non-Pay Reinstates | OPS-EXP |
| 74 | OpEx8_Risk_Factor | Prior Insurance Activity Tier | OPS-EXP |
| 75 | Acq_Exp_Factor_AE1_Risk_Factor | Vehicle Count at Initial Evaluation, Full Coverage Status at Initial Evaluation, Prior Insurance Classification | ACQ-EXP |
| 76 | Acq_Exp_Factor_AE2_Risk_Factor | Prior Insurance Activity Tier | ACQ-EXP |
| 77 | Bad_Debt_Fr_Risk_Factor | Prior Insurance Classification, Financial Responsibility Tier | BI, PD, COMP, COLL, LOAN, MED, UM, UIM, RENT, ACPE, ACQ-EXP, OPS-EXP |
| **UBI/TELEMATICS FACTORS** |
| 78 | NSP_Default_Safety_Score_Risk_Factor (Currently Monitoring: Yes) | Default Safety Score, Months Since Monitoring | BI, PD, COMP, COLL, LOAN, MED, UM, UIM, RENT, ACPE, ACQ-EXP, OPS-EXP |
| 79 | NSP_Default_Safety_Score_Risk_Factor (Currently Monitoring: No) | Default Safety Score, Months Since Monitoring | BI, PD, COMP, COLL, LOAN, MED, UM, UIM, RENT, ACPE, ACQ-EXP, OPS-EXP |

---

**Coverage Codes:** BI (Bodily Injury), PD (Property Damage), COMP (Comprehensive), COLL (Collision), LOAN (Loan/Lease), MED (Medical Payments), UM (Uninsured Motorist), UIM (Underinsured Motorist), RENT (Rental), ACPE (Additional Custom Personal Equipment), ACQ-EXP (Acquisition Expense), OPS-EXP (Operations Expense), TOW (Towing)

**Total Tables:** 79 extracted from 92+ factor/point tables  
**Source:** AZ_2025-07-15_v250.xlsm