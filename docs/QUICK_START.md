# Quality Places Scraper - Quick Start

## 🎯 What You Get

A fully automated n8n workflow that:
- ✅ Scrapes Google Places for cities from your list
- ✅ Filters ONLY quality places (4.0+ stars, 50+ reviews, active)
- ✅ Returns TOP 5 best places per city
- ✅ Saves to Google Sheets automatically
- ✅ Processes: Country → State → City (hierarchical)

## 🚀 Quick Setup (5 Minutes)

### Step 1: Prepare Google Sheets
1. Open: https://docs.google.com/spreadsheets/d/1x38HGrufco-IF_w_GL7GqCFlabNMYfI9-uWAQ3ESOAk
2. Create 2 new sheets:
   - **"Locations"** (input) 
   - **"Results"** (output)

### Step 2: Add Your Cities to "Locations" Sheet
Copy this into the "Locations" sheet:

```
Country         State                           City              Category
USA             California                      Los Angeles       restaurant
USA             California                      San Francisco     hotel
France          Île-de-France                   Paris             restaurant
UK              England                         London            hotel
```

Or import the CSV file: `locations_input_template.csv`

### Step 3: Import Workflow to n8n
1. Go to: https://n8n.iwilltravelto.com
2. Click "+ Add workflow" → "Import from File"
3. Upload: `quality_places_scraper_workflow.json`

### Step 4: Set Up Apify Credential
1. In n8n, go to **Credentials** → **Add Credential**
2. Choose **"Header Auth"**
3. Name: `Apify API`
4. Header Name: `Authorization`
5. Header Value: `Bearer YOUR_APIFY_API_TOKEN`
6. Save

### Step 5: Activate Workflow
1. Open the imported workflow
2. Toggle **"Active"** to ON
3. Click **"Save"**

**Done!** The workflow runs every 6 hours automatically.

## 📊 How to Read Results

Your "Results" sheet will have these columns for each city:

| Column | Meaning |
|--------|---------|
| `TotalFound` | Total places Apify found |
| `QualityPlaces` | How many passed quality filters (4.0+ stars, 50+ reviews) |
| `Place1_Name` | Name of #1 ranked place |
| `Place1_Rating` | Rating (4.0-5.0) |
| `Place1_Reviews` | Number of reviews (min 50) |
| `Place1_Address` | Full address |
| `Place1_Phone` | Phone number |
| `Place1_Website` | Website URL |
| `Place1_GoogleMapsURL` | Google Maps link |

...and same fields for Place2, Place3, Place4, Place5.

## 🎚️ Quality Filters

**Default settings** (change in "Filter Top 5 Quality Places" node):

```javascript
MIN_RATING = 4.0      // Minimum 4 stars
MIN_REVIEWS = 50      // Minimum 50 reviews
MAX_RESULTS = 5       // Top 5 places per city
```

**Ranking logic:**
1. Sort by rating (highest first)
2. If tied, sort by review count (most popular first)

## 🧪 Test First

Before running on all cities:

1. Add just **1 city** to "Locations" sheet
2. In n8n workflow, click **"Execute Workflow"** (manual test)
3. Wait 2-3 minutes
4. Check "Results" sheet

If it works, add more cities!

## 📁 Files

- `locations_input_template.csv` - CSV template for cities
- `quality_places_scraper_workflow.json` - Import this to n8n
- `QUALITY_SCRAPER_GUIDE.md` - Full documentation
- `QUICK_START.md` - This file

## 🆘 Troubleshooting

**No results?**
- Check city spelling
- Lower MIN_RATING to 3.5
- Lower MIN_REVIEWS to 20

**Less than 5 places?**
- City doesn't have 5 quality places
- Lower the quality filters

**API errors?**
- Check Apify token is correct
- Verify Apify quota at: https://console.apify.com

## 📞 Categories You Can Use

- `restaurant`
- `hotel`
- `cafe`
- `bar`
- `tourist_attraction`
- `museum`
- `shopping_mall`
- `spa`
- `gym`
- `nightclub`

## ⏱️ Processing Time

- 1 city = ~2-3 minutes
- 10 cities = ~20-30 minutes
- 100 cities = ~3-5 hours

**Tip**: Process cities in batches (10-20 at a time).

## 🎯 What Makes a Place "Quality"?

✅ **4.0+ stars** - Top 20% rated places  
✅ **50+ reviews** - Proven popular (not just 2-3 lucky reviews)  
✅ **Active** - Not permanently or temporarily closed  
✅ **Ranked** - Best rated + most popular first  

**Result**: Only recommend-worthy places people actually trust!

---

Need help? Check `QUALITY_SCRAPER_GUIDE.md` for full documentation.
