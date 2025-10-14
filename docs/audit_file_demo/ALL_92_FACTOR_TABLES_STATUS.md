# Complete List of ALL 92 Factor & Point Tables

**Status:** ✅ = Headers Extracted | ⏳ = Pending Extraction  
**Source:** AZ_2025-07-15_v250.xlsm

---

## Summary
- **Total Factor/Point Tables:** 92
- **Extracted So Far:** ~55
- **Remaining:** ~37

---

## Driver Risk Factors (20 tables)

| # | Named Range | Status | Segment 1 Dimensions | Segment 2 Coverages |
|---|-------------|--------|---------------------|-------------------|
| 1 | Driver_Age_Risk_Factor_BI_PD | ✅ | Driver Age \| BI/PD Points | BI \| PD |
| 2 | Driver_Age_Risk_Factor_Coll | ✅ | Driver Age \| COLL Points | COLL \| RENT |
| 3 | Driver_Age_Risk_Factor_Comp | ✅ | Driver Age \| COMP Points | COMP \| LOAN |
| 4 | Driver_Age_Risk_Factor_Med | ✅ | Driver Age \| MED Points | MED \| UM \| UIM |
| 5 | Driver_Class_Risk_Factor | ✅ | Gender \| Marital Status \| Driver Age \| Months Since Last Birthday \| Ratable Spouse | All 9 coverages |
| 6 | Driver_License_Type_Risk_Factor | ✅ | License Type Code \| Driver Age | BI \| PD \| COMP \| COLL \| MED \| UM \| UIM |
| 7 | Driver_Training_Disc_Risk_Factor | ✅ | Driver Age \| Driver Training Discount | All 9 coverages |
| 8 | Years_Licensed_Risk_Factor | ✅ | Driver Age \| Years Licensed | All 9 coverages + RENT |
| 9 | Youthful_Driver_Disc_Risk_Factor | ✅ | Driver Age \| Clean Driver \| Distant Student Disc \| Good Student Disc \| Teen Driver Disc \| Driver Add Date Class | All 9 coverages |
| 10 | Senior_Mature_Driver_Factor | ⏳ | TBD | TBD |
| 11 | Financial_Resp_By_Clean_Risk_Factor | ✅ | Financial Responsibility Tier \| Clean Driver | All 9 coverages |
| 12 | Financial_Resp_By_Num_Of_Drivers_Risk_Factor | ⏳ | TBD | TBD |
| 13 | Occupation_Education_Risk_Factor | ✅ | Prior Insurance Classification \| Occupation Education Rank | 8 coverages (no RENT) |
| 14 | HhMemberTable\1_HH_Member_Risk_Factor | ✅ | Vehicle Count \| Household Member Count \| Driver Age | All 9 coverages |
| 15 | HhMemberTable\2_HH_Member_Risk_Factor | ✅ | Vehicle Count \| Household Member Count \| Driver Age | All 9 coverages |
| 16 | Driving_Record_Points_Risk_Point_BI_PD | ✅ | BI/PD Points | BI \| PD |
| 17 | Driving_Record_Points_Risk_Point_Coll | ✅ | COLL Points | COLL \| RENT |
| 18 | Driving_Record_Points_Risk_Point_Comp | ✅ | COMP Points | COMP \| LOAN |
| 19 | Driving_Record_Points_Risk_Point_Med | ✅ | MED Points | MED \| UM \| UIM |
| 20 | Subtraction_Of_Unity_Risk_Point | ⏳ | TBD | TBD |

---

## Vehicle Risk Factors (25 tables)

