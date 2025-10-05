# GitHub Pages Setup Guide

Your beautiful documentation site is ready! Follow these steps to publish it.

## Quick Setup (5 minutes)

### 1. Update Repository URLs

Edit `docs/script.js` (line 2-3):
```javascript
const GITHUB_USER = 'yourusername';  // ← Change this to your GitHub username
const GITHUB_REPO = 'pngmeta';
```

Edit `docs/index.html` and replace all `yourusername` with your actual GitHub username:
```bash
# Quick find/replace
sed -i '' 's/yourusername/YOUR_ACTUAL_USERNAME/g' docs/index.html docs/script.js
```

### 2. Enable GitHub Pages

1. Push your code to GitHub:
   ```bash
   git add docs/
   git commit -m "Add GitHub Pages documentation site"
   git push origin main
   ```

2. Go to your repository on GitHub
3. Click **Settings** → **Pages** (in sidebar)
4. Under **Source**:
   - Branch: `main`
   - Folder: `/docs`
5. Click **Save**

### 3. View Your Site

After 1-2 minutes, your site will be live at:
```
https://YOUR_USERNAME.github.io/pngmeta/
```

Check the Pages settings for the exact URL.

## Features of Your Site

✨ **Live Statistics**
- GitHub stars (auto-updated from API)
- PyPI downloads (from pypistats)
- Latest release info

🎨 **Modern Design**
- Gradient hero section
- Responsive mobile layout
- Smooth animations
- Copy-to-clipboard buttons

📝 **Comprehensive Sections**
- Features overview
- Installation guide
- Code examples with syntax highlighting
- API comparison with iptcinfo3
- Latest release information
- Documentation links

## Customization

### Change Colors

Edit `docs/styles.css`:
```css
:root {
    --primary: #667eea;      /* Main purple */
    --secondary: #764ba2;    /* Gradient end */
    /* Change these to your preferred colors */
}
```

### Update Content

All content is in `docs/index.html`. Sections are clearly labeled with comments.

### Add Your Logo

Replace the SVG logo in the hero section of `index.html` or add an image:
```html
<div class="logo">
    <img src="logo.png" alt="pngmeta" width="60">
</div>
```

## Custom Domain (Optional)

If you own a domain:

1. Edit `docs/CNAME`:
   ```
   pngmeta.yourdomain.com
   ```

2. Add DNS record:
   - Type: CNAME
   - Name: pngmeta
   - Value: YOUR_USERNAME.github.io

3. Wait for DNS propagation (up to 24 hours)

## Local Preview

Test locally before pushing:

```bash
cd docs
python3 -m http.server 8000
# Visit: http://localhost:8000
```

Or use any static server:
```bash
# Node.js
npx serve docs

# PHP
php -S localhost:8000 -t docs
```

## Troubleshooting

### Badges showing "PACKAGE NOT FOUND"?

**Cause**: Shields.io cache hasn't updated yet (normal for new packages)

**Fix**:
1. ✅ Your package IS live: https://pypi.org/project/pngmeta/
2. ⏳ Badges auto-update in 2-6 hours
3. ✅ `pip install pngmeta` works now!
4. See `docs/BADGE_REFRESH.md` for details

### Stats showing "--" or "New!"?

**Cause**: Package just published, stats not yet available

**Fix**:
1. Download stats update daily
2. Will show real numbers after 24 hours
3. "New!" badge is intentional for fresh packages

### Page not updating?

**Cause**: GitHub Pages cache

**Fix**:
1. Wait 1-2 minutes after pushing
2. Hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
3. Check GitHub Actions tab for build status

### 404 errors?

**Cause**: Pages not enabled or wrong folder

**Fix**:
1. Verify Settings → Pages shows `/docs` folder
2. Check the `.nojekyll` file exists in `docs/`
3. Ensure `docs/index.html` exists

## API Rate Limits

- **GitHub API**: 60 requests/hour (anonymous)
- **PyPI Stats**: No strict limit

For high-traffic sites, consider:
- Adding a backend cache
- Using authenticated GitHub API calls
- Implementing CDN caching

## Updating the Site

When you update the docs:

```bash
# Edit files in docs/
git add docs/
git commit -m "Update documentation"
git push

# GitHub Pages auto-deploys in 1-2 minutes
```

## Next Steps

1. ✅ Enable GitHub Pages
2. ✅ Update username in files  
3. ✅ Test the live site
4. ✅ Share the URL!
5. ✅ Consider adding to README.md:
   ```markdown
   ## Documentation
   
   Visit the [documentation site](https://YOUR_USERNAME.github.io/pngmeta/)
   ```

## Need Help?

- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [GitHub Pages Community](https://github.community/c/github-pages/)
- Open an issue in your repository
