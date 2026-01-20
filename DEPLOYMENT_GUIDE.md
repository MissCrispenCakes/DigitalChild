# Website Deployment Guide

Complete guide for deploying GRIMdata.org with GitHub Actions.

## ✅ What's Been Set Up

### 1. MkDocs Installation

**Installed packages:**

- `mkdocs==1.6.1` - Static site generator
- `mkdocs-material==9.7.1` - Material Design theme
- `pymdown-extensions==10.20` - Additional markdown features

**Files created:**

- `requirements-docs.txt` - Documentation dependencies
- `.gitignore` - Excludes `site/` build directory

### 2. GitHub Actions Workflow

**File:** `.github/workflows/deploy-docs.yml`

**Triggers:**

- Automatic deployment on push to `basecamp` branch
- Only when `docs/` or `mkdocs.yml` changes
- Manual trigger available (workflow_dispatch)

**What it does:**

1. Checks out repository
1. Sets up Python 3.12
1. Installs MkDocs and dependencies
1. Builds documentation
1. Deploys to `gh-pages` branch automatically

**Permissions:** Has `contents: write` to push to gh-pages branch

### 3. Multi-Project Structure

**Projects:**

1. **LittleRainbowRights** - `docs/projects/littlerainbowrights/index.md`

   - Child and LGBTQ+ digital rights research
   - Scorecard with 10 indicators across 194 countries
   - Comprehensive project page with all features

1. **SGBV-UPR** - `docs/projects/sgbv/index.md`

   - Sexual and gender-based violence analysis
   - Uses UPR recommendations
   - Published research project

**URL Structure:**

```
grimdata.org                                    → Homepage
grimdata.org/projects/littlerainbowrights/      → LRR Project
grimdata.org/projects/sgbv/                     → SGBV Project
grimdata.org/scorecard/                         → Scorecard data
grimdata.org/getting-started/installation/      → Installation guide
```

### 4. Custom Domain Configuration

**File:** `docs/CNAME`

**Content:** `grimdata.org`

**Secondary domains:**

- `littlerainbowrights.com` → Can redirect to `grimdata.org/projects/littlerainbowrights/`
- Your SGBV domain → Can redirect to `grimdata.org/projects/sgbv/`

## 🚀 Deployment Steps

### Step 1: Enable GitHub Pages

1. Go to GitHub repository settings
1. Navigate to **Settings → Pages**
1. **Source:** Deploy from a branch
1. **Branch:** `gh-pages` (will be created automatically)
1. **Folder:** `/ (root)`
1. Click **Save**

### Step 2: Trigger First Deployment

**Option A: Automatic (Recommended)**

Push any change to docs:

```bash
# Make a small change
echo "Test deployment" >> docs/index.md
git add docs/index.md
git commit -m "Trigger deployment"
git push origin basecamp
```

The GitHub Action will run automatically and deploy within 2-3 minutes.

**Option B: Manual Trigger**

1. Go to **Actions** tab on GitHub
1. Click **Deploy Documentation** workflow
1. Click **Run workflow**
1. Select `basecamp` branch
1. Click **Run workflow**

### Step 3: Verify Deployment

After 2-3 minutes:

1. Go to **Actions** tab
1. Check the workflow run completed successfully (green checkmark)
1. Visit: `https://misscrispcakes.github.io/DigitalChild/`
1. Verify site loads correctly

### Step 4: Configure Custom Domain (grimdata.org)

#### At Your Domain Registrar (e.g., Namecheap, GoDaddy)

Add these DNS records:

**A Records (for grimdata.org):**

```
Type: A
Name: @
Value: 185.199.108.153

Type: A
Name: @
Value: 185.199.109.153

Type: A
Name: @
Value: 185.199.110.153

Type: A
Name: @
Value: 185.199.111.153
```

**CNAME Record (for www):**

```
Type: CNAME
Name: www
Value: misscrispcakes.github.io
```

#### DNS Propagation

