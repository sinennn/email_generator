import time
import random
import requests
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

BASE_URL = "https://api.mail.tm"
MASTER_PASSWORD = "YourGlobalPassword123!"
TOTAL_ACCOUNTS_NEEDED = 100

def get_available_domain():
 
    try:
        response = requests.get(f"{BASE_URL}/domains?limit=1")
        print(f"Domain endpoint status: {response.status_code}")
        
        if response.status_code == 200:
            if response.text:
                domains_data = response.json().get('hydra:member', [])
                if domains_data:
                    return domains_data[0]['domain']
            else:
                print("Domain endpoint returned empty response")
        else:
            print(f"Domain endpoint returned status {response.status_code}: {response.text[:200]}")
    except requests.exceptions.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")
        print(f"Response content: {response.text[:200] if 'response' in locals() else 'N/A'}")
    except requests.exceptions.RequestException as e:
        print(f"Network error fetching domain: {e}")
    except Exception as e:
        print(f"Error fetching domain: {e}")
    return None

def generate_random_username():
    """Generates a human-readable username (e.g., 'peachyavocado')."""
    adjectives = [
        'peachy', 'fuzzy', 'sleepy', 'happy', 'silly', 'bouncy', 'speedy', 'cozy',
        'swift', 'clever', 'mighty', 'gentle', 'bright', 'shiny', 'wild', 'calm',
        'bold', 'eager', 'fresh', 'grand', 'keen', 'lively', 'neat', 'quick',
        'smooth', 'tender', 'witty', 'zesty', 'amber', 'charming', 'dreamy',
        'elegant', 'fabulous', 'glorious', 'harmonic', 'jovial', 'kind', 'lavish',
        'mighty', 'noble', 'opulent', 'proud', 'quirky', 'radiant', 'serene', 'tiny',
        'unique', 'vivid', 'warm', 'zealous', 'adventurous', 'blissful', 'cosmic'
    ]
    
    nouns = [
        'avocado', 'banana', 'cherry', 'dragon', 'eagle', 'falcon', 'giraffe',
        'hedgehog', 'iguana', 'jaguar', 'koala', 'leopard', 'monkey', 'narwhal',
        'ostrich', 'penguin', 'quail', 'rabbit', 'squirrel', 'tiger', 'unicorn',
        'vulture', 'whale', 'xenops', 'yak', 'zebra', 'alpaca', 'bear', 'cat',
        'dolphin', 'elephant', 'fox', 'goose', 'hippo', 'ibis', 'kitten', 'lynx',
        'meerkat', 'newt', 'otter', 'panda', 'raven', 'seal', 'turkey', 'viper',
        'wolf', 'xray', 'zebra', 'butterfly', 'crocodile', 'dragonfly', 'firefly'
    ]
    
    adjective = random.choice(adjectives)
    noun = random.choice(nouns)
    return f"{adjective}{noun}"

def save_emails_to_pdf(email_list, filename="created_emails.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    story = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=22, spaceAfter=8, textColor=colors.HexColor('#2563eb'))
    meta_style = ParagraphStyle('MetaStyle', parent=styles['Normal'], fontSize=10, spaceAfter=20, textColor=colors.HexColor('#64748b'))
    cell_style = ParagraphStyle('CellStyle', parent=styles['Normal'], fontSize=11, leading=14)
    header_style = ParagraphStyle('HeaderStyle', parent=styles['Normal'], fontSize=11, bold=True, textColor=colors.white)

    story.append(Paragraph("Generated Temporary Email Accounts", title_style))
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    story.append(Paragraph(f"<b>Date:</b> {current_time} | <b>Total:</b> {len(email_list)} Accounts | <b>Password for all:</b> {MASTER_PASSWORD}", meta_style))
    
    table_data = [[Paragraph("<b>#</b>", header_style), Paragraph("<b>Temporary Email Address</b>", header_style)]]
    for idx, email in enumerate(email_list, 1):
        table_data.append([Paragraph(str(idx), cell_style), Paragraph(email, cell_style)])
        
    email_table = Table(table_data, colWidths=[40, 480])
    email_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
    ]))
    
    story.append(email_table)
    doc.build(story)

def main():
    print(f"Fetching available domain from Mail.tm...")
    domain = get_available_domain()
    
    if not domain:
        print(" Could not retrieve an active domain. Check your internet connection.")
        return

    print(f"Using domain: @{domain}")
    print(f"Generating {TOTAL_ACCOUNTS_NEEDED} emails. Please wait...\n")

    email_list = []
    
    while len(email_list) < TOTAL_ACCOUNTS_NEEDED:
        username = generate_random_username()
        email_address = f"{username}@{domain}"
        
        payload = {
            "address": email_address,
            "password": MASTER_PASSWORD
        }
        
        try:
            response = requests.post(f"{BASE_URL}/accounts", json=payload)
            
            if response.status_code == 201:
                email_list.append(email_address)
                print(f"[{len(email_list)}/{TOTAL_ACCOUNTS_NEEDED}] Created: {email_address}")
                time.sleep(0.5) 
                
            elif response.status_code == 422:
                continue 
            elif response.status_code == 429:
                print("Rate limit hit. Pausing for 5 seconds...")
                time.sleep(5)
            else:
                print(f"Error (Status {response.status_code}): {response.text}")
                time.sleep(2)
                
        except requests.exceptions.RequestException as e:
            print(f"Network issue: {e}. Retrying in 3 seconds...")
            time.sleep(3)

    print("\n Formatting list and writing to PDF...")
    save_emails_to_pdf(email_list)
    print("Success! File saved as: created_emails.pdf")

if __name__ == "__main__":
    main()


