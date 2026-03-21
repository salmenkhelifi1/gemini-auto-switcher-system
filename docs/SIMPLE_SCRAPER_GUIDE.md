# Simple Apify Places Scraper - Setup Guide

## 🎯 What This Does

A simple, webhook-triggered n8n workflow that:
- ✅ Scrapes Google Places using Apify
- ✅ Saves results to Google Sheets automatically
- ✅ Also provides CSV download option
- ✅ Triggered via HTTP POST request (no schedule needed)

## 📊 Data Saved

For each place, saves:
- **Basic**: Name, Address, Category
- **Ratings**: Rating (stars), Review Count
- **Contact**: Phone, Website
- **Location**: GPS (Latitude, Longitude), Google Maps URL
- **Visual**: Image URL
- **Details**: Price Level, Opening Hours, Is Open
- **Metadata**: Scraped At (timestamp)

## 🚀 Quick Setup

### Step 1: Prepare Google Sheets

1. Open your Google Sheet: https://docs.google.com/spreadsheets/d/1x38HGrufco-IF_w_GL7GqCFlabNMYfI9-uWAQ3ESOAk
2. Create a new sheet named: **"ScrapedPlaces"**
3. Add header row (optional, workflow auto-creates):
   ```
   name | address | rating | reviews | phone | website | category | priceLevel | latitude | longitude | googleMapsUrl | imageUrl | openingHours | isOpen | scrapedAt
   ```

### Step 2: Import Workflow to n8n

1. Go to: https://n8n.iwilltravelto.com
2. Click **"+ Add workflow"** → **"Import from File"**
3. Upload: `simple_apify_scraper.json`
4. Click **"Save"**

### Step 3: Set Up Apify Credential (If Not Already Done)

1. In n8n, go to **Credentials** → **"+ Add Credential"**
2. Choose **"Header Auth"**
3. Configure:
   - **Name**: `Apify API`
   - **Header Name**: `Authorization`
   - **Header Value**: `Bearer YOUR_APIFY_API_TOKEN`
4. Click **"Save"**

### Step 4: Activate the Workflow

**IMPORTANT**: This workflow uses a webhook, so you MUST activate it in the n8n UI first.

1. Open the workflow in n8n
2. Toggle **"Active"** to ON (top right)
3. Click **"Save"**
4. Copy the webhook URL (it will show in the webhook node)

The webhook URL will be:
```
https://n8n.iwilltravelto.com/webhook/apify-scrape
```

## 🎯 How to Use

### Method 1: Simple Search (Default)

Just trigger the webhook with a search query:

```bash
curl -X POST "https://n8n.iwilltravelto.com/webhook/apify-scrape" \
  -H "Content-Type: application/json" \
  -d '{
    "searchQuery": "restaurants in Paris"
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "Places scraped and saved successfully",
  "count": 20,
  "savedToSheets": true,
  "sheetUrl": "https://docs.google.com/spreadsheets/d/1x38HGrufco-IF_w_GL7GqCFlabNMYfI9-uWAQ3ESOAk"
}
```

### Method 2: Custom Parameters

Customize the scraping:

```bash
curl -X POST "https://n8n.iwilltravelto.com/webhook/apify-scrape" \
  -H "Content-Type: application/json" \
  -d '{
    "searchQuery": "hotels in London",
    "maxPlaces": 50,
    "language": "en"
  }'
```

**Parameters:**
- `searchQuery`: What to search for (required)
- `maxPlaces`: How many places to scrape (default: 20)
- `language`: Language code (default: "en")

### Method 3: From Browser

You can also use Postman or any HTTP client:

**URL**: `https://n8n.iwilltravelto.com/webhook/apify-scrape`  
**Method**: POST  
**Headers**: `Content-Type: application/json`  
**Body**:
```json
{
  "searchQuery": "cafes in Barcelona",
  "maxPlaces": 30
}
```

### Method 4: Multiple Searches

You can trigger multiple searches:

