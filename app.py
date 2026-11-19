import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# 1. Page Configuration (Mobile & Laptop Friendly)
st.set_page_config(
    page_title="SafePay AI - Fraud Awareness Simulator",
    page_icon="🛡️",
    layout="centered"
)

# 2. Train Lightweight AI Fraud Detection Model
@st.cache_resource
def load_ai_model():
    # Features: [Amount (INR), Is_New_Receiver, Is_Collect_Request, Has_Urgent_Link, Late_Night_Tx]
    data = [,      # Safe: regular small transfer,     # Safe: known contact,    # Safe: rent/bill to known receiver,      # Safe: small shop payment,    # Fraud: high amount + collect request + link,    # Fraud: "accept request to receive cashback",    # Fraud: fake KYC link,     # Fraud: lottery/prize collect request,      # Safe: late night food order,    # Fraud: urgent refund scam,     # Safe: new merchant scan,    # Fraud: OLX/marketplace QR scam
    ]
    columns = ["Amount", "New_Receiver", "Collect_Request", "Urgent_Link", "Late_Night", "Fraud"]
    df = pd.DataFrame(data, columns=columns)
    
    X = df.drop("Fraud", axis=1)
    y = df["Fraud"]
    
    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X, y)
    return model

model = load_ai_model()

# 3. App Header
st.title("🛡️ SafePay AI")
st.subheader("Digital Payment Fraud Awareness Simulator")
st.info("Educational Prototype for Financial Literacy & Banking — Fictional Brand")

# 4. Navigation Tabs
tab1, tab2, tab3 = st.tabs(["🤖 AI Risk Analyzer", "🎭 Scam Simulator Quiz", "🏦 Banking Safety Rules"])

# --- TAB 1: AI FRAUD RISK ANALYZER ---
with tab1:
    st.markdown("### Test a Digital Transaction")
    st.write("Enter transaction details below to see how an AI banking engine evaluates fraud risk.")
    
    amount = st.number_input("Transaction Amount (₹)", min_value=1, max_value=500000, value=5000, step=500)
    new_receiver = st.checkbox("Paying a brand-new / unknown recipient?", value=True)
    collect_request = st.checkbox("Did you receive a 'Collect / Request Money' prompt or QR code to RECEIVE funds?", value=False)
    urgent_link = st.checkbox("Did the sender share an external link (KYC update, lottery, refund)?", value=False)
    late_night = st.checkbox("Is this happening late at night (11 PM – 5 AM)?", value=False)

    if st.button("Analyze Transaction with AI", type="primary"):
        features = [[
            amount,
            int(new_receiver),
            int(collect_request),
            int(urgent_link),
            int(late_night)
        ]]
        prediction = model.predict(features)[0]
        fraud_prob = model.predict_proba(features)[0][1] * 100

        st.divider()
        if prediction == 1 or fraud_prob >= 50:
            st.error(f"🚨 HIGH FRAUD RISK DETECTED ({fraud_prob:.1f}% Risk Score)")
            st.markdown("#### Why the AI flagged this:")
            if collect_request:
                st.write("- **Collect Request Trap:** You never need to enter a UPI PIN or scan a QR code to *receive* money.")
            if urgent_link:
                st.write("- **Phishing Link:** Banks never ask customers to update KYC or claim refunds via SMS/WhatsApp links.")
            if new_receiver and amount > 10000:
                st.write("- **High-Value New Payee:** Large transfers to unverified accounts carry high irreversible risk.")
        else:
            st.success(f"✅ LOW RISK TRANSACTION ({fraud_prob:.1f}% Risk Score)")
            st.write("This transaction follows normal digital banking behavior. Always double-check the recipient's verified banking name before entering your PIN.")

# --- TAB 2: INTERACTIVE SCAM SIMULATOR ---
with tab2:
    st.markdown("### Can You Spot the Digital Banking Scam?")
    st.write("Test your financial literacy against real-world fraud scenarios.")

    scenarios = [
        {
            "title": "Scenario 1: The Online Marketplace Buyer",
            "msg": "You listed an old phone for ₹12,000 online. A buyer says: 'I am sending you a QR code on WhatsApp. Scan it and enter your UPI PIN to receive the ₹12,000 advance.'",
            "options": ["Scan QR and enter PIN to get paid", "Refuse and block the buyer"],
            "correct": "Refuse and block the buyer",
            "lesson": "Entering a UPI PIN ALWAYS deducts money from your account. Receiving money requires zero PIN entry."
        },
        {
            "title": "Scenario 2: Urgent Bank KYC Alert",
            "msg": "You get an SMS: 'Dear Customer, your bank account will be blocked tonight. Click bit.ly/bank-kyc-update and enter your debit card details and OTP immediately.'",
            "options": ["Click the link quickly so my account stays active", "Ignore the SMS and check the official bank app"],
            "correct": "Ignore the SMS and check the official bank app",
            "lesson": "Banks never threaten immediate account suspension via shortened links or ask for OTPs/card PINs."
        },
        {
            "title": "Scenario 3: Accidental Money Transfer",
            "msg": "A stranger calls saying they accidentally sent ₹5,000 to your UPI ID and begs you to refund it immediately—even though your bank balance hasn't increased.",
            "options": ["Send ₹5,000 back to be helpful", "Verify your official bank statement first"],
            "correct": "Verify your official bank statement first",
            "lesson": "Scammers send fake SMS notifications to trick victims into transferring their own money."
        }
    ]

    score = 0
    for idx, s in enumerate(scenarios):
        st.markdown(f"**{s['title']}**")
        st.warning(s["msg"])
        choice = st.radio("What do you do?", s["options"], key=f"q_{idx}", index=None)
        if choice:
            if choice == s["correct"]:
                st.success(f"Correct! {s['lesson']}")
                score += 1
            else:
                st.error(f"Scam Alert! {s['lesson']}")
        st.divider()

# --- TAB 3: FINANCIAL LITERACY TAKEAWAYS ---
with tab3:
    st.markdown("### Essential Digital Banking Hygiene")
    st.markdown("""
    * **PIN = Payment Out:** Never enter your UPI PIN, ATM PIN, or OTP to receive money or claim cashback.
    * **Verify Official Channels:** Only download banking apps from official app stores and ignore APK files sent over messaging apps.
    * **Set Transaction Limits:** Use your banking app to set daily UPI and card spending limits to minimize potential losses.
    * **Act Within the Golden Hour:** If scammed, immediately call the **National Cyber Crime Helpline (1930 in India)** or freeze your card/UPI through your bank's official helpline.
    """)
