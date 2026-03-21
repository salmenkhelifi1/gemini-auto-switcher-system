# Troubleshooting Checklist

## ✅ Pre-Flight Checklist

Before running the workflow, verify:

- [ ] Google Sheet `1x38HGrufco-IF_w_GL7GqCFlabNMYfI9-uWAQ3ESOAk` exists
- [ ] Sheet "Locations" exists with columns: Country | State | City | Category
- [ ] Sheet "Results" exists (can be empty)
- [ ] At least 1 city added to "Locations" sheet
- [ ] Apify API credential set up in n8n (HTTP Header Auth)
- [ ] Google Sheets credential working (QLIUHzCUR4PCeaCP)
- [ ] Workflow imported successfully
- [ ] Workflow activated (toggle ON)

## 🔍 Testing Steps

### Step 1: Test with One City
```
Action: Add one city to "Locations" sheet
Example: USA | California | Los Angeles | restaurant

Expected: 
- Workflow processes in ~2-3 minutes
- "Results" sheet gets 1 new row
- Row has 5 places (or fewer if not enough quality places)
```

### Step 2: Check n8n Execution
```
Action: Go to n8n → Executions tab

Expected:
- See green checkmark (success)
- No red X (error)
- All nodes executed successfully
```

### Step 3: Verify Results
```
Action: Check "Results" sheet

Expected:
- New row with your city
- TotalFound > 0
- QualityPlaces >= 0
- At least Place1_Name filled (if QualityPlaces > 0)
```

## 🐛 Common Errors & Fixes

### Error: "Failed to fetch from Google Sheets"

**Symptoms:**
- Workflow fails at "Read Locations Sheet" node
- Error message: "Insufficient permissions" or "Sheet not found"

**Solutions:**
1. Verify sheet name is exactly "Locations" (case-sensitive)
2. Check Google Sheets credential has access to the spreadsheet
3. Re-authenticate Google Sheets credential:
   - n8n → Credentials → Google Sheets account
   - Click "Reconnect"
   - Authorize again

---

### Error: "Apify API authentication failed"

**Symptoms:**
- Workflow fails at "Start Apify Scraper" node
- Error: "401 Unauthorized" or "Invalid token"

**Solutions:**
1. Verify Apify token is correct:
   ```
   YOUR_APIFY_API_TOKEN
   ```
2. Check HTTP Header Auth credential in n8n:
   - Credential name: "Apify API"
   - Header name: `Authorization`
   - Header value: `Bearer YOUR_APIFY_API_TOKEN`
3. Verify Apify account is active:
   - Login to https://console.apify.com
   - Check if token is still valid

---

### Error: "No results returned" or "QualityPlaces = 0"

**Symptoms:**
- Workflow completes successfully
- Results sheet shows TotalFound > 0 but QualityPlaces = 0
- All Place1-5 columns are empty

**Causes:**
- No places meet quality criteria (4.0+ stars, 50+ reviews)
- City name misspelled
- Category doesn't exist in that city

**Solutions:**
1. Lower quality filters in "Filter Top 5 Quality Places" node:
   ```javascript
   const MIN_RATING = 3.5;  // Lower from 4.0
   const MIN_REVIEWS = 20;  // Lower from 50
   ```
2. Verify city name spelling:
   - Use English names: "Paris" not "París"
   - Check state/region is correct
3. Try different category:
   - "restaurant" instead of "restaurants"
   - "cafe" instead of "coffee_shop"

---

### Error: "Apify timeout" or "Run took too long"

**Symptoms:**
- Workflow fails at "Get Apify Results" node
- Error: "Timeout" or "Dataset not ready"

**Causes:**
- Apify scraper took longer than 2 minutes
- Very popular city (thousands of places)

**Solutions:**
1. Increase wait time in "Wait 2 Minutes" node:
   - Change from 120 seconds to 180 seconds (3 minutes)
2. Reduce scraping scope in "Start Apify Scraper" node:
   ```json
   {
     "maxCrawledPlacesPerSearch": 30  // Lower from 50
   }
   ```

---

### Error: "Google Sheets write failed"

**Symptoms:**
- Workflow fails at "Save to Google Sheets" node
- Error: "Cannot write to sheet" or "Row not appended"

**Causes:**
- Sheet "Results" doesn't exist
- Sheet is protected/read-only
- Too many columns (Google Sheets limit)

**Solutions:**
1. Create "Results" sheet if missing
2. Remove sheet protection:
   - Google Sheets → Data → Remove protection