```bash
# Search 1: Restaurants in Paris
curl -X POST "https://n8n.iwilltravelto.com/webhook/apify-scrape" \
  -H "Content-Type: application/json" \
  -d '{"searchQuery": "restaurants in Paris", "maxPlaces": 20}'

# Search 2: Hotels in London  
curl -X POST "https://n8n.iwilltravelto.com/webhook/apify-scrape" \
  -H "Content-Type: application/json" \
  -d '{"searchQuery": "hotels in London", "maxPlaces": 30}'

# Search 3: Cafes in Rome
curl -X POST "https://n8n.iwilltravelto.com/webhook/apify-scrape" \
  -H "Content-Type: application/json" \
  -d '{"searchQuery": "cafes in Rome", "maxPlaces": 15}'
```

Each request will:
1. Scrape Google Places
2. Save all results to "ScrapedPlaces" sheet
3. Return success response

## 📊 Google Sheets Output

Results are automatically appended to the "ScrapedPlaces" sheet:

| name | address | rating | reviews | phone | website | category | priceLevel | latitude | longitude | googleMapsUrl | imageUrl | openingHours | isOpen | scrapedAt |
|------|---------|--------|---------|-------|---------|----------|------------|----------|-----------|---------------|----------|--------------|--------|-----------|
| Le Jules Verne | Eiffel Tower, Paris | 4.8 | 2450 | +33... | https://... | Restaurant | $$$ | 48.858 | 2.294 | https://maps... | https://... | Mon-Sun 12-11pm | true | 2026-01-15T... |
| La Tour d'Argent | 15 Quai de..., Paris | 4.7 | 1890 | +33... | https://... | French Restaurant | $$$$ | 48.852 | 2.354 | https://maps... | https://... | Tue-Sat 7-10pm | true | 2026-01-15T... |

## 📥 CSV Download Option

The workflow also creates a CSV file with all results. To get it:

1. The webhook responds with JSON by default (Google Sheets path)
2. CSV is generated in parallel but not sent by default
3. To download CSV, you'd need to modify the workflow slightly (see Advanced Usage)

**Current behavior:**
- ✅ Saves to Google Sheets (always)
- ✅ Creates CSV file (in background)
- ✅ Returns JSON response with sheet URL

## ⏱️ Processing Time

- **Small search** (10-20 places): ~2-3 minutes
- **Medium search** (30-50 places): ~3-4 minutes
- **Large search** (100+ places): ~5-6 minutes

**Note**: Workflow waits 2 minutes for Apify to complete scraping, then fetches results.

## 🧪 Testing

### Test 1: Simple Search

```bash
curl -X POST "https://n8n.iwilltravelto.com/webhook/apify-scrape" \
  -H "Content-Type: application/json" \
  -d '{"searchQuery": "restaurants in Los Angeles", "maxPlaces": 10}'
```

**Expected:**
- Response: Success message with count
- Google Sheets: 10 new rows added to "ScrapedPlaces"

### Test 2: Check Google Sheets

1. Open: https://docs.google.com/spreadsheets/d/1x38HGrufco-IF_w_GL7GqCFlabNMYfI9-uWAQ3ESOAk
2. Go to "ScrapedPlaces" sheet
3. Verify new rows appeared with restaurant data

## 🔧 Customization

### Change Wait Time

If scraping takes longer than 2 minutes:

1. Open workflow in n8n
2. Click on "Wait for Scraping" node
3. Change `amount` from 120 to 180 (3 minutes) or 240 (4 minutes)
4. Save

### Change Default Max Places

Edit "Start Apify Scraper" node:

```javascript
"maxCrawledPlacesPerSearch": parseInt($json.query.maxPlaces) || 50  // Change 20 to 50
```

### Add Filters

To filter results before saving, add a node between "Format Place Data" and "Save to Google Sheets":

1. Add **"Code"** node
2. Add filtering logic:
```javascript
const place = $input.first().json;

// Only keep places with 4.0+ rating and 50+ reviews
if (place.rating >= 4.0 && place.reviews >= 50) {
  return [$input.first()];
} else {
  return [];
}
```

## 🔐 Required Credentials

### 1. Apify API (HTTP Header Auth)
- **Name**: `Apify API`
- **Header**: `Authorization`
- **Value**: `Bearer YOUR_APIFY_API_TOKEN`
- **Status**: ⚠️ Need to set up

