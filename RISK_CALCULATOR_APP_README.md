# 📊 Risk Calculation Table Generator - Streamlit App

A web application that generates risk calculation tables from insurance application JSON data.

## 🚀 Quick Start

### Option 1: Using the run script (Recommended)
```bash
./run_risk_calculator.sh
```

### Option 2: Direct command
```bash
# Activate virtual environment
source venv/bin/activate

# Run the app
streamlit run src/streamlit_risk_calculator.py
```

The app will automatically open in your default web browser at `http://localhost:8501`

## 📋 Features

### Main Features
- **JSON Input**: Paste your insurance application JSON directly into the web interface
- **Automatic Processing**: Generates all risk calculation tables based on the application data
- **Multiple Views**: 
  - All tables view
  - Driver-specific tables
  - Vehicle-specific tables
- **Statistics Dashboard**: Real-time metrics showing table counts and breakdowns
- **Search & Filter**: Search through risk dimensions to find specific tables
- **Export**: Download results as JSON file

### Sample Data
- Click the "📄 Load Sample Data" button in the sidebar to load a sample application
- Uses the economy.json file from the demo_application folder

## 📊 How It Works

1. **Input**: Paste your application JSON containing:
   - `riskProfile.drivers`: Array of driver data
   - `riskProfile.vehicles`: Array of vehicle data

2. **Processing**: The app uses the `risk_subject_ite.py` module to:
   - Categorize risk factors by subject type (driver/vehicle/household)
   - Create risk calculation tables for each combination of:
     - Driver × Driver Risk Dimensions
     - Vehicle × Vehicle Risk Dimensions

3. **Output**: Displays:
   - Total number of risk calculation tables
   - Breakdown by type (driver vs vehicle)
   - Detailed table information with subject IDs
   - Searchable and filterable results

## 🔢 Calculation Logic

**Risk Calculation Tables** are generated based on:
- **Driver Tables** = (Number of Driver Risk Dimensions) × (Number of Drivers)
- **Vehicle Tables** = (Number of Vehicle Risk Dimensions) × (Number of Vehicles)

For example, with:
- 35 driver risk dimensions
- 68 vehicle risk dimensions
- 2 drivers
- 3 vehicles

You get:
- Driver Tables: 35 × 2 = 70
- Vehicle Tables: 68 × 3 = 204
- **Total: 274 tables**

## 📁 Input JSON Structure

```json
{
  "riskProfile": {
    "drivers": [
      {
        "id": "D001",
        "firstName": "John",
        "lastName": "Doe",
        // ... other driver fields
      }
    ],
    "vehicles": [
      {
        "id": "VIN123456789",
        "make": "Toyota",
        "model": "Camry",
        // ... other vehicle fields
      }
    ]
  }
}
```

## 🎯 Use Cases

- **Risk Assessment**: Review all risk dimensions that need to be evaluated
- **Policy Review**: Understand the complete risk profile of an application
- **Audit & Compliance**: Generate comprehensive risk calculation documentation
- **Testing**: Validate that all required risk factors are being calculated

## 🛠️ Technical Details

### Dependencies
- `streamlit`: Web application framework
- `utils.risk_subject_ite`: Core risk calculation logic
- Standard Python libraries (json, sys, os, typing)

### Risk Subject Types
The app recognizes three risk subject types:
- **🚗 Vehicle**: Vehicle-specific risk factors (68 factors)
- **👤 Driver**: Driver-specific risk factors (32 factors)
- **🏠 Household**: Household-specific risk factors (3 factors)

Note: Household factors are grouped with driver factors in the calculation logic.

### Key Functions Used
- `risk_subject_iter()`: Categorizes risk factors by subject type
- `prepare_risk_calculation_tables()`: Generates the risk calculation tables
- `AZ_HARDCODE_RISK_SUBJECT_MAP`: Maps risk dimensions to subject types

## 📈 Output Format

The app provides multiple output formats:

### 1. Interactive Table View
- Sortable and scrollable dataframe
- Shows: Index, Type, Risk Dimension, Subject ID

### 2. JSON Export
```json
[
  {
    "index": 1,
    "type": "driver",
    "risk_dimension": "driver-age-risk-factor-bi-pd",
    "subject_id": "D001"
  },
  // ... more tables
]
```

### 3. Detailed View
- Full information for each table
- Subject details (name, VIN, etc.)
- Searchable by risk dimension name

## 🎨 UI Features

- **Responsive Layout**: Two-column design for input and statistics
- **Tabbed Interface**: Organize views by table type
- **Metrics Dashboard**: Visual display of key statistics
- **Progress Indicators**: Loading spinners during processing
- **Color-Coded Types**: Easy identification of risk subject types
- **Download Button**: Export results with one click

## ⚙️ Configuration

The app uses hardcoded risk subject mappings from `AZ_HARDCODE_RISK_SUBJECT_MAP` which contains 103 risk factors mapped to their subject types.

To modify risk factors:
1. Edit `src/utils/risk_subject_ite.py`
2. Update the `AZ_HARDCODE_RISK_SUBJECT_MAP` dictionary
3. Restart the Streamlit app

## 🐛 Troubleshooting

### "Invalid JSON format" error
- Ensure your JSON is properly formatted
- Check for missing commas, brackets, or quotes
- Use a JSON validator tool

### "riskProfile key not found" error
- Verify your JSON has the correct structure
- Ensure `riskProfile` is at the top level
- Check that `drivers` and `vehicles` arrays exist

### App won't start
- Ensure virtual environment is activated
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Verify Streamlit is installed: `pip install streamlit`

## 📞 Support

For issues or questions:
1. Check the sidebar "ℹ️ Information" section in the app
2. Review the sample data format
3. Ensure your application JSON matches the expected structure

---

**Version**: 1.0  
**Built with**: Streamlit 🎈  
**Last Updated**: October 2025




