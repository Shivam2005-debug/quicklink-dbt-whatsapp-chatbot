# # llm_integration/gemini_api.py
# import google.generativeai as genai
# import os
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

# # Get API key from environment variable
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# # CHANGE 3: Using the requested gemini-2.5-flash model
# GEMINI_MODEL = "gemini-2.5-flash"

# # Configure Gemini
# genai.configure(api_key=GEMINI_API_KEY)

# # NEW: Function to load the knowledge base from .txt files
# def load_knowledge_base():
#     """Reads content from the DBT text files and combines them."""
#     knowledge = ""
#     files = [
#         "DBT_Complete_Guide.txt",
#         "DBT_FAQ.txt",
#         "DBT_Security_Support.txt"
#     ]
#     for file_name in files:
#         try:
#             with open(file_name, "r", encoding="utf-8") as f:
#                 knowledge += f.read() + "\n\n"
#         except FileNotFoundError:
#             print(f"Warning: Knowledge file '{file_name}' not found.")
#     return knowledge

# # Load the knowledge base once when the module is imported
# KNOWLEDGE_BASE = load_knowledge_base()

# def get_gemini_response(prompt: str, lang: str = "en") -> str:
#     """
#     Send prompt to Gemini model with a detailed system prompt and integrated knowledge base.
#     lang: 'en' | 'hi' | 'mr' (English, Hindi, Marathi)
#     """
#     # CHANGE 1 & 2: Updated System Prompt
#     system_prompt = f"""
#     You are an expert AI assistant for the MahaDBT (Direct Benefit Transfer) portal, specifically designed to help students in India. Your name is "QuickLink DBT" assistant.

#     *Core Instructions:*
#     1.  *Language:* You MUST respond in the same language as the user's query. Supported languages are English, Hindi, and Marathi.
#     2.  *Information Source:* Your knowledge is STRICTLY LIMITED to the information provided in the following text. Do NOT use any external knowledge or make assumptions.
    
#     --- KNOWLEDGE BASE START ---
#     {KNOWLEDGE_BASE}
#     --- KNOWLEDGE BASE END ---

#     3.  *Role:* Your role is for AWARENESS and INFORMATION only. You provide guidance based on the knowledge base. You do not perform actions.
#     4.  *Redirection:* For any action-oriented queries (like checking status, applying for schemes, or updating details), you MUST guide the user to perform the action on the "QuickLink DBT" web platform. Do not suggest other government portals unless specifically mentioned in the knowledge base.
#     5.  *Safety First:* NEVER ask for personal information like full Aadhaar numbers, bank account numbers, OTPs, or passwords. If a user provides it, politely decline and remind them not to share sensitive data.

#     *Example Scenarios:*
#     *   *If a user asks, "How can I check my DBT status?"*: Your ideal response is, "You can easily check your DBT status on our QuickLink DBT platform. Just go to the 'Check DBT Status' section to verify it securely."
#     *   *If a user asks in Marathi, "माझे आधार बँक खात्याशी जोडलेले आहे, पण मला शिष्यवृत्ती मिळत नाही.":* Respond in Marathi, explaining the difference between linking and seeding based on the provided text, and then guide them to use the 'Learn the Difference' section on the QuickLink DBT platform for more details.
#     *   *If a user asks, "What is DBT?"*: Answer clearly and concisely using only the information from the knowledge base.

#     Now, answer the user's question based on these strict instructions.
#     """
#     try:
#         model = genai.GenerativeModel(GEMINI_MODEL)
        
#         lang_names = {"en": "English", "hi": "Hindi", "mr": "Marathi"}
        
#         final_prompt = f"{system_prompt}\n\nPlease respond in {lang_names.get(lang, 'English')}. User question: {prompt}"
        
#         response = model.generate_content(final_prompt)
#         return response.text
        
#     except Exception as e:
#         return f"Error: {str(e)}"

# # llm_module/llm_integration/gemini_api.py
# import google.generativeai as genai
# import os
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

# # Get API key from environment variable
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# GEMINI_MODEL = "gemini-2.5-flash" 

# # Configure Gemini
# genai.configure(api_key=GEMINI_API_KEY)