- DNS changes take 24-48 hours to propagate globally
- Use [whatsmydns.net](https://www.whatsmydns.net/) to check propagation status

#### Enable HTTPS

After DNS propagates:

1. Go to **Settings → Pages** on GitHub
1. Check **Enforce HTTPS** (checkbox will be grayed out until DNS propagates)
1. Wait a few minutes for SSL certificate to provision

### Step 5: Configure Secondary Domain (littlerainbowrights.com)

**Option A: Redirect at Domain Registrar**

Most registrars offer URL forwarding:

1. Go to your domain registrar settings
1. Find "URL Forwarding" or "Domain Forwarding"
1. Forward `littlerainbowrights.com` to `https://grimdata.org/projects/littlerainbowrights/`
1. Enable **301 redirect** (permanent)
1. Optional: Enable forwarding with path (maintains subdirectories)

**Option B: DNS with Subdomain**

If you want `littlerainbowrights.com` to show GRIMdata content:

```
Type: CNAME
Name: @
Value: misscrispcakes.github.io
```

Then visitors will see grimdata.org content at littlerainbowrights.com (but GitHub Pages only supports one custom domain per repo)

**Recommendation:** Use Option A (redirect) since you want grimdata.org as the primary domain.

## 🔧 Testing Locally

Before deploying, test locally:

```bash
# Activate virtual environment
source .LittleRainbow/bin/activate

# Serve locally (with live reload)
mkdocs serve

# Open browser to http://127.0.0.1:8000/
```

Navigate the site, check all links work, and verify formatting.

## 📝 Making Updates

### Update Content

1. Edit markdown files in `docs/`
1. Commit and push to `basecamp`
1. GitHub Actions deploys automatically

```bash
# Example: Update FAQ
nano docs/FAQ.md

git add docs/FAQ.md
git commit -m "Update FAQ"
git push origin basecamp

# Wait 2-3 minutes for deployment
```

### Update Navigation

Edit `mkdocs.yml`:

```yaml
nav:
  - Home: index.md
  - Projects:
      - LittleRainbowRights: projects/littlerainbowrights/index.md
      - SGBV-UPR: projects/sgbv/index.md
  # Add more sections here
```

### Update Theme or Styling

- **CSS:** Edit `docs/stylesheets/extra.css`
- **JavaScript:** Edit `docs/javascripts/extra.js`
- **Theme settings:** Edit `mkdocs.yml` under `theme:` section

## 🎨 Customization

### Add Logo and Favicon

1. Create `docs/assets/` directory

1. Add images:

   - `docs/assets/logo.png` (for header, ~200x50px recommended)
   - `docs/assets/favicon.ico` (for browser tab, 32x32px)

1. Update `mkdocs.yml`:

   ```yaml
   theme:
     logo: assets/logo.png
     favicon: assets/favicon.ico
   ```

### Add Google Analytics (Optional)

1. Get Google Analytics ID (format: `G-XXXXXXXXXX`)
1. Update `mkdocs.yml`:
   ```yaml
   extra:
     analytics:
       provider: google
       property: G-XXXXXXXXXX  # Your actual ID
   ```

## 🔍 Monitoring Deployment

### Check GitHub Actions

1. Go to **Actions** tab
1. View workflow runs
1. Click on a run to see detailed logs
1. Green checkmark = success
1. Red X = failure (click to see error logs)

### Common Issues

**Issue: Workflow doesn't trigger**

- Check `.github/workflows/deploy-docs.yml` exists
- Verify you pushed to `basecamp` branch
- Check if paths filter matches your changes

**Issue: Build fails**

- Check Actions logs for error messages
- Common: Missing file references in `mkdocs.yml`
- Test locally first: `mkdocs build`

**Issue: Site deployed but shows 404**

- Verify `gh-pages` branch exists
- Check GitHub Pages settings pointing to correct branch
- Wait a few minutes after first deployment

**Issue: Custom domain not working**

- Verify DNS records are correct
- Check DNS propagation: [whatsmydns.net](https://www.whatsmydns.net/)
- Ensure `docs/CNAME` contains correct domain
- Wait 24-48 hours for DNS to propagate

## 📊 Site Structure Overview

```
grimdata.org/
├── (homepage)
├── projects/
│   ├── littlerainbowrights/  ← littlerainbowrights.com redirects here
│   └── sgbv/                  ← Your SGBV domain redirects here
├── getting-started/
│   ├── installation/
│   └── quickstart/
├── guides/
│   ├── RUNBOOK/
│   ├── SCORECARD_WORKFLOW/
│   └── VALIDATORS_USAGE/
├── scorecard/
│   ├── (visualization)
│   └── explorer/
├── standards/
├── notes/
├── planning/
└── reviews/
```

## 🔐 Security Notes

- GitHub Actions runs in secure environment
- No credentials needed (uses GitHub's built-in authentication)
- `GITHUB_TOKEN` automatically provided by GitHub
- Site is static (no backend vulnerabilities)
- HTTPS enforced after SSL certificate provisioned

## 📞 Support

**Issues with deployment?**

1. Check [GitHub Actions logs](https://github.com/MissCrispenCakes/DigitalChild/actions)
1. Test locally: `mkdocs serve`
1. Review [MkDocs documentation](https://www.mkdocs.org/)
1. Review [Material theme docs](https://squidfunk.github.io/mkdocs-material/)

**DNS/Domain issues?**

1. Check DNS propagation: [whatsmydns.net](https://www.whatsmydns.net/)
1. Verify records with domain registrar
1. Contact registrar support if needed

## ✅ Checklist

Before going live:

- [ ] GitHub Actions workflow runs successfully
- [ ] Site deployed to gh-pages branch
- [ ] Site accessible at `misscrispcakes.github.io/DigitalChild`
- [ ] DNS records configured at domain registrar
- [ ] DNS propagated (check with whatsmydns.net)
- [ ] Custom domain working (grimdata.org)
- [ ] HTTPS enabled in GitHub Pages settings
- [ ] Secondary domain redirecting (littlerainbowrights.com)
- [ ] All links working (test navigation)
- [ ] TODOs completed (security email in SECURITY.md, author info in CITATION.cff)
- [ ] Logo and favicon added (optional but recommended)

## 🎉 Next Steps After Launch

1. **Announce** - Share grimdata.org on social media, academic networks
1. **Monitor** - Watch GitHub Actions for deployment status
1. **Iterate** - Add content, update scorecard, improve visualizations
1. **Analytics** - Add Google Analytics to track visitors (optional)
1. **Feedback** - Gather user feedback via GitHub Issues/Discussions

______________________________________________________________________

**Last updated:** January 2026

**Status:** Ready for deployment! 🚀