### 2. Google Sheets OAuth2
- **ID**: `QLIUHzCUR4PCeaCP`
- **Status**: ✅ Already configured

## 🚨 Troubleshooting

### Error: "Webhook not found"

**Solution**: Activate the workflow in n8n UI (toggle "Active" to ON)

### Error: "Apify API authentication failed"

**Solution**: 
1. Verify Apify credential is set up correctly
2. Check token: `YOUR_APIFY_API_TOKEN`

### Error: "Google Sheets not found"

**Solution**:
1. Create "ScrapedPlaces" sheet in your Google Sheet
2. Verify sheet name is exactly "ScrapedPlaces" (case-sensitive)

### Error: "No results returned"

**Solution**:
1. Check search query is valid ("restaurants in Paris")
2. Increase wait time from 2 to 3 minutes
3. Check Apify quota: https://console.apify.com

### Results look incomplete

**Solution**:
1. Increase `maxPlaces` parameter (default 20)
2. Some places might not have all fields (normal)

## 📋 Example Search Queries

```bash
# Restaurants
"restaurants in Paris"
"best restaurants in Tokyo"
"italian restaurants in New York"

# Hotels
"hotels in London"
"5 star hotels in Dubai"
"budget hotels in Bangkok"

# Cafes
"cafes in Barcelona"
"coffee shops in Seattle"
"best cafes in Melbourne"

# Tourist Attractions
"tourist attractions in Rome"
"museums in Amsterdam"
"parks in Central Park, New York"

# Specific Searches
"sushi restaurants in Los Angeles"
"rooftop bars in Singapore"
"spa and wellness centers in Bali"
```

## 🎯 Use Cases

Perfect for:
- ✅ Quick data collection
- ✅ Market research
- ✅ Competitor analysis
- ✅ Building business directories
- ✅ Travel content creation
- ✅ SEO research

## 📊 Data Quality

**What you get:**
- All places matching your search query
- Complete data (when available from Google)
- Real-time scraping (fresh data)
- Includes closed/inactive places (can filter if needed)

**Note**: Unlike the "Quality Scraper", this workflow saves ALL results without filtering by rating/reviews.

## 🔄 Workflow Flow

```
1. Receive webhook request
   ↓
2. Extract search parameters
   ↓
3. Call Apify to start scraping
   ↓
4. Wait 2 minutes
   ↓
5. Fetch scraped results from Apify
   ↓
6. Split results into individual places
   ↓
7. Format each place data
   ↓
8. Save to Google Sheets (parallel)
9. Create CSV file (parallel)
   ↓
10. Return success response
```

## 📁 Files

- `simple_apify_scraper.json` - Import this to n8n
- `SIMPLE_SCRAPER_GUIDE.md` - This documentation

## 🔗 Links

- **n8n Instance**: https://n8n.iwilltravelto.com
- **Google Sheet**: https://docs.google.com/spreadsheets/d/1x38HGrufco-IF_w_GL7GqCFlabNMYfI9-uWAQ3ESOAk
- **Apify Console**: https://console.apify.com

## ✅ Setup Checklist

- [ ] Google Sheet opened
- [ ] Sheet "ScrapedPlaces" created
- [ ] Workflow imported to n8n
- [ ] Apify credential configured
- [ ] Workflow activated (toggle ON)
- [ ] Webhook URL copied
- [ ] Test request sent
- [ ] Results verified in Google Sheets

## 🎉 You're Ready!

Once activated, just send POST requests to trigger scraping. Results automatically save to Google Sheets!

**Example final test:**

```bash
curl -X POST "https://n8n.iwilltravelto.com/webhook/apify-scrape" \
  -H "Content-Type: application/json" \
  -d '{"searchQuery": "restaurants in Paris", "maxPlaces": 20}'
```

Then check your Google Sheets "ScrapedPlaces" tab! 🎊

---

**Version**: 1.0  
**Created**: January 15, 2026  
**Apify Actor**: Google Maps Scraper (nwua9Gu5YrADL7ZDj)