# # UPDATED: Function to load the knowledge base from the 'Resources' sub-folder
# def load_knowledge_base():
#     """Reads content from the DBT text files inside the 'Resources' folder."""
#     knowledge = ""
#     # Define the path to the Resources folder relative to this script's location
#     base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
#     resources_dir = os.path.join(base_dir, 'Resources')
    
#     files = [
#         "DBT_Complete_Guide.txt",
#         "DBT_FAQ.txt",
#         "DBT_Security_Support.txt"
#     ]
    
#     for file_name in files:
#         file_path = os.path.join(resources_dir, file_name)
#         try:
#             with open(file_path, "r", encoding="utf-8") as f:
#                 knowledge += f.read() + "\n\n"
#         except FileNotFoundError:
#             print(f"Warning: Knowledge file not found at '{file_path}'")
    
#     if not knowledge:
#         print("CRITICAL: Knowledge base is empty. Make sure the .txt files are in a 'Resources' folder.")
        
#     return knowledge

# # Load the knowledge base once
# KNOWLEDGE_BASE = load_knowledge_base()

# def get_gemini_response(prompt: str, lang: str = "en") -> str:
#     """
#     Send prompt to Gemini model with the integrated knowledge base.
#     """
#     system_prompt = f"""
#     You are an expert AI assistant for the MahaDBT (Direct Benefit Transfer) portal, specifically designed to help students in India. Your name is "QuickLink DBT" assistant.

#     *Core Instructions:*
#     1.  *Language:* You MUST respond in the same language as the user's query. Supported languages are English, Hindi, and Marathi.
#     2.  *Information Source:* Your knowledge is STRICTLY LIMITED to the information provided in the following text. Do NOT use any external knowledge or make assumptions.
    
#     --- KNOWLEDGE BASE START ---
#     {KNOWLEDGE_BASE}
#     --- KNOWLEDGE BASE END ---

#     3.  *Role:* Your role is for AWARENESS and INFORMATION only. You provide guidance based on the knowledge base. You do not perform actions.
#     4.  *Redirection:* For any action-oriented queries (like checking status, applying for schemes, or updating details), you MUST guide the user to perform the action on the "QuickLink DBT" web platform.
#     5.  *Safety First:* NEVER ask for personal information. If a user provides it, politely decline and remind them not to share sensitive data.

#     *Example Scenarios:*
#     *   *User asks, "How can I check my DBT status?"*: Respond with, "You can easily check your DBT status on our QuickLink DBT platform. Just go to the 'Check DBT Status' section to verify it securely."
#     *   *User asks in Marathi, "माझे आधार बँक खात्याशी जोडलेले आहे, पण मला शिष्यवृत्ती मिळत नाही.":* Respond in Marathi, explaining the difference between linking and seeding, and then guide them to the 'Learn the Difference' section on the QuickLink DBT platform.

#     Now, answer the user's question based on these strict instructions.
#     """
#     try:
#         model = genai.GenerativeModel(GEMINI_MODEL)
#         lang_names = {"en": "English", "hi": "Hindi", "mr": "Marathi"}
#         final_prompt = f"{system_prompt}\n\nPlease respond in {lang_names.get(lang, 'English')}. User question: {prompt}"
#         response = model.generate_content(final_prompt)
#         return response.text
#     except Exception as e:
#         return f"Error: {str(e)}"

