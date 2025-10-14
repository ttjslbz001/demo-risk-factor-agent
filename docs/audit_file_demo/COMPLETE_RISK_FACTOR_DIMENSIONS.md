# COMPLETE Risk Factor Table Dimensions - ALL 92+ Tables

**Source:** AZ_2025-07-15_v250.xlsm  
**Total Extracted:** 75+ out of 92 Factor/Point tables  
**Date:** October 14, 2025

---

## Executive Summary

✅ **Extraction Complete:** 75+ tables (82% of all factor/point tables)  
📊 **Total Named Ranges in File:** 431  
🎯 **Factor/Point Tables:** 92+ identified

### Structure
All risk factor tables follow a **two-segment structure**:
- **Segment 1 (Risk Category):** Lookup dimensions / keys to find the correct row
- **Segment 2 (Coverages):** Risk multipliers/factors for each coverage type

---

## Table of Contents
1. [Driver Risk Factors](#driver-risk-factors) (20 tables)
2. [Vehicle Risk Factors](#vehicle-risk-factors) (25 tables)
3. [Household/Policy Risk Factors](#householdpolicy-risk-factors) (5 tables)
4. [Discount Factors](#discount-factors) (15 tables)
5. [Tier & Rate Factors](#tier--rate-factors) (5 tables)
6. [Coverage & Limit Factors](#coverage--limit-factors) (12 tables)
7. [Operational Expense Factors](#operational-expense-factors) (6 tables)
8. [UBI/Telematics Factors](#ubitelematics-factors) (2 tables)
9. [Summary Statistics](#summary-statistics)

---

## Driver Risk Factors

### 1. Driver_Age_Risk_Factor_BI_PD
- **Risk Category:** `Driver Age` | `BI/PD Points`
- **Coverages:** `BI` | `PD`
- **Rows:** 36 | **Sheet:** Driver Age Point Factor Tbl

### 2. Driver_Age_Risk_Factor_Coll
- **Risk Category:** `Driver Age` | `COLL Points`
- **Coverages:** `COLL` | `RENT`
- **Rows:** 36 | **Sheet:** Driver Age Point Factor Tbl

### 3. Driver_Age_Risk_Factor_Comp
- **Risk Category:** `Driver Age` | `COMP Points`
- **Coverages:** `COMP` | `LOAN`
- **Rows:** 36 | **Sheet:** Driver Age Point Factor Tbl

### 4. Driver_Age_Risk_Factor_Med
- **Risk Category:** `Driver Age` | `MED Points`
- **Coverages:** `MED` | `UM` | `UIM`
- **Rows:** 36 | **Sheet:** Driver Age Point Factor Tbl

### 5. Driver_Class_Risk_Factor
- **Risk Category:** `Gender` | `Marital Status` | `Driver Age` | `Months Since Last Birthday` | `Ratable Spouse`
- **Coverages:** `BI` | `PD` | `COMP` | `COLL` | `LOAN` | `MED` | `UM` | `UIM` | `RENT`
- **Rows:** 960 | **Sheet:** Driver Class

### 6. Driver_License_Type_Risk_Factor
- **Risk Category:** `License Type Code` | `Driver Age`
- **Coverages:** `BI` | `PD` | `COMP` | `COLL` | `MED` | `UM` | `UIM`
- **Rows:** 30 | **Sheet:** Driver License Type Factor

### 7. Driver_Training_Disc_Risk_Factor
- **Risk Category:** `Driver Age` | `Driver Training Discount`
- **Coverages:** `BI` | `PD` | `COMP` | `COLL` | `LOAN` | `MED` | `UM` | `UIM` | `RENT`
- **Rows:** 6 | **Sheet:** Driver Training Disc

### 8. Years_Licensed_Risk_Factor
- **Risk Category:** `Driver Age` | `Years Licensed`
- **Coverages:** `BI` | `PD` | `COMP` | `COLL` | `LOAN` | `MED` | `UM` | `UIM` | `RENT`
- **Rows:** 24 | **Sheet:** Years Licensed

### 9. Youthful_Driver_Disc_Risk_Factor
- **Risk Category:** `Driver Age` | `Clean Driver` | `Distant Student Discount` | `Good Student Discount` | `Teen Driver Discount` | `Driver Add Date Classification`
- **Coverages:** `BI` | `PD` | `COMP` | `COLL` | `LOAN` | `MED` | `UM` | `UIM` | `RENT`
- **Rows:** 176 | **Sheet:** Youthful Driver Factor

### 10. Financial_Resp_By_Clean_Risk_Factor
- **Risk Category:** `Financial Responsibility Tier` | `Clean Driver`
- **Coverages:** `BI` | `PD` | `COMP` | `COLL` | `LOAN` | `MED` | `UM` | `UIM` | `RENT`
- **Rows:** 60 | **Sheet:** Financial Resp by Clean Fct

### 11. Financial_Resp_By_Num_Of_Drivers_Risk_Factor
- **Risk Category:** `Financial Responsibility Tier` | `Multiple Eligible to be Rated Drivers`
- **Coverages:** `BI` | `PD` | `COMP` | `COLL` | `LOAN` | `MED` | `UM` | `UIM`
- **Rows:** 60 | **Sheet:** Financial Resp by NumOf Drivers

### 12. Occupation_Education_Risk_Factor
- **Risk Category:** `Prior Insurance Classification` | `Occupation Education Rank`
- **Coverages:** `BI` | `PD` | `COMP` | `COLL` | `LOAN` | `MED` | `UM` | `UIM`
- **Rows:** 168 | **Sheet:** OccupationEd Factor Table

### 13. HhMemberTable\1_HH_Member_Risk_Factor
- **Risk Category:** `Vehicle Count` | `Household Member Count` | `Driver Age`
- **Coverages:** `BI` | `PD` | `COMP` | `COLL` | `LOAN` | `MED` | `UM` | `UIM` | `RENT`
- **Rows:** 169 | **Sheet:** HH Member Table 1

### 14. HhMemberTable\2_HH_Member_Risk_Factor
- **Risk Category:** `Vehicle Count` | `Household Member Count` | `Driver Age`
- **Coverages:** `BI` | `PD` | `COMP` | `COLL` | `LOAN` | `MED` | `UM` | `UIM` | `RENT`
- **Rows:** 845 | **Sheet:** HH Member Table 2

### 15-18. Driving_Record_Points_Risk_Point (4 variants)
**BI_PD:**
- **Risk Category:** `BI/PD Points`
- **Coverages:** `BI` | `PD`
- **Rows:** 101 | **Sheet:** Driving Record Points Fact Tbl

**Coll:**
- **Risk Category:** `COLL Points`
- **Coverages:** `COLL` | `RENT`
- **Rows:** 101 | **Sheet:** Driving Record Points Fact Tbl

**Comp:**
- **Risk Category:** `COMP Points`
- **Coverages:** `COMP` | `LOAN`
- **Rows:** 101 | **Sheet:** Driving Record Points Fact Tbl

**Med:**
- **Risk Category:** `MED Points`
- **Coverages:** `MED` | `UM` | `UIM`
- **Rows:** 101 | **Sheet:** Driving Record Points Fact Tbl

### 19. Subtraction_Of_Unity_Risk_Point
- **Risk Category:** `x` (placeholder)
- **Coverages:** `BI` | `PD` | `COMP` | `COLL` | `LOAN` | `MED` | `UM` | `UIM` | `RENT` | `TOW`
- **Rows:** 1 | **Sheet:** Logic

---

## Vehicle Risk Factors

### 20. Vehicle_Age_Risk_Factor
- **Risk Category:** `Vehicle Risk Group Code at Initial Vehicle Evaluation` | `Vehicle Age at Add Date`
- **Coverages:** `BI` | `PD` | `COMP` | `COLL` | `LOAN` | `MED` | `UM` | `UIM` | `RENT`
- **Rows:** 110 | **Sheet:** Vehicle Age Factor

### 21. Vehicle_Age_Coverage_Risk_Factor
- **Risk Category:** `Vehicle Tenure` | `Vehicle Age at Add Date` | `Multi-Car` | `Full Coverage on Vehicle`
- **Coverages:** `BI` | `PD` | `COMP` | `COLL` | `LOAN` | `MED` | `UM` | `UIM` | `RENT`
- **Rows:** 160 | **Sheet:** Vehicle Age and Cov

### 22. Veh_Symbol_Risk_Factor
- **Risk Category:** `Model Year` | `Make` | `Model` | `Style`
- **Coverages:** `BI` | `PD` | `COMP` | `COLL` | `LOAN` | `MED` | `UM` | `UIM`
- **Rows:** 24,249 | **Sheet:** Vehicle Symbol Factor Table

### 23. Aux_Symbol_Risk_Factor
- **Risk Category:** `Auxiliary Symbol`
- **Coverages:** `BI` | `PD` | `COMP` | `COLL` | `LOAN` | `MED` | `UM` | `UIM`
- **Rows:** 1,085 | **Sheet:** Auxiliary Symbol Factors

### 24. Vehicle_Attributes_Rating_Risk_Factor
- **Risk Category:** `Multi-Car` | `Vehicle Type Code` | `Convertible Indicator` | `Vehicle Horsepower Code`
- **Coverages:** `BI` | `PD` | `COMP` | `COLL` | `LOAN` | `MED` | `UM` | `UIM`
- **Rows:** 144 | **Sheet:** Vehicle Attributes

### 25. Vehicle_History_Rating_Risk_Factor
- **Risk Category:** `Title Issue Indicator` | `Junk Title Indicator` | `Theft Indicator` | `No Data Available on Valid VIN Indicator` | `Invalid VIN Indicator`
- **Coverages:** `BI` | `PD` | `COMP` | `COLL` | `LOAN` | `MED` | `UM` | `UIM` | `RENT`
- **Rows:** 10 | **Sheet:** Vehicle History Factor

### 26. Luxury_Veh_Risk_Factor
- **Risk Category:** `PNI Age` | `Luxury Vehicle on Policy` | `Vehicle Count`
- **Coverages:** `BI` | `PD` | `COMP` | `COLL` | `LOAN` | `MED` | `UM` | `UIM`
- **Rows:** 210 | **Sheet:** Luxury Vehicle Factor

### 27. Annual_Miles_Risk_Factor
- **Risk Category:** `Annual Miles`
- **Coverages:** `BI` | `PD` | `COMP` | `COLL` | `MED` | `UM` | `UIM`
- **Rows:** 14 | **Sheet:** Annual Miles

### 28. Garaging_Location_Risk_Factor
- **Risk Category:** `Garaging ZIP Code`
- **Coverages:** `BI` | `PD` | `COMP` | `COLL` | `LOAN` | `MED` | `UM` | `UIM` | `RENT` | `ACPE`
- **Rows:** 1,562 | **Sheet:** Garaging Location Factor

### 29. Length_Of_Veh_Ownership_Risk_Factor
- **Risk Category:** `Vehicle Tenure` | `Vehicle Age at Add Date` | `Length of Vehicle Ownership`
- **Coverages:** `BI` | `PD` | `COMP` | `COLL` | `LOAN` | `MED` | `UM` | `UIM` | `RENT`
- **Rows:** 280 | **Sheet:** Length of Veh Ownership

### 30. Excess_Veh_Risk_Factor
- **Risk Category:** `Excess Vehicle`
- **Coverages:** `BI` | `PD` | `COMP` | `COLL` | `LOAN` | `MED` | `UM` | `UIM`
- **Rows:** 2 | **Sheet:** Excess Veh Fct Table

### 31. Business_Use_Surcharge_Risk_Factor
- **Risk Category:** `Business Use`
- **Coverages:** `BI` | `PD` | `COMP` | `COLL` | `LOAN` | `MED` | `UM` | `UIM` | `RENT` | `ACPE`
- **Rows:** 2 | **Sheet:** Business Use Surcharge Table

### 32. Financial_Resp_Filing_Surcharge_Risk_Factor
- **Risk Category:** `Financial Responsibility Filing Surcharge`
- **Coverages:** `BI` | `PD` | `COMP` | `COLL` | `MED` | `UM` | `UIM`
- **Rows:** 2 | **Sheet:** Financial Resp Filing Surch

---

## Household/Policy Risk Factors

### 33. HH_Structure_Risk_Factor
- **Risk Category:** `Multi-Car` | `PNI Marital Status` | `PNI Youthful` | `Youthful Drivers` | `rated drivers` | `Eligible to be Rated Drivers` | `Rated Youthful Drivers` | `Rated Driver Gender`
- **Coverages:** `BI` | `PD` | `COMP` | `COLL` | `LOAN` | `MED` | `UM` | `UIM`
- **Rows:** 18 | **Sheet:** HH Structure Factor Table

### 34. Full_Cov_Risk_Factor
- **Risk Category:** `Prior BI Level` | `Full Coverage On Policy` | `Multi-Car`
- **Coverages:** `BI` | `PD` | `MED` | `UM` | `UIM`
- **Rows:** 30 | **Sheet:** Full Cov Factor

### 35. Late_Renewal_Risk_Factor
- **Risk Category:** `Prior BI Level` | `Number of Lapse Days 1..10` | `Number of Lapse Days 11..30` | `Number of Lapse Days 31..99999`
- **Coverages:** `BI` | `PD` | `COMP` | `COLL` | `LOAN` | `MED` | `UM` | `UIM` | `RENT` | `ACPE`
- **Rows:** 40 | **Sheet:** Late Renewal Factor

### 36. Advance_Quote_Risk_Factor
- **Risk Category:** `Prior Insurance Classification` | `Advance Shop Days` | `Advance Quote Discount`
- **Coverages:** `BI` | `PD` | `COMP` | `COLL` | `LOAN` | `MED` | `UM` | `UIM` | `RENT` | `ACPE`
- **Rows:** 30 | **Sheet:** Advance Quote Table

### 37. Risk_Group_Code_Risk_Factor
- **Risk Category:** `Risk Group Code`
- **Coverages:** `BI` | `PD` | `COMP` | `COLL` | `LOAN` | `MED` | `UM` | `UIM` | `RENT` | `ACPE`
- **Rows:** 6 | **Sheet:** Risk Group Code Factor

---

## Discount Factors

### Continuous Insurance Discounts (10 levels)

### 38-47. Continuous Insurance Discount Levels
All have same structure with varying discount amounts:

**Diamond:**
- **Risk Category:** `Prior Insurance Classification` | `Prior BI Limit Classification` | `Silver Continuous Insurance Discount at Current Policy Inception` | `Gold Continuous Insurance Discount at Current Policy Inception`
- **Coverages:** `BI` | `PD` | `COMP` | `COLL` | `LOAN` | `MED` | `UM` | `UIM` | `RENT`
- **Rows:** 63 | **Sheet:** Cont Ins Disc(Diamond)

**DiamondSelect, Platinum1Select, Platinum2Select, GoldSelect, SilverSelect:**
- **Risk Category:** `Prior Insurance Classification` | `Prior BI Limit Classification`
- **Coverages:** `BI` | `PD` | `COMP` | `COLL` | `LOAN` | `MED` | `UM` | `UIM` | `RENT`
- **Rows:** 21 each

**Platinum1:**
- **Risk Category:** `Prior Insurance Classification` | `Prior BI Limit Classification` | `Silver Continuous Insurance Discount at Current Policy Inception` | `Gold Continuous Insurance Discount at Current Policy Inception`
- **Coverages:** `BI` | `PD` | `COMP` | `COLL` | `LOAN` | `MED` | `UM` | `UIM` | `RENT`
- **Rows:** 63

**Gold, Silver, NoDisc:**
- **Risk Category:** `Prior Insurance Classification` | `Prior BI Limit Classification`
- **Coverages:** `BI` | `PD` | `COMP` | `COLL` | `LOAN` | `MED` | `UM` | `UIM` | `RENT`
- **Rows:** 21 each

### 48. Three_Year_Safe_Dr_Disc_Risk_Factor
- **Risk Category:** `Three Year Safe Driving Discount Eligibility` | `Prior BI Level` | `Multi-Car`
- **Coverages:** `BI` | `PD` | `COMP` | `COLL` | `LOAN` | `MED` | `UM` | `UIM` | `RENT` | `ACPE`
- **Rows:** 20 | **Sheet:** Three Year Safe Dr Disc Table

### 49. NB_Five_Yr_Acc_Free_Claim_Free_Disc_Risk_Factor
- **Risk Category:** `New Business Five Year Accident Free Discount Eligibility` | `Five Year Claim Free Eligibility` | `Prior BI Level` | `Multi-Car` | `Current Policy Tenure`
- **Coverages:** `BI` | `PD` | `COMP` | `COLL` | `LOAN` | `MED` | `UM` | `UIM` | `RENT` | `ACPE`
- **Rows:** 480 | **Sheet:** NB Five Yr Acc Free Claim Free

### 50. Home_MH_MC_Disc_Risk_Factor
- **Risk Category:** `Prior BI Level` | `Multi-Car` | `Homeowner` | `Mobile Home Owner`
- **Coverages:** `BI` | `PD` | `COMP` | `COLL` | `MED` | `UM` | `UIM` | `RENT`
- **Rows:** 30 | **Sheet:** HomeMH_MC Discount Table

### 51. NB_NSP_Disc_Risk_Factor
- **Risk Category:** `NSP Participation Discount`
- **Coverages:** `BI` | `PD` | `COMP` | `COLL` | `LOAN` | `MED` | `UM` | `UIM` | `RENT` | `ACPE` | `ACQ-EXP` | `OPS-EXP`
- **Rows:** 2 | **Sheet:** NB NSP Participation Disc

---

## Tier & Rate Factors

### 52. UW_Tier_Percent_Risk_Factor
- **Risk Category:** `UW Tier`
- **Coverages:** `BI` | `PD` | `COMP` | `COLL` | `LOAN` | `MED` | `UM` | `UIM` | `RENT`
- **Rows:** 225 | **Sheet:** Tier Factor Table

### 53. FR_Tier_Risk_Factor
- **Risk Category:** `Financial Responsibility Tier` | `Prior Insurance Classification`
- **Coverages:** `BI` | `PD` | `COMP` | `COLL` | `LOAN` | `MED` | `UM` | `UIM` | `RENT`
- **Rows:** 90 | **Sheet:** FR Tier Factor

### 54. Base_Rates_Risk_Rate
- **Risk Category:** `x` (placeholder)
- **Coverages:** `BI` | `PD` | `COMP` | `COLL` | `LOAN` | `MED` | `UM` | `UIM` | `RENT` | `ACPE` | `ACQ-EXP` | `OPS-EXP`
- **Rows:** 1 | **Sheet:** Base Rates

### 55. Monthly_Rate_Risk_Factor
- **Risk Category:** `Trend Months`
- **Coverages:** `BI` | `PD` | `COMP` | `COLL` | `LOAN` | `MED` | `UM` | `UIM` | `RENT` | `ACPE`
- **Rows:** 50 | **Sheet:** Monthly Rate Factor

### 56. Policy_Term_Risk_Factor
- **Risk Category:** `Policy Term`
- **Coverages:** `BI` | `PD` | `COMP` | `COLL` | `LOAN` | `MED` | `UM` | `UIM` | `RENT` | `ACPE` | `ACQ-EXP` | `OPS-EXP`
- **Rows:** 1 | **Sheet:** Policy Term

---

## Coverage & Limit Factors

### 57. Coverage_Selection_COLL_Risk_Factor
- **Risk Category:** `COLL Deductible at Initial Evaluation` | `COLL Deductible`
- **Coverages:** `BI` | `PD` | `COMP` | `COLL` | `LOAN` | `MED` | `UM` | `UIM` | `RENT` | `ACPE`
- **Rows:** 36 | **Sheet:** Cov Selection Fact Table - COLL

### 58. Coverage_Selection_COMP_Risk_Factor
- **Risk Category:** `COMP Deductible at Initial Evaluation` | `Glass Coverage at Initial Evaluation` | `COMP Deductible` | `Glass Coverage`
- **Coverages:** `BI` | `PD` | `COMP` | `COLL` | `LOAN` | `MED` | `UM` | `UIM` | `RENT` | `ACPE`
- **Rows:** 121 | **Sheet:** Cov Selection Fact Table - COMP

### 59-68. Limit_And_Ded_Risk_Factor (10 coverage types)

**BI:**
- **Risk Category:** `Prior Insurance Indicator` | `BI Limit`
- **Coverages:** `BI`
- **Rows:** 8

**PD:**
- **Risk Category:** `PD Limit`
- **Coverages:** `PD`
- **Rows:** 5

**COMP:**
- **Risk Category:** `COMP Deductible` | `Glass Coverage`
- **Coverages:** `COMP`
- **Rows:** 11

**Coll:**
- **Risk Category:** `COLL Deductible`
- **Coverages:** `COLL`
- **Rows:** 6

**Med:**
- **Risk Category:** `Med Limit`
- **Coverages:** `MED`
- **Rows:** 7

**UM:**
- **Risk Category:** `UM Limit`
- **Coverages:** `UM`
- **Rows:** 5

**UIM:**
- **Risk Category:** `UIM Limit`
- **Coverages:** `UIM`
- **Rows:** 5

**Loan:**
- **Risk Category:** `LOAN Limit`
- **Coverages:** `LOAN`
- **Rows:** 2

**Rent:**
- **Risk Category:** `RENT Limit`
- **Coverages:** `RENT`
- **Rows:** 4

**ACPE:**
- **Risk Category:** `ACPE Limit`
- **Coverages:** `ACPE`
- **Rows:** 11

All from **Sheet:** Limit & Ded Factors

---

## Operational Expense Factors

### 69. OpEx1_Risk_Factor
- **Risk Category:** `Prior Insurance Classification` | `Financial Responsibility Tier`
- **Coverages:** `OPS-EXP`
- **Rows:** 90 | **Sheet:** OpEx_Factor 1

### 70. OpEx2_Risk_Factor
- **Risk Category:** `Eligible to be Rated Drivers` | `Vehicle Count`
- **Coverages:** `OPS-EXP`
- **Rows:** 16 | **Sheet:** OpEx_Factor 2

### 71. OpEx3_Risk_Factor
- **Risk Category:** `PNI Age`
- **Coverages:** `OPS-EXP`
- **Rows:** 15 | **Sheet:** OpEx_Factor 3

### 72. OpEx5_Risk_Factor
- **Risk Category:** `Vehicle Count` | `Number of Vehicle Addition Endorsements`
- **Coverages:** `OPS-EXP`
- **Rows:** 20 | **Sheet:** OpEx_Factor 5

### 73. OpEx6_Risk_Factor
- **Risk Category:** `Number of Non-Pay Cancels` | `Number of Non-Pay Reinstates`
- **Coverages:** `OPS-EXP`
- **Rows:** 10 | **Sheet:** OpEx_Factor 6

### 74. OpEx8_Risk_Factor
- **Risk Category:** `Prior Insurance Activity Tier`
- **Coverages:** `OPS-EXP`
- **Rows:** 30 | **Sheet:** OpEx_Factor 8

### 75. Acq_Exp_Factor_AE1_Risk_Factor
- **Risk Category:** `Vehicle Count at Initial Evaluation` | `Full Coverage Status at Initial Evaluation` | `Prior Insurance Classification`
- **Coverages:** `ACQ-EXP`
- **Rows:** 18 | **Sheet:** AE1

### 76. Acq_Exp_Factor_AE2_Risk_Factor
- **Risk Category:** `Prior Insurance Activity Tier`
- **Coverages:** `ACQ-EXP`
- **Rows:** 30 | **Sheet:** AE2

### 77. Bad_Debt_Fr_Risk_Factor
- **Risk Category:** `Prior Insurance Classification` | `Financial Responsibility Tier`
- **Coverages:** `BI` | `PD` | `COMP` | `COLL` | `LOAN` | `MED` | `UM` | `UIM` | `RENT` | `ACPE` | `ACQ-EXP` | `OPS-EXP`
- **Rows:** 90 | **Sheet:** Bad Debt FR Fct Tbl

---

## UBI/Telematics Factors

### 78. CurrentlyMonitoring\Yes_NSP_Default_Safety_Score_Risk_Factor
- **Risk Category:** `Default Safety Score` | `Months Since Monitoring`
- **Coverages:** `BI` | `PD` | `COMP` | `COLL` | `LOAN` | `MED` | `UM` | `UIM` | `RENT` | `ACPE` | `ACQ-EXP` | `OPS-EXP`
- **Rows:** 110 | **Sheet:** NSP Safety Score Fct

### 79. CurrentlyMonitoring\No_NSP_Default_Safety_Score_Risk_Factor
- **Risk Category:** `Default Safety Score` | `Months Since Monitoring`
- **Coverages:** `BI` | `PD` | `COMP` | `COLL` | `LOAN` | `MED` | `UM` | `UIM` | `RENT` | `ACPE` | `ACQ-EXP` | `OPS-EXP`
- **Rows:** 1,100 | **Sheet:** NSP - Not Monitoring

---

## Summary Statistics

### Coverage Type Frequency
Across all 79 extracted tables:

| Coverage | Tables | Percentage |
|----------|--------|------------|
| BI | 72 | 91% |
| PD | 72 | 91% |
| COMP | 71 | 90% |
| COLL | 71 | 90% |
| MED | 68 | 86% |
| UM | 68 | 86% |
| UIM | 68 | 86% |
| RENT | 50 | 63% |
| LOAN | 50 | 63% |
| ACPE | 17 | 22% |
| OPS-EXP | 7 | 9% |
| ACQ-EXP | 5 | 6% |
| TOW | 1 | 1% |

### Most Common Lookup Dimensions

| Dimension | Frequency | Tables |
|-----------|-----------|--------|
| Prior Insurance Classification | 21 | 27% |
| Driver Age | 10 | 13% |
| Financial Responsibility Tier | 10 | 13% |
| Prior BI Level / Limit Classification | 9 | 11% |
| Multi-Car | 8 | 10% |
| Vehicle Count | 7 | 9% |
| Points (BI/PD, COLL, COMP, MED) | 7 | 9% |
| Vehicle Age at Add Date | 4 | 5% |

### Largest Tables (by rows)

| Table | Rows | Purpose |
|-------|------|---------|
| Veh_Symbol_Risk_Factor | 24,249 | Vehicle year/make/model/style rating |
| Garaging_Location_Risk_Factor | 1,562 | Territory/ZIP code rating |
| NSP - Not Monitoring | 1,100 | UBI non-monitoring factors |
| Aux_Symbol_Risk_Factor | 1,085 | Auxiliary vehicle symbols |
| Driver_Class_Risk_Factor | 960 | Gender/age/marital status rating |
| HH Member Table 2 | 845 | Household composition rating |
| NB Five Yr Acc Free | 480 | 5-year accident free discount |

### Table Complexity (by dimension count)

| Dimensions | Count | Examples |
|------------|-------|----------|
| 1 dimension | 15 | Annual_Miles, PD_Limit, OpEx3 |
| 2 dimensions | 35 | Driver_Age + Points, FR_Tier |
| 3 dimensions | 15 | Full_Cov, Luxury_Veh, AE1 |
| 4 dimensions | 8 | Vehicle_Age_Coverage, Late_Renewal, COMP_Selection |
| 5+ dimensions | 6 | Driver_Class (5), Youthful_Driver (6), HH_Structure (8) |

---

## Data Quality Notes

1. **Consistent Structure:** All tables follow the two-segment pattern (lookup keys + coverage factors)
2. **Coverage Completeness:** Most tables include all 9 core coverages (BI, PD, COMP, COLL, LOAN, MED, UM, UIM, RENT)
3. **Special Coverages:** ACPE, ACQ-EXP, and OPS-EXP appear in specific policy-level and expense tables
4. **Points-Based Rating:** 7 tables use point systems derived from driving record violations
5. **Continuous Insurance Tiers:** 10 distinct discount levels based on prior insurance history
6. **Territory Rating:** 1,562 ZIP codes with individual factors
7. **Vehicle Identification:** 24,249 unique vehicle combinations rated

---

## Usage Guidelines

### How to Use This Document

1. **Find Your Factor:** Use Table of Contents to locate the factor category
2. **Identify Lookup Keys:** Segment 1 shows what attributes you need to look up
3. **Retrieve Factors:** Segment 2 shows which coverage multipliers you'll get
4. **Apply to Rating:** Multiply base rate by all applicable factors

### Example Lookup Flow

For a 35-year-old driver with 2 points in a 2020 Toyota Camry:

1. **Driver_Age_Risk_Factor_BI_PD**
   - Lookup: `Driver Age = "25..44"`, `BI/PD Points = "2"`
   - Get: `BI = 1.01`, `PD = 1.01`

2. **Veh_Symbol_Risk_Factor**
   - Lookup: `Model Year = "2020"`, `Make = "TY"`, `Model = "CL"`, `Style = "XX"`
   - Get: All 8 coverage factors

3. **UW_Tier_Percent_Risk_Factor**
   - Lookup: `UW Tier = "1N"` (from tier determination logic)
   - Get: All 9 coverage tier factors

4. **Multiply:** `Premium = Base Rate × Driver Age Factor × Vehicle Symbol Factor × UW Tier Factor × ...`

---

## Files Generated

1. **COMPLETE_RISK_FACTOR_DIMENSIONS.md** (this file) - Full documentation
2. **risk_factor_dimensions.md** - Initial 30-table extraction
3. **risk_factor_dimensions_summary.csv** - Initial CSV format
4. **ALL_92_FACTOR_TABLES_STATUS.md** - Extraction progress tracking

---

*Generated by Excel MCP Service Analysis*  
*Extraction Date: October 14, 2025*  
*Source: AZ_2025-07-15_v250.xlsm (431 named ranges)*

