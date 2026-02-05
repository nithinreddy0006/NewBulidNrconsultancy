
import os
import re

files = [
    r"C:\Users\Nithi\.gemini\antigravity\NewNrconsultancybulid\portfolio.html",
    r"C:\Users\Nithi\.gemini\antigravity\NewNrconsultancybulid\single-portfolio.html"
]

newsletter_replacement = """<img src="assets/img/logo/logo.png" alt="NR Consultancy Logo" style="height: 60px; margin-bottom: 20px;">
                            <div class="space-20"></div>
                            <small>Newsletter</small>
                            <div class="space-20"></div>
                            <h2>Stay Compliant! Subscribe to our <span>Newsletter</span></h2>"""

# Social replacement (generic for all) - we will replace specific icons based on their order or recreate the list
# Actually, the file has 5 columns. I will reconstruct the whole inner row of social-area.
# But regex matching a large block is risky.
# I will match the specific style pattern and replace it.

def fix_file(filepath):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix Newsletter
    # We look for the <small>Newsletter</small>... block
    # We'll use a regex that matches the whitespace
    newsletter_pattern = re.compile(r'<small>Newsletter</small>\s*<div class="space-20"></div>\s*<h2>Stay up to date, subscribe to the free <span>newsletter !</span></h2>', re.DOTALL)
    
    if newsletter_pattern.search(content):
        # We need to preserve the indentation of the start, but we can just use the replacement string which keeps some indentation
        # Actually, let's just use simple string replace if we can match enough uniqueness
        content = newsletter_pattern.sub(newsletter_replacement, content)
        print(f"Fixed Newsletter in {filepath}")
    else:
        print(f"Newsletter pattern not found in {filepath}")

    # Fix Social Icons
    # There are 5 icons.
    # 1. LinkedIn (social4.png)
    # 2. Facebook (social1.png)
    # 3. Dribbble/Instagram (social2.png) - wait, template had duplicates
    # 4. Twitter (social3.png)
    # 5. Instagram (social2.png)
    
    # We will replace the whole style="..." attribute and the text.
    
    # Pattern 1: LinkedIn
    # style="background: url(assets/img/social/social4.png);..."
    # Text: join our instagram community! -> Connect on LinkedIn
    
    # We'll use a specific regex for each.
    
    # LinkedIn
    content = re.sub(
        r'style="background: url\(assets/img/social/social4\.png\);[^"]*"',
        'style="background-color: #0e76a8;"',
        content
    )
    # Fix text inside the LinkedIn block (we assume it follows the style change we just identified? No, we just changed the style)
    # We need to find the text "join our instagram community!" closest to the LinkedIn icon?
    # It's better to match the whole block.
    
    # Regex for a single social item block
    # We can match by the icon class.
    
    # LinkedIn Block
    content = re.sub(
        r'(<div class="sinlge-social-hover"[^>]*background-color: #0e76a8;[^>]*>.*?<a href=")([^"]*)(" target="_blank">.*?<i class="fab fa-linkedin-in"></i>.*?<p class="single-soicial-text">\s*)join our\s*instagram\s*community!(\s*</p>)',
        r'\1https://linkedin.com/in/nrconsultancyforyou06\3Connect on\n                                            LinkedIn\4',
        content, flags=re.DOTALL
    )
    # Wait, the previous sub changed the style. The href was empty before.
    
    # Let's do it in one pass per icon.
    
    # 1. LinkedIn
    # Match the style with social4.png
    content = re.sub(
        r'(<div class="sinlge-social-hover"\s*)style="background: url\(assets/img/social/social4\.png\);[^"]*"',
        r'\1style="background-color: #0e76a8;"',
        content
    )
    # Now find the text. The href is empty "".
    # <a href=""> -> <a href="https://linkedin.com/in/nrconsultancyforyou06" target="_blank">
    # And text.
    # We look for the block containing fa-linkedin-in
    
    # Since all blocks have "join our instagram community!", we rely on the icon class to distinguish.
    
    # Update LinkedIn Text & Link
    content = re.sub(
        r'(<a href=")[^"]*("\s*>\s*<span class="single-social-icon">\s*<i class="fab fa-linkedin-in"></i>\s*</span>\s*<p class="single-soicial-text">\s*)join our\s*instagram\s*community!(\s*</p>)',
        r'\1https://linkedin.com/in/nrconsultancyforyou06\2Connect on\n                                            LinkedIn\3',
        content, flags=re.DOTALL
    )
    # Add target="_blank" to LinkedIn
    content = content.replace('href="https://linkedin.com/in/nrconsultancyforyou06"', 'href="https://linkedin.com/in/nrconsultancyforyou06" target="_blank"')


    # 2. Facebook (social1.png)
    content = re.sub(
        r'(<div class="sinlge-social-hover"\s*)style="background: url\(assets/img/social/social1\.png\);[^"]*"',
        r'\1style="background-color: #3b5998;"',
        content
    )
    content = re.sub(
        r'(<a href=")[^"]*("\s*>\s*<span class="single-social-icon">\s*<i class="fab fa-facebook-f"></i>\s*</span>\s*<p class="single-soicial-text">\s*)join our\s*instagram\s*community!(\s*</p>)',
        r'\1#\2Follow on\n                                            Facebook\3',
        content, flags=re.DOTALL
    )

    # 3. Dribbble/Basketball (social2.png first occurrence) - Let's change this to "Email" or just remove?
    # User just said "social media icons". I'll Keep it as Email? Or just generic.
    # The icon is fa-basketball-ball (Dribbble). Let's change to Envelope (Email)?
    # Or just keep it as is but fix background.
    content = re.sub(
        r'(<div class="sinlge-social-hover"\s*)style="background: url\(assets/img/social/social2\.png\);[^"]*"',
        r'\1style="background-color: #ea4c89;"', # Pink for Dribbble or general
        content, count=1 # Only first one (Dribbble/Basketball)
    )
    content = re.sub(
        r'(<a href=")[^"]*("\s*>\s*<span class="single-social-icon">\s*<i class="fas fa-basketball-ball"></i>\s*</span>\s*<p class="single-soicial-text">\s*)join our\s*instagram\s*community!(\s*</p>)',
        r'\1#\2Follow on\n                                            Dribbble\3',
        content, flags=re.DOTALL
    )

    # 4. Twitter (social3.png)
    content = re.sub(
        r'(<div class="sinlge-social-hover"\s*)style="background: url\(assets/img/social/social3\.png\);[^"]*"',
        r'\1style="background-color: #00acee;"',
        content
    )
    content = re.sub(
        r'(<a href=")[^"]*("\s*>\s*<span class="single-social-icon">\s*<i class="fab fa-twitter"></i>\s*</span>\s*<p class="single-soicial-text">\s*)join our\s*instagram\s*community!(\s*</p>)',
        r'\1https://x.com/nrconsultancyforyou06\2Follow on\n                                            X (Twitter)\3',
        content, flags=re.DOTALL
    )
    content = content.replace('href="https://x.com/nrconsultancyforyou06"', 'href="https://x.com/nrconsultancyforyou06" target="_blank"')

    # 5. Instagram (social2.png second occurrence) 
    # The previous regex replaced one instance of social2.png.
    # The remaining one should be Instagram.
    content = re.sub(
        r'(<div class="sinlge-social-hover"\s*)style="background: url\(assets/img/social/social2\.png\);[^"]*"',
        r'\1style="background-color: #C13584;"',
        content
    )
    content = re.sub(
        r'(<a href=")[^"]*("\s*>\s*<span class="single-social-icon">\s*<i class="fab fa-instagram"></i>\s*</span>\s*<p class="single-soicial-text">\s*)join our\s*instagram\s*community!(\s*</p>)',
        r'\1https://instagram.com/nrconsultancyforyou06\2Follow on\n                                            Instagram\3',
        content, flags=re.DOTALL
    )
    content = content.replace('href="https://instagram.com/nrconsultancyforyou06"', 'href="https://instagram.com/nrconsultancyforyou06" target="_blank"')

    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

for p in files:
    fix_file(p)
