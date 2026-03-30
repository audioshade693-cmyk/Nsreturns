import pandas as pd
import gradio as gr
import openpyxl # Required by pandas for WRITING Excel
import os # Required for reading secrets
import requests # Required for SendGrid
import re # Added for aggressive cleaning

# --- YOUR ORIGINAL CATEGORIZATION ---
categories = {
    'Grey Wired': {'skus': ['greywiredn7313', 'greywirednoe3121', 'greywirednoe912', 'greywirednoe5', 'greywired2', 'wirednewshopsy1', 'greywiredneo02', 'greywirednoe3112', 'greywired9323', 'greywiredflip1', 'wiregreyvbe3', 'wiredgreyneiw8213']},
    'Cable': {'skus': ['cable4inone', '4x1cable', 'cable4inone##', '4inonecable', 'cableshade242', 'cable4new', '4in1charging', 'flipcable', '4in1cableyelloww']},
    'Black': {'skus': ['blackthunder06', 'blackthundernew', 'blackshopsyns2id3', 'black37232', 'blackshade213', 'blackshopsy2xnnn', 'blackns3233', 'blackshopsy4cb3331', 'blackshopsycx34', 'blackshopsy3cbcbs', 'blackthunder02', 'blackshadend3dc', 'blackns3chc3299', 'blacknsshopsy424', 'blackshopsyy3733', 'blacknsthunder', 'zenbuds38271', 'shenzenblack', 'blackvdltch3nd', 'blackbaby', 'blackshopsy#', 'blackns231shopsy', 'black01', 'blackdark1buds', 'blackshopsycnn3c', 'blacknotydxbex', 'blackns3xncc', 'shopsynew4nch4', 'blackthunderbudsflip0087', 'blackbaclk', 'blacknewshop3c4', 'blacknew4213', 'blacknewshopcy', 'blackbuds2vd', 'blackshopsynce3', 'blacknsflip3jce', 'blackshopsy31781', 'blacknew22', 'zenbudsblackshopsy322', 'blackflipnew3', 'blackthunder04', 'blackbuds31314', 'blacknewflip', 'flipmacv3.0', 'blackthunderbudsflip097', 'zenbudsblackflip2', 'flipns3883black', 'flipblackzen1', 'blackns3251', 'blacknsncbe3', 'zenbudsv3.0', 'black2', 'flipblackpody', 'blackshop024', 'blackflip4242f', 'blackshopshy37cb3', 'zenbudsog', 'blacknsflipsj3c', 'black', 'blackm1flip', 'black5311shopsy', 'maverixshopsyblack', 'blackns47361', 'black6312shop', 'blacknsflip34002', 'blackflipnb3c', 'blacknsdh3n4t', 'blackflipcf3', 'blackflipkart3131', 'blackns37474', 'blackthunderbudsflip01', 'blackflip842hf', 'blackns2cncncncn', 'cable+black', 'blackflip2113', 'blackshopcn3cs', 'blackthunder05', 'blackflip37522', 'blackshosy442', 'flipnsblack657', 'blackns37f74c', 'blackflip3c42', 'blacknsw39c3', 'blackthunderbudsflip06', 'blackthunderflip', 'flipblacknew45', 'blacflipz2', 'flipmave1', 'blackthunderbudsflip08', 'blackflip371344', 'blackflipndnd3', 'blackflipkart', 'maverixv2flip', 'blackns3873v', 'blackflipb423nc', 'blackflipdn24', 'blacknsn352', 'blackns3cnnns', 'blackflip4424', 'blackflip74gd', 'blackflipkd3c', 'blackwire82ccc', 'blackflipns1', 'blackflipj3nc83', 'blackflipzen3', 'blackjanam', 'blackflipkart2', 'comboblackandredcable', 'maverixv2shops', 'zenbudsv2is', 'maverixv2shopsy', 'flipnsblack6567', 'blackpb2321', 'combo black and red cable']},
    'Case White': {'skus': ['pbwhiteyello', 'casewhitec3934993', 'casewhite383838', 'whitecombocase35', 'whitewithcovercombo392783', 'whitewithcase2ici3vd', 'whitecasen3nsn', 'caseyellow32cmvvv', 'whitecombocase4', 'whitecovercombo', 'whitewithcaseandcover', 'whitecombocase2', 'whitecasecombo38341', 'whitecasensn3nx', 'casewhite2xyellow', 'whitecombocoverns231', 'whitecasebxn3c', 'whitecaseflipcme', 'whitecombocoverflip324', 'casewhiteyellows993', 'newbudsw1']},
    'Holder': {'skus': ['metalholder3cc3', 'holderrx9', 'metalholder424', 'holdershopsynew', 'holdershopsy32d3', 'mobileholder1', 'holderxx3', 'holderflipkart1']},
    'White': {'skus': ['whiteshopsy45', 'whiteshopsyt43', 'whiteshopsy371734', 'white7', 'white3', 'whiteshopsy34479', 'whitens313xj', 'whitens38475', 'whitegaming1', 'white', 'whitens38c4', 'whitens4flip3c', 'whitens3847f', 'whitense93cn', 'whitepb343231', 'whiteshopsy435c', 'whitens3134flipc', 'whiteshade341', 'whiteshopsy45bc3', 'white00new', 'white1', 'whitens56', 'whiteshopsybbce2', 'whitenew211flip', 'flipwhitens131', 'flipns2214c', 'whitens3742c', 'whitensflip213c', 'whitens3144flip', 'whitns33flip', 'whitenew55flip', 'whitens47d53c', 'white4', 'whitejaishreeram', 'whiteshopsy36264', 'whitecombocover', 'whitecombocoverflip1', 'whitecasenxnex', 'whiteCASEnxenx']},
    'Holder And Cable': {'skus': ['combo holder+4inone']},
    'Neckband': {'skus': ['neckband3d93d93', 'neckbandxi3nn3', 'neckband39cx9jj', 'neckband87128', 'neckband30cnc2', 'neckbandtpt1', 'neckband32939cb', 'neckband28hd28d', 'neckbandcn3n3d', 'neckblack2dk', 'neckband29k3kc', 'neckband2929f83', 'neckblack2cx354', 'neckblackn39c', 'neckband9d3ucecw', 'neckbandcn39v888', 'neckband39dnc', 'neckband2d93kd', 'neckblack23c3', 'neckband39c933', 'neckband39c93', 'neckbandsn3999', 'neckband28cb37cbb', 'neckband3s38c84n', 'neckband03323', 'neckbandflip21222', 'lajpatneck3', 'neckbandflip223134', 'neckband33c3cb']},
    'Case Black': {'skus': ['blackcase323nnc3', 'blackcase88012', 'blackcase001', 'blackcase013', 'blackcase010', 'blackcasethine', 'blackcasens232', 'blackcase2883s2x', 'caseblack299393', 'blackcase23s3', 'blackcaseflip3jx3', 'blackcasenx3c', 'blackcase339xn22c', 'blackcasexk3m', 'blackcasecxm3c', 'caseblackne2d', 'blackcase3cnd3', 'blackcase2k3c', 'caseblack29d9mmm3', 'blackcase3xk3m', 'blackcasemxm3c']},
    'CABLEWHITE': {'skus': ['cablewhitenew4', 'cablewhitenew1', 'cablewhiteflio', 'cablewhitenew6', 'cablewhitecolor', 'cablewhitenew2', 'whitecableflip002', 'whitecableflip0077', 'whitecableflip001']},
    'WIREBLACK': {'skus': ['blackwire328cbbb', 'blackwired921xnn', 'blackwired291cx73', 'blackwire293c', 'blackwirex9327cnn', 'wireblack29077c', 'wiredblack', 'wireblack289cbbb', 'wireblack', 'blackwirex29992', 'wireblack29999', 'wireblack287cncc', 'blackwire28181', 'BLACKwire3cnnn2']},
    'Case With yellow cable': {'skus': ['combowhite+yellowcable']},
    'White and Wireblack': {'skus': ['whiteandgreycombo', 'whiteandgreycombo2465f']},
    'Black withe yellow cab': {'skus': ['black+yellocable combo']},
    'White Sticker': {'skus': ['stickerwhite9']},
    'Cable and Greywire': {'skus': ['4inonecable and greywire combo']},
    'Map': {'skus': ['mapbuds']},
    'T800 WATCH': {'skus': ['watch111']}
}
# --- END OF CATEGORIZATION ---