| # | Named Range | Status | Segment 1 Dimensions | Segment 2 Coverages |
|---|-------------|--------|---------------------|-------------------|
| 21 | Vehicle_Age_Risk_Factor | ✅ | Vehicle Risk Group Code at Initial Vehicle Evaluation \| Vehicle Age at Add Date | All 9 coverages |
| 22 | Vehicle_Age_Coverage_Risk_Factor | ✅ | Vehicle Tenure \| Vehicle Age at Add Date \| Multi-Car \| Full Coverage on Vehicle | All 9 coverages |
| 23 | Veh_Symbol_Risk_Factor | ✅ | Model Year \| Make \| Model \| Style | 8 coverages (no RENT) |
| 24 | Aux_Symbol_Risk_Factor | ✅ | Auxiliary Symbol | 8 coverages (no RENT) |
| 25 | Vehicle_Attributes_Rating_Risk_Factor | ✅ | Multi-Car \| Vehicle Type Code \| Convertible Indicator \| Vehicle Horsepower Code | 8 coverages |
| 26 | Vehicle_History_Rating_Risk_Factor | ⏳ | TBD | TBD |
| 27 | Luxury_Veh_Risk_Factor | ✅ | PNI Age \| Luxury Vehicle on Policy \| Vehicle Count | 8 coverages |
| 28 | Annual_Miles_Risk_Factor | ✅ | Annual Miles | 7 coverages (no LOAN, RENT, ACPE) |
| 29 | Garaging_Location_Risk_Factor | ✅ | Garaging ZIP Code | All 10 coverages (includes ACPE) |
| 30 | Length_Of_Veh_Ownership_Risk_Factor | ✅ | Vehicle Tenure \| Vehicle Age at Add Date \| Length of Vehicle Ownership | All 9 coverages |
| 31 | Excess_Veh_Risk_Factor | ✅ | Excess Vehicle | 8 coverages |
| 32 | Business_Use_Surcharge_Risk_Factor | ✅ | Business Use | All 10 coverages |
| 33 | Rideshare_Use_Factor_Table | ⏳ | TBD | TBD |
| 34 | Population_Density_Fact_Tbl | ⏳ | TBD | TBD |
| 35 | Value_Class_Symbol_Factors | ⏳ | TBD | TBD |
| 36 | Average_By_Number_Of_Vehicles_Risk_Factor | ⏳ | TBD | TBD |
| 37 | Financial_Resp_Filing_Surcharge_Risk_Factor | ✅ | Financial Responsibility Filing Surcharge | 7 coverages |
| 38 | FR_Tier_Risk_Factor | ✅ | Financial Responsibility Tier \| Prior Insurance Classification | All 9 coverages |
| 39 | Acq_Exp_Factor_AE1_Risk_Factor | ✅ | Vehicle Count at Initial Evaluation \| Full Coverage Status at Initial Evaluation \| Prior Insurance Class | ACQ-EXP only |
| 40 | Acq_Exp_Factor_AE2_Risk_Factor | ✅ | Prior Insurance Activity Tier | ACQ-EXP only |
| 41 | Bad_Debt_Fr_Risk_Factor | ✅ | Prior Insurance Classification \| Financial Responsibility Tier | All 12 (includes ACQ-EXP, OPS-EXP) |
| 42 | Bad_Debt_PIAT_Fct_Tbl | ⏳ | TBD | TBD |
| 43 | Bad_Debt_Renew_With_Lapse_Fct | ⏳ | TBD | TBD |
| 44 | Risk_Group_Code_Risk_Factor | ✅ | Risk Group Code | All 10 coverages |
| 45 | UBI_Tier_Fct_-_OBD | ⏳ | TBD | TBD |

---

## Household/Policy Risk Factors (8 tables)

| # | Named Range | Status | Segment 1 Dimensions | Segment 2 Coverages |
|---|-------------|--------|---------------------|-------------------|
| 46 | HH_Structure_Risk_Factor | ✅ | Multi-Car \| PNI Marital Status \| PNI Youthful \| Youthful Drivers \| rated drivers \| Eligible to be Rated Drivers \| Rated Youthful Drivers \| Rated Driver Gender | 8 coverages |
| 47 | Full_Cov_Risk_Factor | ✅ | Prior BI Level \| Full Coverage On Policy \| Multi-Car | BI \| PD \| MED \| UM \| UIM |
| 48 | Late_Renewal_Risk_Factor | ✅ | Prior BI Level \| Number of Lapse Days 1..10 \| Number of Lapse Days 11..30 \| Number of Lapse Days 31..99999 | All 10 coverages |
| 49 | Advance_Quote_Risk_Factor | ✅ | Prior Insurance Classification \| Advance Shop Days \| Advance Quote Discount | All 10 coverages |
| 50 | Advanced_Quote_Table | ⏳ | TBD (likely duplicate of above) | TBD |
| 51 | Renew_With_Lapse_Factor | ⏳ | TBD | TBD |
| 52 | Omitted_Incident_Fct_Table | ⏳ | TBD | TBD |
| 53 | Diminishing_Ded_Option | ⏳ | TBD | TBD |

