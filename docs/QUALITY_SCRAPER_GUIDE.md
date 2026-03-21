# Quality Places Scraper - Complete Setup Guide

## 📋 Overview

This n8n workflow automatically scrapes Google Places for the **TOP 5 QUALITY locations** per city based on:
- ⭐ **Rating**: Minimum 4.0 stars
- 💬 **Reviews**: Minimum 50 reviews (proves it's popular)
- ✅ **Active**: Not closed permanently or temporarily
- 🏆 **Ranking**: Sorted by rating (highest first), then review count

## 🎯 What It Does

1. Reads your list of cities from Google Sheets (Country > State > City format)
2. Scrapes Google Places for each city and category
3. Filters out low-quality places (below 4 stars, less than 50 reviews)
4. Ranks remaining places by rating and popularity
5. Saves the TOP 5 places per city back to Google Sheets
6. Processes one city at a time (Country 1 > State 1 > City 1 > City 2 > State 2 > Country 2)

## 📊 Google Sheets Setup

You need **2 sheets** in your Google Sheets document:

### Sheet 1: "Locations" (Input)
This is where you list all cities you want to scrape.

**Columns:**
```
Country | State | City | Category
```

**Example:**
```csv
USA,California,Los Angeles,restaurant
USA,California,Los Angeles,hotel
USA,California,San Francisco,restaurant
France,Île-de-France,Paris,restaurant
UK,England,London,hotel
```

**Categories you can use:**
- `restaurant`
- `hotel`
- `cafe`
- `bar`
- `tourist_attraction`
- `museum`
- `park`
- `shopping_mall`
- `gym`
- `spa`

### Sheet 2: "Results" (Output)
This is where the workflow saves results. The workflow will auto-create columns, but here's the structure:

**Columns (auto-generated):**
```
Country | State | City | Category | TotalFound | QualityPlaces | LastScraped |
Place1_Name | Place1_Rating | Place1_Reviews | Place1_Address | Place1_Phone | Place1_Website | Place1_Category | Place1_PriceLevel | Place1_Image | Place1_GoogleMapsURL | Place1_Latitude | Place1_Longitude |
Place2_Name | Place2_Rating | ... (same fields for Place 2) |
Place3_Name | Place3_Rating | ... (same fields for Place 3) |
Place4_Name | Place4_Rating | ... (same fields for Place 4) |
Place5_Name | Place5_Rating | ... (same fields for Place 5)
```

## 🚀 Installation Steps

### Step 1: Prepare Your Google Sheet

1. Go to your existing Google Sheet: `1x38HGrufco-IF_w_GL7GqCFlabNMYfI9-uWAQ3ESOAk`
2. Create a new sheet named **"Locations"**
3. Add the header row: `Country | State | City | Category`
4. Add your cities (see example above)
5. Create another sheet named **"Results"** (leave it empty, workflow will populate it)

### Step 2: Upload the CSV Template (Alternative)

If you prefer working with CSV files:

1. Use the provided `locations_input_template.csv`
2. Edit it with your cities
3. Import it into your Google Sheet as "Locations" sheet

### Step 3: Import the Workflow to n8n

**Option A: Via n8n UI (Recommended)**
1. Go to https://n8n.iwilltravelto.com
2. Click **"Add workflow"** > **"Import from File"**
3. Upload `quality_places_scraper_workflow.json`
4. The workflow will be imported with all nodes configured

**Option B: Via n8n API**
```bash
curl -X POST "https://n8n.iwilltravelto.com/api/v1/workflows" \
  -H "X-N8N-API-KEY: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d @quality_places_scraper_workflow.json
```

### Step 4: Configure Credentials

You need to set up 2 credentials in n8n:

#### A. Google Sheets Credential
- Already exists: `QLIUHzCUR4PCeaCP` (Google Sheets account)
- No action needed if it's still working

#### B. Apify API Credential
You need to create an **HTTP Header Auth** credential:

1. In n8n, go to **Credentials** > **Add Credential**
2. Choose **"Header Auth"**
3. Name it: **"Apify API"**
4. Add header:
   - **Name**: `Authorization`
   - **Value**: `Bearer YOUR_APIFY_API_TOKEN`
5. Save

### Step 5: Activate the Workflow

1. Open the workflow in n8n
2. Click the **"Active"** toggle in the top right
3. Click **"Save"**

The workflow will now run **every 6 hours automatically**.

## ⚙️ Customization Options

### Change Scraping Frequency

Edit the **"Schedule Every 6 Hours"** node:
- Every hour: `hoursInterval: 1`
- Every 12 hours: `hoursInterval: 12`
- Daily: Change to `days` field with `daysInterval: 1`

### Adjust Quality Filters

Edit the **"Filter Top 5 Quality Places"** node, change these values:

```javascript
const MIN_RATING = 4.0;      // Minimum star rating (1.0 - 5.0)
const MIN_REVIEWS = 50;      // Minimum number of reviews
const MAX_RESULTS = 5;       // How many places per city (default: 5)
```

**Examples:**
- **Super strict** (only the best): `MIN_RATING = 4.5`, `MIN_REVIEWS = 100`
- **More lenient**: `MIN_RATING = 3.5`, `MIN_REVIEWS = 20`
- **Top 10 per city**: `MAX_RESULTS = 10`

### Change Number of Places Scraped

Edit the **"Start Apify Scraper"** node, in the JSON body:

```json
{
  "maxCrawledPlacesPerSearch": 50
}
```

- Higher number = more places to filter from (but slower)
- Lower number = faster but might miss some quality places

## 🧪 Testing

### Test with One City First

1. In your "Locations" sheet, add just one city:
   ```
   USA,California,Los Angeles,restaurant
   ```
2. In the workflow, click **"Execute Workflow"** (manual trigger)
3. Wait ~2-3 minutes
4. Check the "Results" sheet - you should see 5 top-rated restaurants from LA

### Check Workflow Execution

1. Go to n8n **"Executions"** tab
2. You'll see each run with:
   - ✅ Success (green)
   - ❌ Error (red)
3. Click on an execution to see detailed logs

## 📁 Files Created

```
iwilltravelto/
├── locations_input_template.csv          # CSV template for cities
├── quality_places_scraper_workflow.json  # n8n workflow (import this)
└── QUALITY_SCRAPER_GUIDE.md             # This documentation
```

## 🔧 Troubleshooting

### Problem: "No results returned"

**Solution:**
- Check if the city name is spelled correctly
- Try different category (e.g., use `restaurant` instead of `restaurants`)
- Lower the quality filters (MIN_RATING, MIN_REVIEWS)

### Problem: "Apify API error"

**Solution:**
- Verify your Apify token is correct
- Check Apify quota: https://console.apify.com/billing-new
- Make sure HTTP Header Auth credential is set up correctly

### Problem: "Google Sheets error"

**Solution:**
- Verify sheet names are exactly "Locations" and "Results"
- Check that Google Sheets credential has access to the spreadsheet
- Make sure the spreadsheet ID is correct

### Problem: "Less than 5 places returned"

**Solution:**
- The city might not have 5 quality places matching your filters
- Lower MIN_RATING or MIN_REVIEWS in the filter node
- Increase `maxCrawledPlacesPerSearch` to scrape more places

## 📊 Understanding the Results

Each row in "Results" sheet represents one city:

- **TotalFound**: Total places Apify found for this city
- **QualityPlaces**: How many passed your quality filters
- **Place1_Rating**: Star rating (4.0 - 5.0)
- **Place1_Reviews**: Number of reviews (minimum 50)
- **Place1_PriceLevel**: $ = Budget, $$ = Moderate, $$$ = Expensive, $$$$ = Very Expensive

**What if QualityPlaces < 5?**
- Some Place columns will be empty
- The city doesn't have 5 places meeting your quality criteria
- Consider lowering your filters for that category

## 🎯 Quality Criteria Explained

**Why these filters?**

1. **4.0+ stars**: Ensures places are well-rated (top 20% on Google)
2. **50+ reviews**: Proves it's popular and rating is reliable (not just 2-3 reviews)
3. **Active status**: Excludes closed businesses
4. **Sorted by rating then reviews**: Best-rated places first, if tied then most popular

**This ensures you only recommend places that:**
- Are actually good (high rating)
- Many people trust (lots of reviews)
- Are currently open
- Are proven favorites (combination of both)

## 🔄 Workflow Execution Flow

```
1. Trigger (Every 6 hours)
   ↓
2. Read "Locations" sheet
   ↓
3. Group unique city/category combinations
   ↓
4. Loop through each city one by one:
   ├─ Start Apify scraper for this city
   ├─ Wait 2 minutes for scraping to complete
   ├─ Fetch results from Apify
   ├─ Filter: Keep only 4.0+ rating, 50+ reviews, active
   ├─ Sort: By rating DESC, then reviews DESC
   ├─ Take top 5
   ├─ Save to "Results" sheet
   └─ Move to next city
   ↓
5. Complete (all cities processed)
```

## ⏱️ Performance

- **Per city processing**: ~2-3 minutes
- **10 cities**: ~20-30 minutes
- **100 cities**: ~3-5 hours

**Tip**: Start with a small list (5-10 cities) to test, then expand.

## 🆘 Support

If you encounter issues:

1. Check the n8n execution logs
2. Verify all credentials are set up correctly
3. Test with just one city first
4. Review the AGENTS.md file for additional guidelines

## 📝 CSV Template

Use this as a starting point:

```csv
Country,State,City,Category
USA,California,Los Angeles,restaurant
USA,California,Los Angeles,hotel
USA,California,San Francisco,restaurant
USA,New York,New York City,restaurant
France,Île-de-France,Paris,restaurant
UK,England,London,hotel
Spain,Catalonia,Barcelona,restaurant
Italy,Lazio,Rome,restaurant
```

Import this into your Google Sheet's "Locations" tab and customize!

---

**Last Updated**: January 15, 2026  
**Workflow Version**: 1.0  
**Apify Actor**: Google Maps Scraper (nwua9Gu5YrADL7ZDj)
