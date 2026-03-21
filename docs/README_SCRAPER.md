# Quality Places Scraper - Complete Package

## 📦 What You've Received

A complete, production-ready n8n workflow that automatically scrapes Google Places and returns **ONLY recommend-worthy locations** (4.0+ stars, 50+ reviews, active).

## 🎯 Key Features

✅ **Quality-First Filtering**: Only places worth recommending  
✅ **Hierarchical Processing**: Country → State → City  
✅ **Top 5 per City**: Best-ranked locations only  
✅ **Fully Automated**: Runs every 6 hours  
✅ **Comprehensive Data**: Name, rating, reviews, address, phone, website, GPS, images  
✅ **Google Sheets Integration**: Easy to view and export results  

## 📁 Files Included

| File | Purpose |
|------|---------|
| `quality_places_scraper_workflow.json` | **Import this to n8n** - Complete workflow |
| `locations_input_template.csv` | **CSV template** for your cities list |
| `QUICK_START.md` | **Start here** - 5-minute setup guide |
| `QUALITY_SCRAPER_GUIDE.md` | **Full documentation** - Everything explained |
| `WORKFLOW_SUMMARY.md` | **Technical overview** - Architecture & data flow |
| `TROUBLESHOOTING.md` | **Problem solving** - Common issues & fixes |
| `README_SCRAPER.md` | **This file** - Package overview |

## 🚀 Quick Start (3 Steps)

### 1️⃣ Prepare Google Sheets
- Open: https://docs.google.com/spreadsheets/d/1x38HGrufco-IF_w_GL7GqCFlabNMYfI9-uWAQ3ESOAk
- Create sheet: **"Locations"** (input)
- Create sheet: **"Results"** (output)
- Add cities to "Locations" (see template below)

### 2️⃣ Import Workflow
- Go to: https://n8n.iwilltravelto.com
- Import: `quality_places_scraper_workflow.json`
- Set up Apify credential (see QUICK_START.md)

### 3️⃣ Activate & Run
- Toggle "Active" to ON
- First run: Click "Execute Workflow"
- Automated: Runs every 6 hours

**Done!** Check "Results" sheet in ~3 minutes.

## 📊 Input Format (Locations Sheet)

```
Country         State                    City              Category
USA             California               Los Angeles       restaurant
USA             California               San Francisco     hotel
France          Île-de-France            Paris             restaurant
UK              England                  London            hotel
Spain           Catalonia                Barcelona         cafe
```

**Supported categories**: restaurant, hotel, cafe, bar, tourist_attraction, museum, spa, gym, etc.

## 📈 Output Format (Results Sheet)

Each row = 1 city with these columns:

**Summary Columns:**
- Country, State, City, Category
- TotalFound (all places Apify found)
- QualityPlaces (passed filters)
- LastScraped (date)

**5 Place Columns** (Place1 through Place5):
- Name, Rating, Reviews
- Address, Phone, Website
- Category, PriceLevel
- Image URL, Google Maps URL
- Latitude, Longitude

**Example Row:**
```
Country: USA
City: Los Angeles
Category: restaurant
TotalFound: 287
QualityPlaces: 58

Place1_Name: The French Laundry
Place1_Rating: 4.9
Place1_Reviews: 2,450
Place1_Address: 6640 Washington St, Yountville, CA
Place1_Phone: (707) 944-2380
Place1_Website: https://www.thomaskeller.com/tfl
...

Place2_Name: Providence
Place2_Rating: 4.8
...
```

## ⭐ Quality Criteria

**Only places that meet ALL criteria:**

| Filter | Value | Why |
|--------|-------|-----|
| **Min Rating** | 4.0+ stars | Top 20% on Google (excellent quality) |
| **Min Reviews** | 50+ reviews | Proven popular, reliable rating |
| **Status** | Active | Not closed (permanent or temporary) |
| **Ranking** | Rating → Reviews | Best quality first, if tied then most popular |

**Result**: Only recommend-worthy places people actually trust!

## 🎚️ Customization

### Change Quality Filters

Edit `Filter Top 5 Quality Places` node:

```javascript
const MIN_RATING = 4.0;      // Default: 4.0 (range: 1.0-5.0)
const MIN_REVIEWS = 50;      // Default: 50 (higher = more strict)
const MAX_RESULTS = 5;       // Default: 5 (how many per city)
```

**Examples:**
- **Super strict**: `MIN_RATING = 4.5`, `MIN_REVIEWS = 100`
- **More lenient**: `MIN_RATING = 3.5`, `MIN_REVIEWS = 20`
- **Top 10**: `MAX_RESULTS = 10`

### Change Schedule

Edit `Schedule Every 6 Hours` node:

```javascript
hoursInterval: 6    // Default: every 6 hours
// Other options:
// hoursInterval: 1     (every hour)
// hoursInterval: 12    (twice daily)
// daysInterval: 1      (daily)
```

## ⏱️ Performance

| Cities | Time | API Calls |
|--------|------|-----------|
| 1 city | ~2-3 min | 1 Apify run |
| 10 cities | ~25 min | 10 Apify runs |
| 50 cities | ~2 hours | 50 Apify runs |
| 100 cities | ~4 hours | 100 Apify runs |