3. Check sheet has fewer than 18,278 columns (Google limit)

---

### Error: "Loop never completes"

**Symptoms:**
- Workflow runs forever
- Same city processed multiple times
- n8n shows "Running" for hours

**Causes:**
- Loop configuration error
- "Continue Loop" node not connected properly

**Solutions:**
1. Check workflow connections:
   - "Save to Google Sheets" → "Continue Loop" → "Loop Through Cities"
2. Verify "Loop Through Cities" node settings:
   - Batch size: 1
   - Options: Default
3. Manually stop execution and fix connections

---

### Error: "Too many requests" (429 error)

**Symptoms:**
- Workflow fails midway through processing
- Error: "429 Too Many Requests" from Apify

**Causes:**
- Hitting Apify rate limits
- Processing too many cities too fast

**Solutions:**
1. Add delay between cities:
   - Add "Wait" node after "Save to Google Sheets"
   - Set to 30-60 seconds
2. Process fewer cities at once:
   - Split your locations list into batches
   - Process 10-20 cities per run

---

## 🔧 Advanced Debugging

### Enable Detailed Logging

1. In n8n workflow settings:
   - Settings → Execution → Save execution progress: ON
2. Check execution details:
   - n8n → Executions → Click on execution
   - View each node's input/output

### Inspect Node Data

1. Run workflow manually (Execute Workflow button)
2. After completion, click on each node
3. Check "Output" tab to see data flowing through
4. Look for empty arrays or missing fields

### Test Individual Nodes

1. Disconnect node from workflow
2. Add "Manual Trigger" before it
3. Provide sample data using "Set" node
4. Execute just that node
5. Verify output is correct

---

## 📊 Data Quality Issues

### Issue: Some Place columns empty even though QualityPlaces > 0

**Example:**
- QualityPlaces = 3
- Place1, Place2, Place3 filled
- Place4, Place5 empty

**This is NORMAL**:
- Means only 3 quality places were found
- Not all cities have 5 quality places
- Not an error

**Actions:**
- No action needed (working as designed)
- Or lower quality filters to get more results

---

### Issue: Duplicate places across different cities

**Symptoms:**
- Same restaurant appears for multiple nearby cities

**Causes:**
- Google Places returns nearby results
- Chain restaurants with multiple locations

**This is EXPECTED**:
- Google Places behavior
- Proximity-based search

**Actions:**
- No action needed
- Or add deduplication logic in "Prepare Sheet Data" node

---

### Issue: Place rating doesn't match Google Maps

**Symptoms:**
- Rating in results differs from manual Google Maps check

**Causes:**
- Rating fluctuates over time
- Different data sources (Apify cache vs live Google)

**Actions:**
- Re-run workflow to get fresh data
- Or accept slight variations (normal)

---

## 🆘 Getting Help

If you've tried all troubleshooting steps:

1. **Check n8n execution log**:
   - Copy full error message
   - Note which node failed

2. **Verify workflow structure**:
   - Compare with original `quality_places_scraper_workflow.json`
   - Re-import if needed

3. **Test external services**:
   - Apify: https://console.apify.com (check quota/status)
   - Google Sheets: Manually open spreadsheet

4. **Review documentation**:
   - `QUALITY_SCRAPER_GUIDE.md` - Full setup guide
   - `QUICK_START.md` - Quick reference
   - `WORKFLOW_SUMMARY.md` - Architecture details

5. **Check logs**:
   - n8n execution logs
   - Apify actor run logs

---

## 🎯 Quick Diagnostic

Run this mental checklist:

```
Is workflow activated? → NO → Activate it
         ↓ YES
Can it read "Locations" sheet? → NO → Check sheet name/permissions
         ↓ YES
Can it call Apify? → NO → Check API token/credential
         ↓ YES
Does Apify return results? → NO → Check city name/category
         ↓ YES
Do any places pass filters? → NO → Lower MIN_RATING/MIN_REVIEWS
         ↓ YES
Can it write to "Results" sheet? → NO → Check sheet permissions
         ↓ YES
✅ WORKING!
```

---

## 📝 Logging Best Practices

For easier debugging:

1. **Keep execution history**:
   - n8n → Settings → Workflow → Save execution progress: ON
   - Keep last 100 executions

2. **Add manual checkpoints**:
   - Insert "NoOp" nodes between steps
   - Use descriptive node names

3. **Monitor regularly**:
   - Check n8n executions daily
   - Review "Results" sheet for completeness

---

**Last Updated**: January 15, 2026  
**Version**: 1.0