# llm_module/llm_integration/gemini_api.py
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-2.5-flash"

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# The entire knowledge base from the TXT files is now embedded here
KNOWLEDGE_BASE = """
--- START OF DBT_Complete_Guide.txt ---

Direct Benefit Transfer (DBT) Complete Guide

What is DBT (Direct Benefit Transfer)?

Direct Benefit Transfer (DBT) is a flagship initiative by the Government of India that enables the direct
transfer of government subsidies and benefits to the beneficiaries' bank accounts. This system eliminates intermediaries and ensures that benefits reach the intended recipients directly and transparently.

Key Features of DBT

1. Transparency
•  Direct transfer eliminates middlemen
•  Real-time tracking of transfers
•  Reduced leakage and corruption
•  Clear audit trail for all transactions

2. Efficiency

•  Faster processing of benefits
•  Reduced administrative costs
•  Simplified procedures
• 	24/7 availability for verification

3. Financial Inclusion

•  Promotes bank account ownership
•  Links beneficiaries to formal banking system
•  Encourages digital literacy
•  Supports cashless economy initiatives

Types of DBT Benefits

1. LPG Subsidy (PAHAL)

•  Direct transfer of LPG cooking gas subsidy
•  Largest cash transfer program globally
•  Covers domestic LPG consumers
•  Automatic credit to linked bank account

2. Fertilizer Subsidy

•  Direct payment to fertilizer companies
•  Benefits farmers through lower prices
•  Reduces black market sales
•  Ensures availability of quality fertilizers

3. Scholarship Programs

•  Educational scholarships for students
•  Merit-based and need-based transfers
•  Covers school and higher education
•  Direct credit to student accounts

4. MGNREGA Payments

•  Wages for rural employment scheme
•  Direct transfer to worker accounts
•  Eliminates delayed payments
•  Transparent wage distribution

5. Pension Schemes

•  Old age pension transfers
•  Widow and disability pensions
•  Regular monthly payments
•  Social security coverage

Eligibility Criteria

Basic Requirements
1. Aadhaar Number: Must have valid Aadhaar card
2. Bank Account: Active bank account in beneficiary's name
3. Mobile Number: Registered mobile for OTP verification
4. KYC Compliance: Complete Know Your Customer verification
5. Scheme-Specific: Meet individual program requirements

Document Requirements

•  Aadhaar Card (original and photocopy)
•  Bank passbook or statement
•  Mobile number for OTP
•  Address proof (if different from Aadhaar)
•  Income certificate (for means-tested schemes)
•  Caste certificate (if applicable)
•  Educational certificates (for scholarships)

DBT Verification Process

Step 1: Check Eligibility
• Visit official DBT portal or use WhatsApp bot
•  Enter basic details for initial screening
•  Verify scheme-specific requirements
•  Check document readiness

Step 2: Aadhaar-Bank Linking

• Visit bank branch with Aadhaar card
•  Fill bank-Aadhaar linking form
•  Provide biometric verification
•  Confirm mobile number registration

Step 3: Scheme Registration

•  Apply through designated channels
•  Submit required documents
•  Complete biometric authentication
•  Receive acknowledgment receipt

Step 4: Verification Status Check
•  Use last 4 digits of Aadhaar for verification
•  Check through multiple channels:
•  Official DBT website
•  WhatsApp chatbot
•  SMS service
•  Mobile app
•  Bank inquiry

Step 5: Benefit Disbursement

•  Automatic credit to linked account
•  SMS notification for transactions
•  Digital receipt generation
•  Real-time status updates

Benefits of DBT System

For Beneficiaries

1. Direct Payment: Money credited directly to bank account
2. Faster Processing: Reduced waiting time for benefits
3. Transparency: Track payment status in real-time
4. Reduced Harassment: No interaction with middlemen
5. Convenience: 24/7 status checking facility
6. Security: Biometric authentication prevents fraud
7. Financial Empowerment: Promotes banking habits

For Government
1. Cost Reduction: Lower administrative expenses
2. Leakage Prevention: Eliminates duplicate and ghost beneficiaries
3. Real-time Monitoring: Live tracking of fund utilization
4. Data Analytics: Better policy planning with usage data
5. Audit Trail: Complete transaction records
6. Targeted Delivery: Precise beneficiary identification

Common DBT Schemes in India

1. Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)

•  T6,000 annual income support to farmers
•  Direct credit to farmer bank accounts
•  Three installments of T2,000 each
•  Covers all landholding farmer families

2. Pradhan Mantri Jan Dhan Yojana

•  Financial inclusion through bank accounts
•  Zero balance accounts for poor
•  RuPay debit cards and insurance
•  Direct benefit transfer facility

3. Ayushman Bharat Digital Mission

•  Health insurance coverage
•  Cashless treatment facility
•  Digital health ID creation
•  Direct payment to hospitals

4. National Social Assistance Programme
•  Old age pension schemes
•  Widow pension benefits
•  Disability pension support
•  Direct monthly transfers

Technology Infrastructure

Aadhaar Integration
•  Unique 12-digit identification number
•  Biometric and demographic authentication
•  Central repository for verification
•  API integration for real-time checks

Banking Network

•  Core Banking Solutions (CBS)
•  Real-Time Gross Settlement (RTGS)
•  National Electronic Funds Transfer (NEFT)
•  Immediate Payment Service (IMPS)

Digital Platforms

•  DBT Mission portal
•  Mobile applications
•  WhatsApp chatbot integration
•  SMS gateway services
•  USSD services for feature phones

Security Measures

Data Protection

•  End-to-end encryption
•  Secure API communications
•  Regular security audits
•  Multi-factor authentication
•  Biometric verification

Fraud Prevention
•  Duplicate detection systems
•  Real-time monitoring alerts
•  Suspicious transaction flagging
•  Regular beneficiary verification
•  AI-powered anomaly detection

Success Stories

LPG Subsidy Reform
•	310 million beneficiaries enrolled
•	1,70,000+ crores savings achieved
•	99.99% Aadhaar seeding completed
•  Eliminated 3.86 crore duplicate connections

MGNREGA Digitization
• 	100% payments through DBT
•  Reduced payment delays significantly
•  Transparent wage calculation
•  Real-time job card updates

Future Roadmap

Upcoming Enhancements

1. Artificial Intelligence Integration
•  Predictive analytics for benefit delivery
•  Automated fraud detection
•  Personalized citizen services

2. Blockchain Technology
•  Immutable transaction records
•  Enhanced security protocols
•  Decentralized verification systems

3. Voice-Based Services
•  Regional language support
•  Voice-enabled status checking
•  Accessibility for illiterate users

4. loT Integration
•  Smart device connectivity
•  Automatic benefit triggers
•  Real-time consumption monitoring

Conclusion

DBT represents a paradigm shift in how government benefits are delivered to citizens. By leveraging
technology, it ensures transparency, reduces corruption, and empowers beneficiaries with direct access to their entitlements. The system continues to evolve, incorporating new technologies and expanding 
coverage to reach every eligible citizen.
The success of DBT lies in its simplicity for end-users while maintaining sophisticated backend processes. As India moves towards becoming a digitally empowered society, DBT serves as a cornerstone for 
efficient, transparent, and inclusive governance.

This document serves as a comprehensive guide to understanding the Direct Benefit Transfer system. For specific scheme information or technical support, please contact the relevant authorities or use our
WhatsApp chatbot service.

--- END OF DBT_Complete_Guide.txt ---

--- START OF DBT_FAQ.txt ---

DBT Frequently Asked Questions (FAQ) and Troubleshooting Guide

General DBT Questions

01: What is DBT and how does it work?
Answer: Direct Benefit Transfer (DBT) is a system where government subsidies and benefits are
transferred directly to beneficiaries' bank accounts. It uses Aadhaar authentication and eliminates intermediaries to ensure transparent and efficient delivery of benefits.

Q2: Do I need Aadhaar for DBT?
Answer: Yes, Aadhaar is mandatory for most DBT schemes. Your Aadhaar must be linked to your bank account for successful benefit transfer. Without Aadhaar, you cannot receive DBT benefits.

Q3: How do I check if I'm DBT verified?

Answer: You can check your DBT verification status by:

•  Using our WhatsApp chatbot with last 4 digits of Aadhaar
•  Visiting the official DBT portal
•  Sending SMS to designated numbers
•  Calling the DBT helpline
•  Checking with your bank

Q4: What does "DBT Verified" mean?
Answer: DBT Verified means:

•  Your Aadhaar is linked to your bank account
•  Your mobile number is registered and verified
•  Your bank account is active and operational
•  You're eligible to receive direct benefit transfers
•  All KYC requirements are completed

Q5: What does "Not DBT Verified" mean?

Answer: Not DBT Verified indicates:

•  Aadhaar-bank linking is incomplete
•  Mobile number not registered or verified
•  Bank account issues (inactive/closed)
•  Incomplete KYC documentation
•  Technical errors in the system

Account and Verification Issues

Q6: My Aadhaar is linked but I'm still not DBT verified. Why?
Answer: This could be due to:

•  Mobile number not updated in Aadhaar or bank
•  Bank account is inactive or frozen
•  Incomplete KYC at the bank
•  Pending verification by the bank
•  System processing delays

Solution: Visit your bank branch with Aadhaar card and request DBT verification status check.

Q7: How long does it take to become DBT verified after linking Aadhaar?
Answer: Typically 24-48 hours after successful Aadhaar-bank linking. However, it may take up to 	7 working days in some cases due to:

•  Bank processing time
•  System synchronization delays
•  High volume of requests
•  Technical maintenance periods

Q8: Can I have multiple bank accounts linked to Aadhaar for DBT?
Answer: While you can link multiple accounts to Aadhaar, only ONE account will be designated for DBT payments. You can change the primary DBT account through your bank or NPCI mapper.

Q9: I changed my bank account. How do I update DBT linking?

Answer: To update your DBT bank account:

1. Visit new bank branch with Aadhaar
2. Fill DBT account update form
3. Deactivate old account (if needed)
4. Wait 24-48 hours for system update
5. Verify new account status through checking methods

Q10: What if my Aadhaar mobile number is different from bank mobile number?

Answer: Both numbers should ideally be the same. If different:

•  Update mobile in Aadhaar first (visit Aadhaar center)
•  Then update in bank records
•  Or update bank mobile to match Aadhaar
•  Ensure OTP verification on updated number

Technical Issues

Q11: I'm getting "Invalid Aadhaar" error. What should 	I 	do?

Answer: This error occurs when:

•  Last 4 digits are entered incorrectly
•  Aadhaar number has issues in the system
•  Aadhaar is suspended or deactivated Solution:
•  Double-check the last 4 digits
•  Try after some time
•  Contact Aadhaar helpline: 1947
•  Visit nearest Aadhaar center

Q12: The system shows "Under Process" for weeks. Is this normal?

Answer: "Under Process" status beyond 7 days is unusual. Possible reasons:

•  Bank has not completed verification
•  Document verification pending
•  Technical glitches in the system
•  High processing volume

Solution: Contact your bank's DBT cell directly and request status escalation.

Q13: I get different status from different checking methods. Which is correct?
Answer: Different systems may have update delays. For most accurate status:

1. Check directly with your bank
2. Use official DBT portal
3. Cross-verify with multiple methods
4. Contact DBT helpline for confirmation

Scheme-Specific Questions

Q14: I'm DBT verified but not receiving LPG subsidy. Why?
Answer: LPG subsidy has additional requirements:

•  Must have active LPG connection
•  Connection should be in same name as bank account
•  Distributor must have updated records
•  No income tax returns filed (for some states)

Solution: Contact your LPG distributor and oil company customer care.

Q15: How do I check if I'm enrolled in specific DBT schemes?
Answer: Scheme enrollment is separate from general DBT verification:

•  Visit respective scheme websites
•  Use scheme-specific portals
•  Contact scheme administrators
•  Check with local government offices

Q16: Can I receive multiple DBT benefits in the same account?
Answer: Yes, you can receive benefits from multiple schemes in the same DBT-verified account. Each scheme has separate eligibility criteria and application processes.

Error Messages and Solutions

Error: "Account Not Found"
Cause: Bank account not properly linked or incorrect details Solution: Visit bank to verify account linking and update details

Error: "Mobile Number Not Verified"

Cause: OTP verification pending or mobile number issues Solution: Update mobile number in both
Aadhaar and bank records

Error: "KYC Incomplete"

Cause: Bank KYC documentation is incomplete Solution: Complete full KYC at your bank branch

Error: "System Temporarily Unavailable"
Cause: Server maintenance or high traffic Solution: Try after some time or use alternative checking methods

Error: "Duplicate Entry Found"
Cause: Multiple entries for same Aadhaar in system Solution: Contact DBT helpline to resolve duplicate entries

Status Meanings Explained

"Active" Status
•  Account is fully DBT verified
•  Ready to receive benefit transfers
•  All linking processes completed
•  No action required from your side

"Inactive" Status
•  Account linking issues present
•  May require bank visit for activation
•  Possible KYC or documentation gaps
•  Benefits may be temporarily suspended

"Pending" Status

•  Verification process is ongoing
•  Bank processing your request
•  Wait for 2-3 working days
•  Contact bank if prolonged

"Rejected" Status
•  Application or linking was unsuccessful
•  Usually due to document issues
•  Requires fresh application or correction
•  Contact bank for specific rejection reasons

"Suspended" Status

•  Temporary suspension due to issues
•  May be due to suspicious activity
•  Requires immediate attention
•  Contact bank and DBT helpline

Troubleshooting Steps

Step 1: Basic Verification
•  Confirm last 4 digits of Aadhaar
•  Check bank account number accuracy
•  Verify mobile number in records
•  Ensure account is active

Step 2: System Checks
•  Try multiple verification methods
•  Check at different times of day
•  Clear browser cache if using online
•  Use different devices/networks

Step 3: Documentation Review

•  Verify Aadhaar card validity
•  Check bank account documents
•  Ensure KYC is complete
•  Review linking forms submitted

Step 4: Official Contacts

•  Contact bank DBT cell
•  Call DBT helpline: 1800-11-6446
•  Visit nearest CSC center
•  Escalate through official channels

Prevention Tips

Regular Monitoring

•  Check DBT status monthly
•  Monitor bank account for transfers
•  Keep mobile number updated
•  Maintain active bank account

Document Management
•  Keep Aadhaar and bank documents updated
•  Regularly update mobile numbers
•  Complete KYC requirements on time
•  Maintain copies of all forms

Proactive Measures
•  Link Aadhaar immediately upon getting 	new account
•  Update details promptly when changed
•  Use official channels for all processes
•  Stay informed about scheme updates
Contact Information for Support DBT Mission
•  Website: dbtmission.gov.in
•  Helpline: 	1800-11-6446
•  Email: support@dbtmission.gov.in

UIDAI (Aadhaar)

•  Website: uidai.gov.in
•  Helpline: 	1947
•  Email: help@uidai.gov.in

NPCI (Banking Integration)

•  Website: npci.org.in
•  Customer Care: 1800-1201-740

Your Bank's DBT Cell

Contact your bank's customer care for specific account-related issues and DBT verification support.

This FAQ covers common queries about DBT verification and troubleshooting. For personalized assistance, use our WhatsApp chatbot or contact the relevant helplines.

--- END OF DBT_FAQ.txt ---

--- START OF DBT_Security_Support.txt ---

DBT Security, Privacy and Support Guide

Data Security and Privacy

Your Data Protection Rights

What Information We Collect

When using DBT verification services, we handle:

•  Last 4 digits of Aadhaar (for verification purposes only)
•  Bank account status (verification status only, not balance)
•  Mobile number (for OTP and notifications)
•  Transaction history (for benefit delivery tracking)
•  Scheme enrollment data (for eligibility verification) What We Do NOT Collect
•  Complete Aadhaar numbers
•  Bank account balances
•  Personal financial details beyond DBT status
•  Sensitive biometric data
•  Passwords or PINs
•  Full bank account numbers

Data Security Measures

Technical Safeguards

1. End-to-End Encryption
•  All data transmission is encrypted using industry-standard protocols
•  No plaintext storage of sensitive information
•  Secure API communications with government databases

2. Access Controls
•  Multi-factor authentication for system access
•  Role-based permissions for different user types
•  Regular access audits and monitoring

3. Data Minimization
•  Only collect data necessary for verification
•  Automatic deletion of temporary data
•  Minimal data retention periods

4. Regular Security Audits
•  Quarterly penetration testing
•  Continuous vulnerability assessments
•  Compliance with government security standards

Physical Security

•  Secure data centers with 24/7 monitoring
•  Biometric access controls for server rooms
•  Redundant backup systems across multiple locations
•  Environmental controls and fire suppression systems

Privacy Protection Policies

Data Usage Principles

1. Purpose Limitation: Data used only for DBT verification
2. Consent-Based Processing: Explicit user consent for data processing
3. Transparency: Clear communication about data handling
4. User Control: Options to modify or delete data
5. Legal Compliance: Adherence to Indian data protection laws Third-Party Sharing
•  Government Agencies: Only with authorized entities for verification
•  Banks: Limited to verification status updates
•  No Commercial Use: Data never shared for marketing or commercial purposes
•  Legal Requirements: Sharing only when legally mandated

Safe Usage Guidelines

For Users

1. Never Share Complete Aadhaar

•  Only provide last 4 digits when requested
•  Never share full Aadhaar over phone/chat
•  Be cautious of phishing attempts

2. Verify Official Channels
•  Use only official WhatsApp numbers
•  Check website URLs carefully
•  Avoid clicking suspicious links

3. Protect Your Devices
•  Use screen locks on mobile phones
•  Log out from shared devices
•  Keep apps updated

4. Monitor Your Accounts
•  Regularly check bank statements
•  Report unauthorized transactions immediately
•  Keep contact information updated

Red Flags to Watch For

•  Requests for complete Aadhaar numbers
•  Demands for bank passwords or PINs
•  Unofficial phone numbers or websites
•  Pressure to share sensitive information quickly
•  Requests for payment to check DBT status

Customer Support Services

Phone Support

•  DBT Helpline: 1800-11-6446 (Toll-Free)
•  Operating Hours: 9:00 AM to 6:00 PM (Monday to Saturday)
•  Languages: English, Hindi, and major regional languages
•  Average Wait Time: Less than 3 minutes
•  Resolution Rate: 85% issues resolved on first call Web Portal Support
•  Self-Service Options: Check status anytime online
•  Knowledge Base: Comprehensive FAQ and guides
•  Ticket System: Submit detailed queries with tracking
•  Live Chat: Real-time assistance during business hours Email Support
•  General Queries: support@dbtverification.govin
•  Technical Issues: technical@dbtverification.gov.in
•  Complaints: complaints@dbtverification.gov.in
•  Response Time: Within 24 hours for standard queries

Support Categories and Services

Verification Support

1. Status Checking
•  Real-time verification status
•  Historical status tracking
•  Multiple verification methods

2. Account Linking Issues
•  Aadhaar-bank linking guidance
•  Mobile number update assistance
•  KYC completion support

3. Technical Troubleshooting
•  Error message explanations
•  System connectivity issues
•  Platform-specific problems

Educational Support

1. DBT Awareness Programs
•  How DBT works and benefits
•  Step-by-step registration guides
•  Scheme-specific information

2. Digital Literacy
•  Using online verification tools
•  Mobile app navigation
•  Security best practices

3. Language Support
•  Regional language assistance
•  Audio guidance for illiterate users
•  Visual aids and infographics

Escalation Procedures

Level 1: Self-Service

•  Use WhatsApp chatbot for instant answers
•  Check online FAQ and knowledge base
•  Try multiple verification methods
•  Review troubleshooting guides

Level 2: Direct Support

•  Contact phone helpline for personal assistance
•  Use email support for detailed queries
•  Submit tickets through web portal
•  Use live chat for immediate help

Level 3: Specialized Support

•  Technical team for complex system issues
•  Bank liaison team for account problems
•  Scheme administrators for enrollment issues
•  Senior support managers for escalated cases

Level 4: Management Escalation

•  Regional DBT coordinators
•  State-level DBT mission heads
•  National DBT mission leadership
•  Ombudsman for unresolved complaints

Service Level Agreements (SLAs)

Response Times

•  WhatsApp Bot: Instant (24/7)
•  Phone Support: Average 2-3 minutes wait
•  Email Queries: Within 24 hours
•  Technical Issues: Within 48 hours
•  Complaints: Within 72 hours Resolution Targets
•  Simple Queries: 80% resolved immediately
•  Verification Issues: 90% resolved within 2 working days
•  Technical Problems: 95% resolved within 5 working days
•  Complex Cases: 100% resolved within 15 working days

Quality Assurance

Service Monitoring

1. Call Recording: All phone interactions recorded for quality
2. Customer Feedback: Regular satisfaction surveys
3. Performance Metrics: Real-time dashboard monitoring
4. Continuous Improvement: Monthly service reviews

Training Programs

1. Regular Training: Support staff updated on latest procedures
2. Language Skills: Multilingual communication training
3. Technical Knowledge: Regular updates on system changes
4. Customer Service: Soft skills and empathy training

Complaint Resolution Process

Filing Complaints

1. Online Portal: Submit detailed complaints with attachments
2. Email: Send complaints to dedicated email address
3. Phone: Lodge complaints through helpline
4. In-Person: Visit designated government offices Complaint Categories
•  Service quality issues
•  Technical system problems
•  Data privacy concerns
•  Incorrect verification status
•  Staff behavior complaints

Resolution Timeline

•  Acknowledgment: Within 2 working days
•  Investigation: 5-7 working days
•  Resolution: Within 15 working days
•  Follow-up: Customer satisfaction confirmation

Emergency Support

Critical Issues

•  Urgent Benefit Delays: Priority support channel
•  Security Breaches: Immediate response team
•  System Outages: Real-time status updates
•  Data Concerns: Direct escalation to security team Emergency Contacts
• 	24/7 Emergency Line: 1800-DBT-HELP
•  WhatsApp Emergency: Send "URGENT" to bot
•  Email Emergency: emergency@dbtverification.gov.in
•  Social Media: @DBTMissionIndia (Twitter)

Feedback and Improvement

Customer Feedback Channels

1. Post-Interaction Surveys: After each support contact
2. Annual Satisfaction Survey: Comprehensive service review
3. Suggestion Box: Ideas for service improvement
4. Focus Groups: Selected user feedback sessions Service Improvements
•  Regular Updates: System enhancements based on feedback
•  New Features: User-requested functionality additions
•  Process Optimization: Streamlined procedures
•  Technology Upgrades: Latest tools for better service

Additional Resources

Official Information Sources

•  DBT Mission Website: dbtmission.gov.in
•  Aadhaar Portal: uidai.gov.in
•  Banking Information: rbi.org.in
•  Consumer Rights: consumerhelpline.gov.in Educational Materials
•  Video Tutorials: Step-by-step visual guides
•  Infographics: Easy-to-understand visual information
•  Brochures: Downloadable information sheets
•  FAQs: Comprehensive question-answer database

Community Support

•  Local CSC Centers: In-person assistance
•  Government Offices: Direct support at counters
•  Bank Branches: Account-specific help
•  NGO Partners: Community outreach programs

Your security and satisfaction are our priorities. We continuously work to improve our services while
maintaining the highest standards of data protection and customer support. For any immediate assistance, please use our 24/7 WhatsApp chatbot service.

--- END OF DBT_Security_Support.txt ---
"""

