# Quality Places Scraper - Workflow Summary

## 📋 Executive Summary

**Purpose**: Automatically scrape and filter Google Places to find the TOP 5 quality locations per city.

**Quality Criteria**:
- ⭐ Rating: 4.0+ stars
- 💬 Reviews: 50+ reviews minimum
- ✅ Status: Active (not closed)
- 🏆 Ranking: By rating DESC, then review count DESC

**Input**: Google Sheet with Country/State/City/Category  
**Output**: Google Sheet with TOP 5 places per city (name, rating, reviews, address, phone, website, etc.)

## 🔄 Workflow Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    AUTOMATED WORKFLOW                            │
│                  (Runs Every 6 Hours)                            │
└─────────────────────────────────────────────────────────────────┘

    ┌──────────────────┐
    │  1. TRIGGER      │
    │  Schedule        │
    │  Every 6 Hours   │
    └────────┬─────────┘
             │
             ▼
    ┌──────────────────┐
    │  2. READ INPUT   │
    │  Google Sheets   │
    │  "Locations"     │
    └────────┬─────────┘
             │
             ▼
    ┌──────────────────┐
    │  3. GROUP DATA   │
    │  Unique Cities   │
    │  + Categories    │
    └────────┬─────────┘
             │
             ▼
    ┌──────────────────────────────────────────────┐
    │  4. LOOP: For Each City                      │
    │  ┌────────────────────────────────────────┐  │
    │  │  a. Start Apify Scraper                │  │
    │  │     (Search: "restaurant in Paris")    │  │
    │  └─────────────┬──────────────────────────┘  │
    │                ▼                              │
    │  ┌────────────────────────────────────────┐  │
    │  │  b. Wait 2 Minutes                     │  │
    │  │     (Let Apify complete scraping)      │  │
    │  └─────────────┬──────────────────────────┘  │
    │                ▼                              │
    │  ┌────────────────────────────────────────┐  │
    │  │  c. Get Apify Results                  │  │
    │  │     (Fetch scraped places)             │  │
    │  └─────────────┬──────────────────────────┘  │
    │                ▼                              │
    │  ┌────────────────────────────────────────┐  │
    │  │  d. FILTER QUALITY PLACES              │  │
    │  │     • 4.0+ stars ⭐                    │  │
    │  │     • 50+ reviews 💬                   │  │
    │  │     • Active (not closed) ✅           │  │
    │  └─────────────┬──────────────────────────┘  │
    │                ▼                              │
    │  ┌────────────────────────────────────────┐  │
    │  │  e. RANK & SELECT TOP 5                │  │
    │  │     Sort by: Rating → Reviews          │  │
    │  │     Take: Top 5 results                │  │
    │  └─────────────┬──────────────────────────┘  │
    │                ▼                              │
    │  ┌────────────────────────────────────────┐  │
    │  │  f. Prepare Data for Sheet             │  │
    │  │     (Format: 1 row per city,           │  │
    │  │      5 place columns)                  │  │
    │  └─────────────┬──────────────────────────┘  │
    │                ▼                              │
    │  ┌────────────────────────────────────────┐  │
    │  │  g. Save to Google Sheets              │  │
    │  │     Sheet: "Results"                   │  │
    │  └─────────────┬──────────────────────────┘  │
    │                │                              │
    │                └──────┐ Next City             │
    └───────────────────────┼───────────────────────┘
                            │
                            ▼
                    ┌──────────────┐
                    │   COMPLETE   │
                    │ All Cities   │
                    │  Processed   │
                    └──────────────┘
```

## 📊 Data Flow

### INPUT (Google Sheets "Locations")
```
┌─────────┬────────────┬───────────────┬────────────┐
│ Country │ State      │ City          │ Category   │
├─────────┼────────────┼───────────────┼────────────┤
│ USA     │ California │ Los Angeles   │ restaurant │
│ USA     │ California │ San Francisco │ hotel      │
│ France  │ Île-de-F.  │ Paris         │ restaurant │
└─────────┴────────────┴───────────────┴────────────┘
```

### PROCESSING
```
For "restaurant in Los Angeles":
  
  Apify finds: 150 restaurants
       ↓
  Filter (4.0+ stars, 50+ reviews, active): 42 restaurants
       ↓
  Sort by rating DESC, then reviews DESC
       ↓
  Take top 5:
    1. The French Laundry (4.9★, 2,450 reviews)
    2. Providence (4.8★, 1,890 reviews)
    3. Bestia (4.7★, 3,200 reviews)
    4. Republique (4.6★, 5,100 reviews)
    5. Guelaguetza (4.6★, 2,800 reviews)
```

### OUTPUT (Google Sheets "Results")
```
┌─────────┬───────┬──────┬──────────┬────────────┬────────────┬───────────┬──────────┐
│ Country │ State │ City │ Category │ TotalFound │ Quality... │ Place1... │ Place2...│
├─────────┼───────┼──────┼──────────┼────────────┼────────────┼───────────┼──────────┤
│ USA     │ CA    │ LA   │ rest...  │ 150        │ 42         │ French... │ Provid...│
└─────────┴───────┴──────┴──────────┴────────────┴────────────┴───────────┴──────────┘

Each row has 5 places with these fields (×5):
  • Place_Name
  • Place_Rating
  • Place_Reviews
  • Place_Address
  • Place_Phone
  • Place_Website
  • Place_Category
  • Place_PriceLevel
  • Place_Image
  • Place_GoogleMapsURL
  • Place_Latitude
  • Place_Longitude
