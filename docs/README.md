# pngmeta Documentation Site

This directory contains the GitHub Pages documentation site for pngmeta.

## Files

- `index.html` - Main documentation page
- `styles.css` - Styling and animations
- `script.js` - JavaScript for GitHub/PyPI API integration and interactivity
- `.nojekyll` - Prevents Jekyll processing
- `CNAME` - Custom domain configuration (optional)

## Features

### Live Statistics
- **GitHub Stars** - Fetched from GitHub API
- **PyPI Downloads** - Fetched from pypistats API
- **Latest Release** - Automatically shows latest GitHub release

### Sections
1. **Hero** - Main introduction with badges and stats
2. **Features** - Why use pngmeta
3. **Installation** - Quick install commands with copy buttons
4. **Quick Example** - Live code example with syntax highlighting
5. **Features Detail** - Comprehensive feature breakdown
6. **Latest Release** - Download latest version
7. **Documentation** - Links to all docs
8. **Comparison** - Side-by-side with iptcinfo3
9. **Footer** - Links and resources

## Setup

### 1. Update Repository Information

Edit `script.js` and update these variables:
```javascript
const GITHUB_USER = 'yourusername';  // Your GitHub username
const GITHUB_REPO = 'pngmeta';
```

Edit `index.html` and replace all instances of:
- `yourusername` with your actual GitHub username
- Update any other URLs as needed

### 2. Enable GitHub Pages

1. Go to your repository settings
2. Navigate to "Pages" section
3. Under "Source", select the branch (usually `main`)
4. Set the directory to `/docs`
5. Click "Save"

Your site will be available at: `https://yourusername.github.io/pngmeta/`

### 3. Custom Domain (Optional)

If you have a custom domain:

1. Edit `CNAME` file and add your domain:
   ```
   pngmeta.yourdomain.com
   ```

2. Add DNS records for your domain:
   - Type: CNAME
   - Name: pngmeta (or your subdomain)
   - Value: yourusername.github.io

## Customization

### Colors

Edit CSS variables in `styles.css`:
```css
:root {
    --primary: #667eea;
    --secondary: #764ba2;
    /* ... */
}
```

### Content

All content is in `index.html`. Sections are clearly marked with comments.

### Features

Add/remove features in the `.features-grid` section.

### Code Examples

Update code examples in the `.example` section.

## Local Development

Open `index.html` in a browser or use a local server:

```bash
# Python 3
python -m http.server 8000

# Then visit: http://localhost:8000
```

## API Rate Limits

The site uses public GitHub and PyPI APIs:
- **GitHub**: 60 requests/hour (unauthenticated)
- **PyPI**: No strict limits

For production with many visitors, consider:
1. Caching API responses
2. Using GitHub personal access token
3. Implementing backend proxy

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers

## Performance

- Minimal dependencies (no frameworks)
- Optimized CSS with CSS Grid/Flexbox
- Async API calls
- Smooth scroll and animations
- Responsive design

## Troubleshooting

**Stats showing "--" or emoji?**
- Check browser console for API errors
- Verify GitHub username/repo in script.js
- Ensure repository is public

**Styles not loading?**
- Check paths are relative (no leading /)
- Clear browser cache
- Check console for errors

**GitHub Pages not updating?**
- Can take a few minutes to deploy
- Check repository settings > Pages
- Ensure .nojekyll file exists
