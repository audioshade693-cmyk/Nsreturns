import streamlit as st
import pandas as pd
import os
import requests
import re
from io import BytesIO

# --- CATEGORIZATION DATA ---
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

# --- PRE-PROCESS MAP ---
sku_to_category_map = {}
for category, data in categories.items():
    for sku in data['skus']:
        cleaned_key = re.sub(r'\s+', '', sku, flags=re.UNICODE).lower()
        sku_to_category_map[cleaned_key] = category

# --- PAGE SETUP ---
st.set_page_config(page_title="Flipkart Return Processor", layout="wide")
st.title("📦 Flipkart Return Processor")

# --- EMAIL FUNCTION ---
def send_email(summary_df, cust_total, cour_total, grand_total):
    # Streamlit uses st.secrets instead of os.environ
    try:
        api_key = st.secrets["SENDER_PASSWORD"]
        sender = st.secrets.get("SENDER_EMAIL", "nalt3224@gmail.com")
        recipient = st.secrets.get("RECIPIENT_EMAIL", "nsworld003@gmail.com")
    except:
        return "⚠️ Secrets not configured in Streamlit Cloud."

    email_df = summary_df.drop(columns=['Tracking_IDs'], errors='ignore')
    html_body = f"""
    <html><body>
        <h2>Flipkart Return Summary</h2>
        <p><b>Total Customer:</b> {cust_total} | <b>Total Courier:</b> {cour_total} | <b>Grand Total:</b> {grand_total}</p>
        {email_df.to_html(index=False)}
    </body></html>
    """
    
    url = "https://api.sendgrid.com/v3/mail/send"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {
        "personalizations": [{"to": [{"email": recipient}]}],
        "from": {"email": sender},
        "subject": "Returns NS Summary",
        "content": [{"type": "text/html", "value": html_body}]
    }

    response = requests.post(url, headers=headers, json=data)
    return "✅ Email Sent!" if response.status_code < 300 else f"❌ Email Failed: {response.text}"

# --- UI ---
uploaded_file = st.file_uploader("Upload Flipkart CSV", type=['csv'])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file, encoding_errors='ignore')
        
        # Data Cleaning
        df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce').fillna(0)
        df['Clean_SKU'] = df['SKU'].astype(str).apply(lambda x: re.sub(r'\s+', '', x).lower())
        df['Category'] = df['Clean_SKU'].map(sku_to_category_map).fillna('Uncategorized')
        df['Return Type Clean'] = df['Return Type'].astype(str).str.lower().apply(
            lambda x: 'Courier Return' if 'courier' in x else 'Customer Return'
        )

        # Summary calculations
        summary = df.groupby(['Category', 'Return Type Clean'])['Quantity'].sum().reset_index()
        cust_total = summary[summary['Return Type Clean'] == 'Customer Return']['Quantity'].sum()
        cour_total = summary[summary['Return Type Clean'] == 'Courier Return']['Quantity'].sum()
        
        st.write("### Summary Report")
        st.dataframe(summary)

        # Export to Excel
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df[['Category', 'Return Type Clean', 'Tracking ID', 'SKU', 'Quantity']].to_excel(writer, index=False)
        
        st.download_button(
            label="📥 Download Detailed Excel",
            data=output.getvalue(),
            file_name="return_summary.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        if st.button("📧 Send Email Summary"):
            status = send_email(summary, cust_total, cour_total, cust_total + cour_total)
            st.info(status)

    except Exception as e:
        st.error(f"Error: {e}")
