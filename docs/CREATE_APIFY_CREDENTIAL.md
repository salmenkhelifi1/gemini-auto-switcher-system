# 🔐 CREATE APIFY CREDENTIAL - Step by Step Guide

## 📋 You Need This Information

**Credential Type:** Header Auth  
**Credential Name:** `Apify API`  
**Header Name:** `Authorization`  
**Header Value:** `Bearer YOUR_APIFY_API_TOKEN`

---

## 🚀 STEP-BY-STEP INSTRUCTIONS

### Step 1: Open n8n Credentials Page

1. Open your browser
2. Go to: **https://n8n.iwilltravelto.com**
3. Log in if needed
4. Click **"Credentials"** in the left sidebar (it has a key icon 🔑)

### Step 2: Create New Credential

1. Click the **"+ Add Credential"** button (top right)
2. In the search box, type: **"Header Auth"**
3. Click on **"Header Auth"** from the results

### Step 3: Fill in the Credential Details

You'll see a form. Fill it in EXACTLY as shown below:

```
┌─────────────────────────────────────────────────────────────┐
│ Credential Name                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Apify API                                               │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ Header Name                                                 │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Authorization                                           │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ Header Value                                                │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Bearer YOUR_APIFY_API_TOKEN  │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│            [Cancel]  [Save]                                 │
└─────────────────────────────────────────────────────────────┘
```

**IMPORTANT - Copy/Paste These Exact Values:**

**Field 1 - Credential Name:**
```
Apify API
```

**Field 2 - Header Name:**
```
Authorization
```

**Field 3 - Header Value:**
```
Bearer YOUR_APIFY_API_TOKEN
```

### Step 4: Save the Credential

1. Double-check all fields match exactly (especially the Bearer token)
2. Click **"Save"** button

You should see a success message: "Credential saved successfully"

---

## ✅ VERIFY IT WAS CREATED

After saving, you should see "Apify API" in your credentials list.

To verify:
1. Click on **"Credentials"** in the left sidebar
2. Look for **"Apify API"** in the list
3. It should show type: **"Header Auth"**

---

## 🔗 NEXT STEP: Assign to Workflow Nodes

After creating the credential, you need to assign it to the workflow:

### Assign to "Start Apify Scraper" Node

1. Go to: https://n8n.iwilltravelto.com/workflow/LLrnAOY5x1QuD3GD
2. Click on the **"Start Apify Scraper"** node (2nd node)
3. Scroll down to **"Credential to connect with"** section
4. Click the dropdown that says **"Select credential..."**
5. Select: **"Apify API"**
6. You should see it selected with a green checkmark ✅

### Assign to "Get Scraped Data" Node

1. Click on the **"Get Scraped Data"** node (4th node)
2. Scroll down to **"Credential to connect with"** section
3. Click the dropdown
4. Select: **"Apify API"**
5. You should see it selected with a green checkmark ✅

### Save the Workflow

1. Click **"Save"** button (top right corner)
2. You should see: "Workflow saved successfully"

---

## 🧪 TEST THE CREDENTIAL

Once saved and assigned, test it with this command:

```bash
curl -X POST "https://n8n.iwilltravelto.com/webhook/apify-scrape" \
  -H "Content-Type: application/json" \
  -d '{"searchQuery": "restaurants in Paris", "maxPlaces": 5}'
```

**Expected:**
- Wait 2-3 minutes
- Response: `{"success": true, "message": "Places scraped and saved successfully", ...}`
- Results saved to Google Sheets "ScrapedPlaces" tab

---

## 🚨 TROUBLESHOOTING

### Error: "Credentials not found"

**Fix:**
1. Make sure you spelled the name exactly: `Apify API` (with space)
2. Make sure credential type is **"Header Auth"** not something else

### Error: "Invalid token"

**Fix:**
1. Make sure Header Value starts with `Bearer ` (with a space after)
2. Copy/paste the token exactly as shown above
3. Full value should be: `Bearer YOUR_APIFY_API_TOKEN`

### Error: "Credential not assigned"

**Fix:**
1. Open the workflow
2. Click on "Start Apify Scraper" node
3. Make sure "Apify API" is selected in credentials dropdown
4. Do the same for "Get Scraped Data" node
5. Click Save

---

## 📋 QUICK CHECKLIST

- [ ] Opened n8n.iwilltravelto.com
- [ ] Clicked "Credentials" in sidebar
- [ ] Clicked "+ Add Credential"
- [ ] Selected "Header Auth"
- [ ] Filled in Credential Name: `Apify API`
- [ ] Filled in Header Name: `Authorization`
- [ ] Filled in Header Value: `Bearer YOUR_APIFY_API_TOKEN`
- [ ] Clicked "Save"
- [ ] Opened workflow: LLrnAOY5x1QuD3GD
- [ ] Assigned "Apify API" to "Start Apify Scraper" node
- [ ] Assigned "Apify API" to "Get Scraped Data" node
- [ ] Clicked "Save" on workflow
- [ ] Tested with curl command

---

## 🎯 SCREENSHOT GUIDE

If you need visual help, here's what each screen should look like:

**Screen 1 - Credentials Page:**
```
Credentials
  [+ Add Credential]
  
  Search credentials...
  
  📋 List of credentials:
  - Google Sheets account (OAuth2)
  - Apify API (Header Auth) ← You'll see this after creation
```

**Screen 2 - Create Credential Form:**
```
Header Auth

Credential Name
  [Apify API                                    ]

Header Name  
  [Authorization                                ]

Header Value
  [Bearer YOUR_APIFY_API_TOKEN... ]

                           [Cancel] [Save]
```

**Screen 3 - Workflow Node with Credential:**
```
Start Apify Scraper

Parameters
  ...

Credential to connect with
  [Apify API ✅                                 ▼]
```

---

## ✅ YOU'RE DONE!

Once you complete all checkboxes above, your workflow will be fully functional and ready to scrape places!

**Next:** Run the test command and check your Google Sheets! 🎉

---

**Token:** `YOUR_APIFY_API_TOKEN`  
**Full Bearer Value:** `Bearer YOUR_APIFY_API_TOKEN`
