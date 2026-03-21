# ✅ ACTIVATE SIMPLE APIFY SCRAPER - Step by Step

## 🎯 Quick Activation Guide

Since the n8n API has strict validation, I'll guide you through activating via the UI (easiest method).

## 📋 Steps to Activate

### Step 1: Import the Workflow

1. Open your browser and go to: **https://n8n.iwilltravelto.com**

2. Click **"+ Add workflow"** (top right corner)

3. Click **"Import from File"**

4. Select the file: **`simple_apify_scraper.json`**
   - Location: `/home/salmen/Documents/Developer/iwilltravelto/simple_apify_scraper.json`

5. Click **"Import"**

The workflow will be loaded with all nodes configured!

### Step 2: Set Up Apify Credential (If Needed)

If you haven't already set up the Apify API credential:

1. Click on **"Credentials"** in the left sidebar

2. Click **"+ Add Credential"**

3. Search for **"Header Auth"** and select it

4. Fill in:
   - **Credential Name**: `Apify API`
   - **Header Name**: `Authorization`
   - **Header Value**: `Bearer YOUR_APIFY_API_TOKEN`

5. Click **"Save"**

### Step 3: Verify Credentials in Workflow

1. Open the imported workflow

2. Click on **"Start Apify Scraper"** node

3. In the **Credentials** section, select: **Apify API**

4. Click on **"Get Scraped Data"** node

5. Verify **Apify API** credential is selected

6. Click **"Save"** (top right)

### Step 4: IMPORTANT - Activate the Workflow

**⚠️ CRITICAL STEP FOR WEBHOOK WORKFLOWS**

1. In the workflow editor, look for the toggle switch at the top right

2. Toggle **"Active"** from OFF to ON (it should turn green)

3. Click **"Save"**

4. You should see a message: **"Workflow activated"**

### Step 5: Get Your Webhook URL

1. Click on the **"Webhook Trigger"** node (first node)

2. Look for **"Webhook URLs"** section

3. You'll see a URL like:
   ```
   Production URL: https://n8n.iwilltravelto.com/webhook/apify-scrape
   ```

4. **Copy this URL** - you'll use it to trigger the workflow

## 🧪 Test the Workflow

### Option 1: Test from Terminal

```bash
curl -X POST "https://n8n.iwilltravelto.com/webhook/apify-scrape" \
  -H "Content-Type: application/json" \
  -d '{
    "searchQuery": "restaurants in Paris",
    "maxPlaces": 10
  }'
```

### Option 2: Test from n8n UI

1. In the workflow, click **"Execute Workflow"** (top right)

2. Wait 2-3 minutes (scraping takes time)

3. Check each node - green checkmarks = success

4. Check Google Sheets to verify data was saved

## 📊 Verify Results

### Check Google Sheets

1. Open: https://docs.google.com/spreadsheets/d/1x38HGrufco-IF_w_GL7GqCFlabNMYfI9-uWAQ3ESOAk

2. Look for the **"ScrapedPlaces"** sheet
   - If it doesn't exist, create it

3. After running the workflow, you should see new rows with:
   - name
   - address
   - rating
   - reviews
   - phone
   - website
   - category
   - priceLevel
   - latitude
   - longitude
   - googleMapsUrl
   - imageUrl
   - openingHours
   - isOpen
   - scrapedAt

## ✅ Activation Checklist

Mark these off as you complete them:

- [ ] Logged into n8n.iwilltravelto.com
- [ ] Imported `simple_apify_scraper.json`
- [ ] Apify API credential created/verified
- [ ] Google Sheets credential verified
- [ ] Workflow saved
- [ ] Workflow activated (toggle ON)
- [ ] Webhook URL copied
- [ ] Test request sent
- [ ] Google Sheets verified
- [ ] Results confirmed

## 🔧 If You Get Errors

### Error: "Credentials not found"

**Fix:**
1. Go to Credentials menu
2. Create "Header Auth" credential named "Apify API"
3. Re-open workflow and select the credential

### Error: "Sheet not found"

**Fix:**
1. Open Google Sheets
2. Create a new sheet named "ScrapedPlaces"
3. Re-run workflow

### Error: "Webhook not responding"

**Fix:**
1. Make sure workflow is **ACTIVE** (toggle ON)
2. Save the workflow
3. Try the webhook URL again

## 🚀 Quick Commands to Test

Once activated, use these commands:

```bash
# Test 1: Simple search
curl -X POST "https://n8n.iwilltravelto.com/webhook/apify-scrape" \
  -H "Content-Type: application/json" \
  -d '{"searchQuery": "restaurants in Paris", "maxPlaces": 10}'

# Test 2: Hotels
curl -X POST "https://n8n.iwilltravelto.com/webhook/apify-scrape" \
  -H "Content-Type: application/json" \
  -d '{"searchQuery": "hotels in London", "maxPlaces": 20}'

# Test 3: Cafes
curl -X POST "https://n8n.iwilltravelto.com/webhook/apify-scrape" \
  -H "Content-Type: application/json" \
  -d '{"searchQuery": "cafes in Barcelona", "maxPlaces": 15}'
```

## 📞 Expected Response

When successful, you'll get:

```json
{
  "success": true,
  "message": "Places scraped and saved successfully",
  "count": 10,
  "savedToSheets": true,
  "sheetUrl": "https://docs.google.com/spreadsheets/d/1x38HGrufco-IF_w_GL7GqCFlabNMYfI9-uWAQ3ESOAk"
}
```

## 🎉 You're Done!

Once activated:
- ✅ Workflow runs automatically when you send POST requests
- ✅ Results automatically save to Google Sheets
- ✅ No manual intervention needed
- ✅ Can trigger unlimited searches

---

**Next**: Check `SIMPLE_SCRAPER_GUIDE.md` for usage examples and customization options!