---

## Discount Factors (20 tables)

### Continuous Insurance Discounts (10 levels)
| # | Named Range | Status | Segment 1 Dimensions | Segment 2 Coverages |
|---|-------------|--------|---------------------|-------------------|
| 54 | DiscountLevel\Diamond_Cont_Ins_Disc_Risk_Factor | ✅ | Prior Insurance Class \| Prior BI Limit Class \| Silver Cont Ins Disc at Current Policy Inception \| Gold Cont Ins Disc at Current Policy Inception | All 9 coverages |
| 55 | DiscountLevel\DiamondSelect_Cont_Ins_Disc_Risk_Factor | ⏳ | TBD | TBD |
| 56 | DiscountLevel\Platinum1_Cont_Ins_Disc_Risk_Factor | ✅ | Prior Insurance Class \| Prior BI Limit Class \| Silver Cont Ins Disc \| Gold Cont Ins Disc | All 9 coverages |
| 57 | DiscountLevel\Platinum1Select_Cont_Ins_Disc_Risk_Factor | ⏳ | TBD | TBD |
| 58 | DiscountLevel\Platinum2Select_Cont_Ins_Disc_Risk_Factor | ⏳ | TBD | TBD |
| 59 | DiscountLevel\Gold_Cont_Ins_Disc_Risk_Factor | ✅ | Prior Insurance Classification \| Prior BI Limit Classification | All 9 coverages |
| 60 | DiscountLevel\GoldSelect_Cont_Ins_Disc_Risk_Factor | ⏳ | TBD | TBD |
| 61 | DiscountLevel\Silver_Cont_Ins_Disc_Risk_Factor | ✅ | Prior Insurance Classification \| Prior BI Limit Classification | All 9 coverages |
| 62 | DiscountLevel\SilverSelect_Cont_Ins_Disc_Risk_Factor | ⏳ | TBD | TBD |
| 63 | DiscountLevel\NoDisc_Cont_Ins_Disc_Risk_Factor | ✅ | Prior Insurance Classification \| Prior BI Limit Classification | All 9 coverages |

### Other Discounts
| # | Named Range | Status | Segment 1 Dimensions | Segment 2 Coverages |
|---|-------------|--------|---------------------|-------------------|
| 64 | Three_Year_Safe_Dr_Disc_Risk_Factor | ✅ | Three Year Safe Driving Discount Eligibility \| Prior BI Level \| Multi-Car | All 10 coverages |
| 65 | NB_Five_Yr_Acc_Free_Claim_Free_Disc_Risk_Factor | ✅ | New Business Five Year Accident Free Discount Eligibility \| Five Year Claim Free Eligibility \| Prior BI Level \| Multi-Car \| Current Policy Tenure | All 10 coverages |
| 66 | Home_MH_MC_Disc_Risk_Factor | ✅ | Prior BI Level \| Multi-Car \| Homeowner \| Mobile Home Owner | 8 coverages (no LOAN, ACPE) |
| 67 | NB_NSP_Disc_Risk_Factor | ✅ | NSP Participation Discount | All 12 (includes ACQ-EXP, OPS-EXP) |
| 68 | E-Signature_Discount | ⏳ | TBD | TBD |
| 69 | Online_Quote_Disc_Tbl | ⏳ | TBD | TBD |
| 70 | Paperless_Disc_Table | ⏳ | TBD | TBD |
| 71 | Multi-Policy_Discount_Table | ⏳ | TBD | TBD |
| 72 | Partnership_Disc | ⏳ | TBD | TBD |
| 73 | SmartTech_Disc_Table | ⏳ | TBD | TBD |

---

## Tier & Rate Factors (5 tables)

| # | Named Range | Status | Segment 1 Dimensions | Segment 2 Coverages |
|---|-------------|--------|---------------------|-------------------|
| 74 | UW_Tier_Percent_Risk_Factor | ✅ | UW Tier | All 9 coverages |
| 75 | Tier_Factor_Table | ⏳ | TBD (likely same as UW_Tier) | TBD |
| 76 | Base_Rates_Risk_Rate | ✅ | x (placeholder) | All 12 (includes ACQ-EXP, OPS-EXP) |
| 77 | Monthly_Rate_Risk_Factor | ✅ | Trend Months | All 10 coverages |
| 78 | Policy_Term_Risk_Factor | ✅ | Policy Term | All 12 coverages |

