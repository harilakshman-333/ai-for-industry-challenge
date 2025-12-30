# GitHub Pages Setup Instructions

Follow these steps to publish your project documentation to GitHub Pages.

## Step 1: Create GitHub Repository

1. Go to [GitHub](https://github.com) and log in
2. Click the "+" icon in the top right and select "New repository"
3. Name your repository: `ai-for-industry-challenge`
4. Set visibility to **Public** (required for free GitHub Pages)
5. Do NOT initialize with README (we already have one)
6. Click "Create repository"

## Step 2: Push Your Code to GitHub

```bash
cd /home/kwalker96/.gemini/antigravity/scratch/ai-for-industry-challenge

# Add remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/ai-for-industry-challenge.git

# Rename branch to main (GitHub's default)
git branch -M main

# Push to GitHub
git push -u origin main
```

## Step 3: Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** (top right)
3. Scroll down to **Pages** in the left sidebar
4. Under "Source", select:
   - **Branch:** `main`
   - **Folder:** `/docs`
5. Click **Save**

## Step 4: Wait for Deployment

- GitHub will build and deploy your site (takes 1-2 minutes)
- Your site will be available at: `https://YOUR_USERNAME.github.io/ai-for-industry-challenge/`
- You'll see a green checkmark when deployment is complete

## Step 5: Update Repository Settings

In `docs/_config.yml`, update the repository field:

```yaml
repository: YOUR_USERNAME/ai-for-industry-challenge
```

Then commit and push:

```bash
git add docs/_config.yml
git commit -m "Update repository config for GitHub Pages"
git push
```

## Step 6: Verify Your Site

Visit `https://YOUR_USERNAME.github.io/ai-for-industry-challenge/` to see your documentation!

## Customization Options

### Change Theme

Edit `docs/_config.yml` and change the theme:

```yaml
theme: jekyll-theme-minimal
# Other options: jekyll-theme-slate, jekyll-theme-architect, etc.
```

### Add Custom Domain (Optional)

1. Buy a domain name
2. In repository Settings → Pages → Custom domain
3. Enter your domain and save
4. Configure DNS with your domain provider

### Update Navigation

Edit `docs/_config.yml` to modify the navigation menu:

```yaml
navigation:
  - title: Home
    url: /
  - title: Strategy
    url: /technical-strategy
  - title: Setup
    url: /setup
  - title: Team
    url: /team
```

## Troubleshooting

### Site Not Loading
- Check that GitHub Pages is enabled in Settings
- Verify the source is set to `main` branch and `/docs` folder
- Wait a few minutes for deployment to complete

### 404 Errors
- Ensure all markdown files are in the `docs/` directory
- Check that file names match the URLs (e.g., `setup.md` → `/setup`)
- Verify `_config.yml` is in the `docs/` directory

### Styling Issues
- Clear your browser cache
- Check that `_config.yml` has the correct theme
- Verify markdown formatting is correct

## Updating Your Site

Whenever you make changes:

```bash
git add .
git commit -m "Update documentation"
git push
```

GitHub Pages will automatically rebuild and deploy your site within 1-2 minutes.

## Additional Resources

- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Jekyll Themes](https://pages.github.com/themes/)
- [Markdown Guide](https://www.markdownguide.org/)

---

**Your documentation site will be live at:**
`https://YOUR_USERNAME.github.io/ai-for-industry-challenge/`