```

## 🎯 Key Features

### 1. Quality Assurance
- **No low-rated places**: 4.0+ stars only
- **No unproven places**: 50+ reviews minimum
- **No closed businesses**: Active status check
- **Best-ranked first**: Rating + popularity sorting

### 2. Hierarchical Processing
- Processes one city at a time
- Order: Country 1 → State 1 → All cities in State 1 → State 2 → Country 2
- No parallel processing (avoids API rate limits)

### 3. Comprehensive Data
Each place includes:
- Basic: Name, Rating, Reviews, Category
- Contact: Address, Phone, Website
- Visual: Image URL
- Navigation: Google Maps URL, GPS coordinates
- Pricing: Price level indicator

### 4. Automation
- Runs every 6 hours automatically
- No manual intervention needed
- Processes entire list sequentially
- Results saved to Google Sheets

## ⚙️ Configuration

### Quality Thresholds (Adjustable)
```javascript
MIN_RATING = 4.0      // 1.0 - 5.0
MIN_REVIEWS = 50      // Any positive integer
MAX_RESULTS = 5       // How many places per city
```

### Scraping Settings
```json
{
  "maxCrawledPlacesPerSearch": 50,  // More = better filtering, slower
  "maxReviews": 10,                 // Reviews to fetch per place
  "maxImages": 3                    // Images to fetch per place
}
```

### Schedule
```javascript
hoursInterval: 6  // Run every 6 hours
// Alternatives:
// - Every hour: hoursInterval: 1
// - Every 12 hours: hoursInterval: 12
// - Daily: Change to daysInterval: 1
```

## 📈 Performance Metrics

### Processing Time
- **Per city**: 2-3 minutes (scraping + filtering)
- **10 cities**: ~25 minutes
- **50 cities**: ~2 hours
- **100 cities**: ~4 hours

### API Usage (Apify)
- **Per city**: 1 actor run
- **Cost**: Depends on Apify plan
- **Rate limit**: Respects Apify limits (2-minute wait between requests)

### Data Quality
- **Before filtering**: 20-150 places per search
- **After filtering**: 5-50 quality places
- **Final output**: Top 5 per city
- **Average quality retention**: 30-40% of places pass filters

## 🔐 Security & Credentials

### Required Credentials
1. **Google Sheets OAuth2** (ID: `QLIUHzCUR4PCeaCP`)
   - Scope: Read/Write spreadsheets
   - Already configured

2. **Apify API Token** (Bearer auth)
   - Token: `YOUR_APIFY_API_TOKEN`
   - Set up as HTTP Header Auth in n8n

### Google Sheet Access
- Sheet ID: `1x38HGrufco-IF_w_GL7GqCFlabNMYfI9-uWAQ3ESOAk`
- Required sheets: "Locations" (input), "Results" (output)

## 🚨 Error Handling

### Common Issues & Solutions

1. **No results for a city**
   - City name might be misspelled
   - Category might not exist in that city
   - Filters too strict (lower MIN_RATING/MIN_REVIEWS)

2. **Less than 5 places returned**
   - Not enough quality places exist
   - Normal behavior - not an error
   - Consider lowering quality filters

3. **Apify timeout**
   - City has too many places (very common location)
   - Increase wait time from 2 to 3 minutes
   - Or reduce `maxCrawledPlacesPerSearch`

4. **Google Sheets quota exceeded**
   - Processing too many cities too fast
   - Add delay between cities (Wait node)
   - Or reduce batch size

## 📊 Example Results

### Sample Output for "restaurant in Paris, France"

```
TotalFound: 287 places
QualityPlaces: 58 places (passed filters)

Top 5:
1. ⭐ 4.9 | 💬 3,245 | Le Jules Verne
2. ⭐ 4.8 | 💬 2,890 | L'Atelier de Joël Robuchon
3. ⭐ 4.8 | 💬 2,103 | Septime
4. ⭐ 4.7 | 💬 4,567 | Breizh Café
5. ⭐ 4.7 | 💬 3,890 | L'Ami Jean
```

### Why These Filters Work

**4.0+ stars:**
- Google average is ~3.5 stars
- 4.0+ = Top 30% of all places
- Indicates consistent quality

**50+ reviews:**
- Eliminates new/unproven places
- Ensures rating reliability
- Proves sustained popularity

**Active status:**
- Avoids recommending closed businesses
- Ensures current data

**Ranking by rating then reviews:**
- Best quality first (rating)
- If tied, most popular (reviews)
- Balanced approach

## 🎓 Best Practices

1. **Start small**: Test with 5-10 cities first
2. **Monitor**: Check n8n execution logs
3. **Adjust filters**: Based on your needs (more/less strict)
4. **Batch processing**: Don't add 1000 cities at once
5. **Regular updates**: Re-run monthly to get fresh data
6. **Verify results**: Spot-check a few cities manually

## 📞 Support Resources

- **Full guide**: `QUALITY_SCRAPER_GUIDE.md`
- **Quick start**: `QUICK_START.md`
- **CSV template**: `locations_input_template.csv`
- **Workflow JSON**: `quality_places_scraper_workflow.json`
- **Agent guidelines**: `AGENTS.md`

---

**Workflow Version**: 1.0  
**Created**: January 15, 2026  
**Apify Actor**: Google Maps Scraper (nwua9Gu5YrADL7ZDj)  
**n8n Instance**: https://n8n.iwilltravelto.com
