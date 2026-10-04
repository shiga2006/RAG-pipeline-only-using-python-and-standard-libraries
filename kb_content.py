"""Source text for the sample knowledge base (fictional company: Zenvora Technologies).
make_kb.py turns this into PDF / DOCX / TXT / PPTX files inside kb/.
Edit or extend this file to build your own KB (keep facts specific so retrieval is testable)."""

# filename -> (document title, [(section heading, section text), ...])
DOCS = {
    "leave_policy.pdf": ("Zenvora Leave Policy", [
        ("Annual Leave",
         "Full-time employees are entitled to 18 days of paid annual leave per calendar year. "
         "Leave accrues at 1.5 days per month from the date of joining. Employees must submit leave "
         "requests in the HR portal at least 5 working days in advance for absences of 3 days or more."),
        ("Carry Forward",
         "Up to 8 unused annual leave days can be carried forward to the next calendar year. "
         "Carried-forward days expire on 31 March. Leave encashment is not available except at separation."),
        ("Sick Leave",
         "Employees receive 10 days of paid sick leave per year. Sick leave cannot be carried forward. "
         "Employees must inform their manager before the start of the working day on which they are unwell."),
        ("Medical Documentation",
         "A medical certificate from a registered doctor is required if sick leave exceeds 2 consecutive days. "
         "Certificates must be uploaded to the HR portal within 3 working days of returning to work."),
        ("Maternity and Paternity Leave",
         "Female employees are entitled to 26 weeks of paid maternity leave. Male employees receive 10 days of "
         "paid paternity leave, to be taken within 6 months of the child's birth."),
        ("Public Holidays",
         "The company observes 12 public holidays per year. The holiday list is published every December on "
         "the intranet. Employees who work on a public holiday receive a compensatory day off."),
    ]),
    "expense_policy.pdf": ("Zenvora Travel and Expense Policy", [
        ("Travel Reimbursement",
         "Business travel must be approved by the reporting manager before booking. Economy class is permitted "
         "for flights under 6 hours. Hotel stays are reimbursed up to INR 6,000 per night in metro cities and "
         "INR 4,000 per night elsewhere."),
        ("Meal Allowance",
         "A meal allowance of INR 1,200 per day applies during business travel. Alcohol is never reimbursable."),
        ("Claim Submission",
         "Expense claims must be submitted within 30 days of the expense through the Finance portal with original "
         "receipts attached. Claims above INR 25,000 need approval from the department head. Reimbursement is "
         "processed within 10 working days of approval."),
        ("Company Credit Card",
         "Company credit cards are issued only to employees at grade L5 and above. Lost or stolen cards must be "
         "reported to the Finance team immediately so the card can be blocked."),
    ]),
    "code_of_conduct.docx": ("Zenvora Code of Conduct", [
        ("Workplace Behaviour",
         "All employees must treat colleagues, clients and vendors with respect. Harassment, discrimination and "
         "bullying are strictly prohibited and may lead to termination of employment."),
        ("Reporting Concerns",
         "Concerns about misconduct can be reported to the Ethics Committee at ethics@zenvora.example or through "
         "the anonymous helpline 1800-555-0142. Retaliation against anyone who reports in good faith is prohibited. "
         "The Ethics Committee acknowledges every report within 48 hours."),
        ("Conflict of Interest",
         "Employees must disclose any financial interest in a vendor, competitor or client to HR. Gifts worth more "
         "than INR 2,000 must be declined or declared."),
        ("Dress Code",
         "Business casual is the standard dress code on weekdays. Casual wear is allowed on Fridays. Employees "
         "meeting clients must wear formal attire."),
        ("Company Property and Data",
         "Laptops, access cards and other company property remain the property of Zenvora. Loss, theft or misuse "
         "of company property, or any suspected data breach, must be reported to the Ethics Committee and the IT "
         "Security team without delay. Employees are accountable for damage caused by negligence."),
        ("Confidentiality",
         "Client and company information must not be shared outside the organisation without written approval. "
         "This obligation continues after employment ends."),
    ]),
    "remote_work_policy.docx": ("Zenvora Remote and Hybrid Work Policy", [
        ("Eligibility",
         "Employees who have completed 6 months of service may apply for hybrid work. Hybrid employees work from "
         "the office at least 3 days a week."),
        ("Approval Process",
         "Remote work arrangements must be approved by the reporting manager and recorded in the HR portal. "
         "Fully remote roles can be approved only by the department head."),
        ("Home Office Setup",
         "The company provides a one-time home office allowance of INR 15,000 for approved remote employees. "
         "A stable internet connection of at least 25 Mbps is required."),
        ("Working Hours",
         "Core hours are 10:00 to 16:00 IST, during which remote employees must be reachable on Teams. "
         "Overtime must be pre-approved by the manager."),
        ("Security While Remote",
         "Remote employees must connect to the company VPN when accessing internal systems. Public Wi-Fi may only "
         "be used with the VPN enabled."),
    ]),
    "it_security.txt": ("Zenvora IT Security Guidelines", [
        ("Passwords",
         "Passwords must be at least 12 characters and include upper case, lower case, a number and a symbol. "
         "Passwords expire every 90 days and the last 5 passwords cannot be reused. Never share your password "
         "with anyone, including IT staff."),
        ("Multi-Factor Authentication",
         "MFA is mandatory for email, VPN and the HR portal. Use the Zenvora Authenticator app. SMS codes are "
         "not accepted."),
        ("VPN Usage",
         "The company VPN must be used when accessing internal systems from outside the office. Connect using the "
         "GlobalProtect client with your corporate credentials. VPN sessions disconnect after 30 minutes of "
         "inactivity."),
        ("Laptop and Device Rules",
         "Company laptops must have disk encryption enabled and may not be used by family members. Installing "
         "unapproved software is prohibited. If a laptop is lost or stolen, report it to the IT helpdesk at "
         "helpdesk@zenvora.example or extension 4040 within 2 hours so the device can be remotely wiped."),
        ("Reporting Security Incidents",
         "Phishing emails, malware alerts and suspected data breaches must be reported to security@zenvora.example "
         "immediately. Do not delete the suspicious email; use the Report Phishing button. The Security team "
         "responds within 1 hour."),
        ("Email and Data Handling",
         "Confidential data must not be sent to personal email accounts. USB storage devices are blocked by default."),
    ]),
    "benefits_faq.txt": ("Zenvora Benefits FAQ", [
        ("Health Insurance",
         "All employees are covered under a group health insurance policy of INR 5,00,000 from the first day of "
         "employment. Spouse, children and parents can be added during enrollment at a nominal premium."),
        ("Provident Fund",
         "Both the employee and the employer contribute 12 percent of basic salary to the provident fund."),
        ("Learning Allowance",
         "Each employee gets INR 30,000 per year for courses and certifications. Courses must be relevant to the "
         "role and approved by the manager."),
        ("Employee Referral Bonus",
         "A referral bonus of INR 25,000 is paid after the referred candidate completes 3 months in the company."),
        ("Salary Payment",
         "Salaries are credited on the last working day of each month."),
        ("Probation and Notice",
         "The probation period is 3 months. After confirmation the notice period is 60 days."),
    ]),
    # PPTX: one slide per entry; the text is a list of bullets
    "onboarding.pptx": ("Zenvora Onboarding", [
        ("Welcome to Zenvora",
         ["Orientation begins at 9:30 AM on your first day",
          "Meet your buddy and your reporting manager",
          "Collect your laptop and access card from IT"]),
        ("Week 1 Schedule",
         ["Day 1: HR induction and laptop setup",
          "Day 2: IT security training (mandatory)",
          "Day 3: Meet your team and review role goals",
          "Day 4: Code of conduct session",
          "Day 5: Review with manager and 30-day plan"]),
        ("Benefits Enrollment",
         ["Enroll in health insurance within 15 days of joining",
          "Submit nominee details for the provident fund",
          "Add dependants through the HR portal"]),
        ("Complete Within 30 Days",
         ["Complete mandatory IT security and ethics e-learning",
          "Set up MFA on email, VPN and the HR portal",
          "Submit all joining documents to HR"]),
        ("Who to Contact",
         ["HR helpdesk: hr@zenvora.example",
          "IT helpdesk: extension 4040",
          "Finance queries: finance@zenvora.example"]),
    ]),
}
