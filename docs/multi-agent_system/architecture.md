**Agent Responsibilities:**
1. **Orchestrator Agent (Master Agent)**
   - Receives and validates insurance applications
   - Manages overall workflow coordination
   - Initializes context (timestamp, product type)
   - Coordinates risk factor processing loop
   - Collects and aggregates risk factor values
   - Manages the premium calculation process

2. **Product Definition Agent**
   - Defines required risk factors for products
   - Provides risk factor definitions `<risk_subject, risk_factor_name>[]`
   - Supplies assessment rules for each risk factor
   - Maintains product-specific rule configurations
   - Defines how risk factors should be evaluated

3. **Risk Factor Reasoning Agent**
   - Applies assessment rules to application data
   - Coordinates with Lookup Agent for mapping values
   - Determines risk tier values
   - Validates rule application results
   - Returns calculated risk factor values

4. **Data Lookup Agent**
   - Provides mapping values during risk calculation
   - Maps risk tiers to specific values
   - Provides coverage values for premium calculation
   - Maintains lookup tables and mappings

5. **Premium Calculation Agent**
   - Applies premium calculation formulas
   - Processes risk factors and coverage values
   - Calculates final premium amount
   - Validates calculation results


   ```plantuml

   @startuml AI Rating Engine Flow

actor User
participant "Orchestrator\nAgent" as OA
participant "Product Definition\nAgent" as PDA
participant "Risk Factor\nReasoning Agent" as RFRA
participant "Data Lookup\nAgent" as LA
participant "Premium Calculation\nAgent" as PCA

== Initialization Phase ==

User -> OA: Submit Insurance Application\n(includes historical data)
activate OA

OA -> OA: Initialize Context\n(timestamp, product type)
OA -> PDA: Request Product Definition
activate PDA

PDA -> PDA: Load Risk Factor Definitions\n<risk_subject, risk_factor_name>[]
PDA --> OA: Return Risk Factor Definitions\nand Assessment Rules
deactivate PDA

== Risk Assessment Phase ==

OA -> OA: Begin Risk Factor Processing
loop For Each Risk Factor
    OA -> PDA: Get Risk Assessment Rules\nfor Current Risk Factor
    activate PDA
    PDA --> OA: Return Factor-Specific Rules
    deactivate PDA
    
    OA -> RFRA: Determine Risk Tier\n(application + rules)
    activate RFRA
    
    RFRA -> LA: Lookup Mapping Value\n(for risk calculation)
    activate LA
    LA --> RFRA: Return Mapped Value
    deactivate LA
    
    RFRA -> RFRA: Apply Rules to Application Data
    RFRA --> OA: Return Risk Factor Value
    deactivate RFRA
end

== Premium Calculation Phase ==

OA -> LA: Lookup Coverage Values\n(based on risk factors)
activate LA
LA --> OA: Return Coverage Values
deactivate LA

OA -> PCA: Calculate Premium\n(risk factors + coverage values)
activate PCA
PCA -> PCA: Apply Premium Formula
PCA --> OA: Return Final Premium
deactivate PCA

OA --> User: Return Quote Result
deactivate OA

@enduml
   ```