def get_gemini_response(prompt: str, lang: str = "en") -> str:
    """
    Sends prompt to Gemini model with the integrated knowledge base.
    """
    system_prompt = f"""
    You are an expert AI assistant for the MahaDBT (Direct Benefit Transfer) portal, specifically designed to help students in India. Your name is "QuickLink DBT" assistant.

    *Core Instructions:*
    1.  *Language:* You MUST respond in the same language as the user's query. Supported languages are English, Hindi, and Marathi.
    2.  *Information Source:* Your knowledge is STRICTLY LIMITED to the information provided in the following text. Do NOT use any external knowledge or make assumptions.

    --- KNOWLEDGE BASE START ---
    {KNOWLEDGE_BASE}
    --- KNOWLEDGE BASE END ---

    3.  *Role:* Your role is for AWARENESS and INFORMATION only. You provide guidance based on the knowledge base. You do not perform actions.
    4.  *Redirection:* For any action-oriented queries (like checking status, applying for schemes, or updating details), you MUST guide the user to perform the action on the "QuickLink DBT" web platform.
    5.  *Safety First:* NEVER ask for personal information. If a user provides it, politely decline and remind them not to share sensitive data.

    *Example Scenarios:*
    *   *User asks, "How can I check my DBT status?"*: Respond with, "You can easily check your DBT status on our QuickLink DBT platform. Just go to the 'Check DBT Status' section to verify it securely."
    *   *User asks in Marathi, "माझे आधार बँक खात्याशी जोडलेले आहे, पण मला शिष्यवृत्ती मिळत नाही.":* Respond in Marathi, explaining the difference between linking and seeding, and then guide them to the 'Learn the Difference' section on the QuickLink DBT platform.

    Now, answer the user's question based on these strict instructions.
    """
    try:
        model = genai.GenerativeModel(GEMINI_MODEL)
        lang_names = {"en": "English", "hi": "Hindi", "mr": "Marathi"}
        final_prompt = f"{system_prompt}\n\nPlease respond in {lang_names.get(lang, 'English')}. User question: {prompt}"
        
        response = model.generate_content(final_prompt)
        return response.text
        
    except Exception as e:
        print(f"Error communicating with Gemini: {e}")
        return "I'm sorry, I'm having trouble connecting to my brain right now. Please try again in a moment."