**Tip**: Process in batches (10-20 cities at a time) for better control.

## 🔐 Required Credentials

### 1. Google Sheets (Already Set Up)
- ID: `QLIUHzCUR4PCeaCP`
- Type: OAuth2
- Status: ✅ Active

### 2. Apify API (Need to Set Up)
- Type: HTTP Header Auth
- Name: `Apify API`
- Header: `Authorization`
- Value: `Bearer YOUR_APIFY_API_TOKEN`

See `QUICK_START.md` for detailed credential setup.

## 🧪 Testing

### Test with 1 City First

1. Add to "Locations" sheet:
   ```
   USA,California,Los Angeles,restaurant
   ```
2. In n8n, click "Execute Workflow"
3. Wait 2-3 minutes
4. Check "Results" sheet
5. Verify 5 restaurants appear (or fewer if not enough quality places)

If successful, add more cities!

## 📚 Documentation Guide

**Read in this order:**

1. **QUICK_START.md** ← Start here (5 min setup)
2. **QUALITY_SCRAPER_GUIDE.md** ← Full documentation
3. **WORKFLOW_SUMMARY.md** ← Technical details
4. **TROUBLESHOOTING.md** ← If something goes wrong

## 🆘 Common Issues

### No results?
- Check city spelling
- Lower MIN_RATING to 3.5
- Lower MIN_REVIEWS to 20

### Less than 5 places?
- City doesn't have 5 quality places
- Normal behavior
- Consider lowering filters

### API errors?
- Check Apify token is correct
- Verify credential setup
- Check Apify quota: https://console.apify.com

**See TROUBLESHOOTING.md for complete solutions.**

## 🎓 Best Practices

1. ✅ **Start small**: Test with 5-10 cities
2. ✅ **Monitor executions**: Check n8n logs regularly
3. ✅ **Adjust filters**: Based on your needs
4. ✅ **Batch processing**: Don't add 1000 cities at once
5. ✅ **Update monthly**: Re-run for fresh data
6. ✅ **Spot check**: Verify results manually

## 📊 What Makes This Different?

**Other scrapers** return ALL places (including bad ones).

**This workflow** returns ONLY quality places because:
- ⭐ 4.0+ stars = Excellent quality
- 💬 50+ reviews = Proven popular
- ✅ Active = Currently operating
- 🏆 Ranked = Best first

**Result**: Every place is recommend-worthy!

## 🔄 Workflow Flow

```
INPUT (Google Sheets)
  ↓
Read cities list
  ↓
For each city:
  ├─ Scrape Google Places (Apify)
  ├─ Filter (4.0+ stars, 50+ reviews, active)
  ├─ Rank (rating DESC → reviews DESC)
  ├─ Take top 5
  └─ Save to Results sheet
  ↓
COMPLETE
```

## 📞 Categories Supported

Common categories:
- `restaurant` - Restaurants
- `hotel` - Hotels
- `cafe` - Cafes & Coffee Shops
- `bar` - Bars & Pubs
- `tourist_attraction` - Tourist Attractions
- `museum` - Museums
- `shopping_mall` - Shopping Malls
- `spa` - Spas & Wellness
- `gym` - Fitness Centers
- `nightclub` - Nightclubs

[Full list in Google Places API docs]

## 🎯 Use Cases

Perfect for:
- ✅ Travel guide websites
- ✅ City recommendation apps
- ✅ Tourism content creation
- ✅ Business directories
- ✅ Local SEO research
- ✅ Market analysis

## 🔗 Links & Resources

- **n8n Instance**: https://n8n.iwilltravelto.com
- **Google Sheet**: https://docs.google.com/spreadsheets/d/1x38HGrufco-IF_w_GL7GqCFlabNMYfI9-uWAQ3ESOAk
- **Apify Console**: https://console.apify.com
- **GitHub Repo**: https://github.com/salmenkhelifi1/iwilltravelto

## 📋 Checklist: Are You Ready?

Before activating:

- [ ] Google Sheet prepared (Locations + Results sheets)
- [ ] Cities added to Locations sheet
- [ ] Workflow imported to n8n
- [ ] Apify credential configured
- [ ] Google Sheets credential working
- [ ] Tested with 1 city successfully
- [ ] Workflow activated

**All checked?** You're ready to go! 🚀

## 🎉 What's Next?

1. **Add your cities** to the Locations sheet
2. **Activate workflow** in n8n
3. **Wait for results** (check Results sheet)
4. **Review & adjust** filters if needed
5. **Scale up** once confident

## 📝 Version Info

- **Version**: 1.0
- **Created**: January 15, 2026
- **Apify Actor**: Google Maps Scraper (nwua9Gu5YrADL7ZDj)
- **n8n Version**: Compatible with n8n v1.0+
- **Status**: Production-ready ✅

---

**Need help?** Check the documentation files or review n8n execution logs.

**Everything working?** Great! Enjoy your automated quality place scraper! 🎊