---

## Coverage & Limit Factors (12 tables)

| # | Named Range | Status | Segment 1 Dimensions | Segment 2 Coverages |
|---|-------------|--------|---------------------|-------------------|
| 79 | Coverage_Selection_COLL_Risk_Factor | ✅ | COLL Deductible at Initial Evaluation \| COLL Deductible | All 10 coverages |
| 80 | Coverage_Selection_COMP_Risk_Factor | ⏳ | TBD | TBD |
| 81 | Limit_And_Ded_Risk_Factor_BI | ✅ | Prior Insurance Indicator \| BI Limit | BI only |
| 82 | Limit_And_Ded_Risk_Factor_PD | ⏳ | TBD | TBD |
| 83 | Limit_And_Ded_Risk_Factor_COMP | ⏳ | TBD | TBD |
| 84 | Limit_And_Ded_Risk_Factor_Coll | ⏳ | TBD | TBD |
| 85 | Limit_And_Ded_Risk_Factor_Med | ⏳ | TBD | TBD |
| 86 | Limit_And_Ded_Risk_Factor_UM | ⏳ | TBD | TBD |
| 87 | Limit_And_Ded_Risk_Factor_UIM | ⏳ | TBD | TBD |
| 88 | Limit_And_Ded_Risk_Factor_Loan | ⏳ | TBD | TBD |
| 89 | Limit_And_Ded_Risk_Factor_Rent | ⏳ | TBD | TBD |
| 90 | Limit_And_Ded_Risk_Factor_ACPE | ⏳ | TBD | TBD |

---

## Operational Expense Factors (2 tables)

| # | Named Range | Status | Segment 1 Dimensions | Segment 2 Coverages |
|---|-------------|--------|---------------------|-------------------|
| 91 | OpEx1_Risk_Factor | ✅ | Prior Insurance Classification \| Financial Responsibility Tier | OPS-EXP only |
| 92 | OpEx2_Risk_Factor | ✅ | Eligible to be Rated Drivers \| Vehicle Count | OPS-EXP only |
| -- | OpEx3_Risk_Factor | ✅ | PNI Age | OPS-EXP only |
| -- | OpEx5_Risk_Factor | ✅ | Vehicle Count \| Number of Vehicle Addition Endorsements | OPS-EXP only |
| -- | OpEx6_Risk_Factor | ✅ | Number of Non-Pay Cancels \| Number of Non-Pay Reinstates | OPS-EXP only |
| -- | OpEx8_Risk_Factor | ✅ | Prior Insurance Activity Tier | OPS-EXP only |

**Note:** There are actually MORE OpEx factors (OpEx 1-14 mentioned in named ranges) than originally counted.

---

## Additional UBI/NSP Factors (not in original 92 count)

| Named Range | Status | Notes |
|-------------|--------|-------|
| UBI_Tier_Fct_-_Mobile | ⏳ | UBI telematics factors |
| NSP_Safety_Score_Fct | ⏳ | NovoNav safety score |
| CurrentlyMonitoring\Yes_NSP_Default_Safety_Score_Risk_Factor | ⏳ | NSP monitoring |
| CurrentlyMonitoring\No_NSP_Default_Safety_Score_Risk_Factor | ⏳ | NSP not monitoring |
| Not_Monitoring_Duration | ⏳ | NSP duration factors |
| Safety_Score_Movement | ⏳ | NSP score changes |

---

## Summary of Remaining Work

**Still Need to Extract (~37 tables):**
1. All "Select" Continuous Insurance Discount levels (5 tables)
2. Remaining Limit & Ded factors (10 tables: PD, COMP, Coll, Med, UM, UIM, Loan, Rent, ACPE)
3. Coverage_Selection_COMP_Risk_Factor
4. UBI/NSP factors (6+ tables)
5. Additional discount tables (7 tables: E-Signature, Online Quote, Paperless, Multi-Policy, Partnership, SmartTech)
6. Miscellaneous factors (8 tables: Senior Mature Driver, Financial Resp By Num Of Drivers, Vehicle History Rating, etc.)

---

**Next Steps:**
1. Continue extracting remaining 37+ tables
2. Update comprehensive documentation with all headers
3. Create final complete CSV summary

