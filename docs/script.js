// GitHub API Configuration
const GITHUB_USER = 'yourusername'; // Update with actual username
const GITHUB_REPO = 'pngmeta';
const GITHUB_API = `https://api.github.com/repos/${GITHUB_USER}/${GITHUB_REPO}`;

// Copy button functionality
function setupCopyButtons() {
    document.querySelectorAll('.copy-btn').forEach(button => {
        button.addEventListener('click', async () => {
            const textToCopy = button.getAttribute('data-clipboard');
            
            try {
                await navigator.clipboard.writeText(textToCopy);
                const originalText = button.textContent;
                button.textContent = 'Copied!';
                button.style.background = '#48bb78';
                
                setTimeout(() => {
                    button.textContent = originalText;
                    button.style.background = '';
                }, 2000);
            } catch (err) {
                console.error('Failed to copy:', err);
                button.textContent = 'Failed';
                setTimeout(() => {
                    button.textContent = 'Copy';
                }, 2000);
            }
        });
    });
}

// Fetch GitHub repository stats
async function fetchGitHubStats() {
    try {
        const response = await fetch(GITHUB_API);
        if (!response.ok) throw new Error('Failed to fetch GitHub data');
        
        const data = await response.json();
        
        // Update stars count
        const starsCount = data.stargazers_count || 0;
        document.getElementById('stars-count').textContent = starsCount.toLocaleString();
        
        // Update forks count (optional)
        const forksCount = data.forks_count || 0;
        
        console.log(`GitHub Stats: ${starsCount} stars, ${forksCount} forks`);
    } catch (error) {
        console.error('Error fetching GitHub stats:', error);
        document.getElementById('stars-count').textContent = '⭐';
    }
}

// Fetch latest release information
async function fetchLatestRelease() {
    try {
        const response = await fetch(`${GITHUB_API}/releases/latest`);
        if (!response.ok) throw new Error('No releases found');
        
        const release = await response.json();
        
        // Update release information
        document.getElementById('release-name').textContent = release.name || 'Latest Release';
        document.getElementById('release-tag').textContent = release.tag_name || 'v0.1.0';
        
        // Parse and display release notes (first 200 chars)
        const body = release.body || 'View release notes on GitHub';
        const shortBody = body.length > 200 ? body.substring(0, 200) + '...' : body;
        document.getElementById('release-notes').textContent = shortBody;
        
        // Update download link
        document.getElementById('download-link').href = release.html_url;
        
        console.log('Latest release:', release.tag_name);
    } catch (error) {
        console.error('Error fetching release info:', error);
        document.getElementById('release-name').textContent = 'pngmeta 0.1.0';
        document.getElementById('release-notes').textContent = 'First release with full PNG metadata support including tEXt, iTXt, zTXt chunks and XMP.';
    }
}

// Fetch PyPI download stats
async function fetchPyPIStats() {
    try {
        const response = await fetch('https://api.pepy.tech/api/v2/projects/pngmeta');
        if (!response.ok) throw new Error('Failed to fetch PyPI data');
        
        const data = await response.json();
        const downloads = data.total_downloads || 0;
        
        // Format large numbers (e.g., 1.5K, 2.3M)
        let formatted;
        if (downloads >= 1000000) {
            formatted = (downloads / 1000000).toFixed(1) + 'M';
        } else if (downloads >= 1000) {
            formatted = (downloads / 1000).toFixed(1) + 'K';
        } else {
            formatted = downloads.toString();
        }
        
        document.getElementById('downloads-count').textContent = formatted;
        console.log(`PyPI downloads: ${downloads}`);
    } catch (error) {
        console.error('Error fetching PyPI stats:', error);
        // Fallback to showing package emoji
        document.getElementById('downloads-count').textContent = '📦';
    }
}

// Smooth scroll for anchor links
function setupSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href === '#') return;
            
            e.preventDefault();
            const target = document.querySelector(href);
            
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Add scroll-based animations
function setupScrollAnimations() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, {
        threshold: 0.1
    });

    // Observe all sections except hero
    document.querySelectorAll('section:not(.hero)').forEach(section => {
        section.style.opacity = '0';
        section.style.transform = 'translateY(20px)';
        section.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(section);
    });
}

// Initialize all functionality
function init() {
    setupCopyButtons();
    setupSmoothScroll();
    setupScrollAnimations();
    
    // Fetch data from APIs
    fetchGitHubStats();
    fetchLatestRelease();
    fetchPyPIStats();
}

// Run initialization when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