# --- Pre-process the categories to create a fast lookup map (SKU -> Category) ---
sku_to_category_map = {}
for category, data in categories.items():
    for sku in data['skus']:
        # ----- FIX: Remove all whitespace and make lowercase -----
        cleaned_key = re.sub(r'\s+', '', sku, flags=re.UNICODE).lower()
        sku_to_category_map[cleaned_key] = category


# --- EMAIL FUNCTION (using SendGrid) ---
def send_notification_email(summary_df_for_email, customer_return_total, courier_return_total, grand_total):
    """
    Sends a summary email using the SendGrid API.
    Reads credentials from Hugging Face secrets.
    The incoming DataFrame 'summary_df_for_email' should be the summary, not the detailed list.
    """
    sender_email = os.environ.get('SENDER_EMAIL')
    sendgrid_api_key = os.environ.get('SENDER_PASSWORD') # This is your SendGrid API Key
    recipient_email = os.environ.get('RECIPIENT_EMAIL')

    if not sender_email:
        sender_email = "nalt3224@gmail.com"
    if not recipient_email:
        recipient_email = "nsworld003@gmail.com"

    if not sendgrid_api_key:
        print("Email credentials (SendGrid 'SENDER_PASSWORD') not found. Skipping email.")
        return "File processed, but email NOT sent. Reason: 'SENDER_PASSWORD' secret is not set in Hugging Face."
    
    subject = "Returns NS"
    
    # Create a version of the DataFrame for the email, excluding the Tracking_IDs
    email_df = summary_df_for_email.drop(columns=['Tracking_IDs'], errors='ignore')

    # Create the HTML body using the summary
    html_body = f"""
    <html>
    <head>
    <style>
        body {{ font-family: Arial, sans-serif; }}
        table {{ border-collapse: collapse; width: 90%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
    </style>
    </head>
    <body>
        <h2>Flipkart Return Summary</h2>
        <p>Here is the summary of today's returns:</p>
        <ul>
            <li><b>Total Customer Returns:</b> {customer_return_total} units</li>
            <li><b>Total Courier Returns:</b> {courier_return_total} units</li>
            <li><b>Grand Total Returns:</b> {grand_total} units</li>
        </ul>
        <h3>Detailed Breakdown by Category (No Tracking IDs):</h3>
        {email_df.to_html(index=False)} 
    </body>
    </html>
    """
    
    url = "https://api.sendgrid.com/v3/mail/send"
    headers = {"Authorization": f"Bearer {sendgrid_api_key}", "Content-Type": "application/json"}
    
    data = {
        "personalizations": [{"to": [{"email": recipient_email}]}],
        "from": {"email": sender_email},
        "subject": subject,
        "content": [{"type": "text/html", "value": html_body}]
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        if 200 <= response.status_code < 300:
            print(f"Notification email sent successfully! Status: {response.status_code}")
            return "File processed AND email sent successfully!"
        else:
            print(f"EMAIL FAILED: Status: {response.status_code}, Body: {response.text}")
            return f"File processed, but email FAILED. SendGrid Error: {response.text}"
    except Exception as e:
        print(f"Failed to send email: {e}")
        return f"File processed, but email FAILED. Error: {str(e)}"

# --- The Core Processing Function ---
def process_return_file(uploaded_file):
    """
    Processes the uploaded Flipkart return file (CSV).
    """
    if uploaded_file is None:
        raise gr.Error("Please upload a file first.")

    try:
        # --- 1. File Processing ---
        # ----- Read as CSV with robust encoding detection -----
        df = None
        encodings_to_try = ['utf-8', 'utf-8-sig', 'cp1252', 'latin1'] # Removed utf-16 as it's less likely for this error
        
        for encoding in encodings_to_try:
            try:
                # Use engine='python' for flexibility
                df = pd.read_csv(
                    uploaded_file.name, 
                    on_bad_lines='skip', 
                    encoding=encoding,
                    engine='python' 
                )
                print(f"File read successfully with encoding: {encoding}") 
                break # If successful, stop trying
            except (UnicodeDecodeError, pd.errors.ParserError, LookupError) as e:
                print(f"Failed to read with encoding {encoding}: {e}")
                continue # Try the next encoding

        if df is None:
            # If all encodings failed
            raise gr.Error("Failed to parse the file. The file encoding is not supported or the file is corrupt. Please try re-downloading from Flipkart or re-saving as a CSV (UTF-8) in Excel/Google Sheets and try again.")
        # ---------------------------------------------------------------------
        
        required_cols = ['Tracking ID', 'SKU', 'Quantity', 'Return Type']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise gr.Error(f"File is missing required columns: {', '.join(missing_cols)}. Found columns: {list(df.columns)}")

        # --- 2. Data Cleaning and Transformation ---
        df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce').fillna(0)
        df['SKU'] = df['SKU'].astype(str) # Convert to string first
        df['Return Type'] = df['Return Type'].astype(str).str.strip()
        
        # ----- AGGRESSIVE SKU CLEANING (from last time) -----
        # Create a 'Clean_SKU' by removing ALL whitespace and making lowercase
        df['Clean_SKU'] = df['SKU'].apply(lambda x: re.sub(r'\s+', '', x, flags=re.UNICODE).lower())
        
        # Map using the 'Clean_SKU' column
        df['Category'] = df['Clean_SKU'].map(sku_to_category_map).fillna('Uncategorized')
        
        df['Simplified Return Type'] = df['Return Type'].apply(
            lambda x: 'Courier Return' if x.lower() == 'courier_return' else 'Customer Return' # Made return type check case-insensitive
        )
        
        # --- 3. Create Excel Output (Line-by-Line) ---
        # We use the original 'SKU' column, which still has its original case
        excel_df = df[['Category', 'Simplified Return Type', 'Tracking ID', 'SKU', 'Quantity']]
        excel_df = excel_df.sort_values(by=['Category', 'Simplified Return Type', 'Tracking ID'])
        
        output_filename = "return_summary.xlsx"
        excel_df.to_excel(output_filename, index=False, engine='openpyxl')

        # --- 4. Create Summary for Email ---
        grouped = df.groupby(['Category', 'Simplified Return Type'])
        summary_df = grouped.agg(
            Total_Quantity=('Quantity', 'sum')
        ).reset_index()
        summary_df = summary_df.sort_values(by=['Category', 'Simplified Return Type'])
        
        # --- 5. Email Logic ---
        customer_return_total = int(summary_df[summary_df['Simplified Return Type'] == 'Customer Return']['Total_Quantity'].sum())
        courier_return_total = int(summary_df[summary_df['Simplified Return Type'] == 'Courier Return']['Total_Quantity'].sum())
        grand_total = int(summary_df['Total_Quantity'].sum())

        email_status = send_notification_email(
            summary_df, 
            customer_return_total, 
            courier_return_total, 
            grand_total
        )
        
        return output_filename, email_status

    except pd.errors.ParserError:
        raise gr.Error("Failed to parse the file. Please ensure it's a valid Excel or CSV file.")
    except Exception as e:
        # This will catch other errors
        raise gr.Error(f"An error occurred: {str(e)}")

# --- Create and Launch the Gradio App ---
app = gr.Interface(
    fn=process_return_file,
    inputs=gr.File(
        label="Upload Flipkart Return File (CSV or .xls)",
        # ----- THIS IS THE MOBILE FIX -----
        file_types=[".csv", ".xls"]
        # ------------------------------------
    ),
    outputs=[
        gr.File(label="Download Detailed Summary (Excel)"),
        gr.Textbox(label="Email Status")
    ],
    title="Flipkart Return Processor",
    description=(
        "Upload your daily return Excel or CSV file from Flipkart. \n"
        "The app will categorize SKUs, provide a detailed line-by-line Excel output, and email a high-level summary."
        "\n\n**Required columns in the file:** `Tracking ID`, `SKU`, `Quantity`, `Return Type`"
    )
)

# Launch the app
if __name__ == "__main__":
    app.launch()
