# Test results

Chunks: 42 | mode: hybrid | k=3

| # | Type | Query | Verdict | Top-1 (source, score) |
|---|---|---|---|---|
| 1 | direct | How many days of annual leave do I get? | **PASS** | leave_policy.pdf, 0.62 |
| 2 | direct | What is the VPN policy? | **PASS** | it_security.txt, 0.30 |
| 3 | direct | What is the dress code on Fridays? | **PASS** | code_of_conduct.docx, 0.55 |
| 4 | direct | When are salaries credited? | **PASS** | benefits_faq.txt, 0.70 |
| 5 | direct | What happens on day 2 of the first week? | **PASS** | onboarding.pptx, 0.29 |
| 6 | direct | How much is the hotel reimbursement in metro cities? | **PASS** | expense_policy.pdf, 0.34 |
| 7 | direct | How many weeks of maternity leave are given? | **PASS** | leave_policy.pdf, 0.53 |
| 8 | paraphrase | How much time off am I allowed each year? | **PASS** | leave_policy.pdf, 0.30 |
| 9 | paraphrase | Can I work from home? | **PASS** | remote_work_policy.docx, 0.39 |
| 10 | paraphrase | How often do I have to change my password? | **PASS** | it_security.txt, 0.72 |
| 11 | paraphrase | Who do I contact if I feel harassed at work? | **PASS** | code_of_conduct.docx, 0.27 |
| 12 | paraphrase | What is the staff referral reward amount? | **PASS** | benefits_faq.txt, 0.55 |
| 13 | no-match | What is the company's stock price? | **PASS** | none returned |
| 14 | no-match | Best pizza places in Chennai | **PASS** | none returned |
| 15 | no-match | How do I request a company car? | **PASS** | none returned |
| 16 | multi-chunk | What should I do if I lose my laptop? | **PARTIAL** | it_security.txt, 0.39 |
| 17 | multi-chunk | Explain sick leave and the documentation required | **PASS** | leave_policy.pdf, 0.41 |
| 18 | multi-chunk | How do I report a data breach? | **PASS** | code_of_conduct.docx, 0.41 |
| 19 | multi-chunk | Rules for connecting from public Wi-Fi while working remotely | **PARTIAL** | remote_work_policy.docx, 0.40 |
| 20 | multi-chunk | What do I need to finish in my first month? | **FAIL** | none returned |

Summary: {'PASS': 17, 'PARTIAL': 2, 'FAIL': 1}

## Retrieved chunks

### 1. How many days of annual leave do I get?  (direct, PASS)
1. `leave_policy.pdf` chunk 0 (score 0.617): Full-time employees are entitled to 18 days of paid annual leave per calendar year. Leave accrues at 1.5 days per month from the date of joining.
2. `leave_policy.pdf` chunk 1 (score 0.516): Leave accrues at 1.5 days per month from the date of joining. Employees must submit leave requests in the HR portal at least 5 working days in advance for absences of 3 days or more.
3. `leave_policy.pdf` chunk 2 (score 0.376): Up to 8 unused annual leave days can be carried forward to the next calendar year. Carried-forward days expire on 31 March. Leave encashment is not available except at separation.

### 2. What is the VPN policy?  (direct, PASS)
1. `it_security.txt` chunk 2 (score 0.296): The company VPN must be used when accessing internal systems from outside the office. Connect using the GlobalProtect client with your corporate credentials. VPN sessions disconnect after 30 minutes of inactivity.

### 3. What is the dress code on Fridays?  (direct, PASS)
1. `code_of_conduct.docx` chunk 4 (score 0.547): Business casual is the standard dress code on weekdays. Casual wear is allowed on Fridays. Employees meeting clients must wear formal attire.

### 4. When are salaries credited?  (direct, PASS)
1. `benefits_faq.txt` chunk 4 (score 0.700): Salaries are credited on the last working day of each month.
2. `expense_policy.pdf` chunk 3 (score 0.262): Company credit cards are issued only to employees at grade L5 and above. Lost or stolen cards must be reported to the Finance team immediately so the card can be blocked.

### 5. What happens on day 2 of the first week?  (direct, PASS)
1. `onboarding.pptx` chunk 1 (score 0.287): Day 1: HR induction and laptop setup. Day 2: IT security training (mandatory). Day 3: Meet your team and review role goals. Day 4: Code of conduct session. Day 5: Review with manager and 30-day plan.

### 6. How much is the hotel reimbursement in metro cities?  (direct, PASS)
1. `expense_policy.pdf` chunk 0 (score 0.337): Business travel must be approved by the reporting manager before booking. Economy class is permitted for flights under 6 hours. Hotel stays are reimbursed up to INR 6,000 per night in metro cities and INR 4,000 per night elsewhere.

### 7. How many weeks of maternity leave are given?  (direct, PASS)
1. `leave_policy.pdf` chunk 5 (score 0.527): Female employees are entitled to 26 weeks of paid maternity leave. Male employees receive 10 days of paid paternity leave, to be taken within 6 months of the child's birth.

### 8. How much time off am I allowed each year?  (paraphrase, PASS)
1. `leave_policy.pdf` chunk 0 (score 0.297): Full-time employees are entitled to 18 days of paid annual leave per calendar year. Leave accrues at 1.5 days per month from the date of joining.

### 9. Can I work from home?  (paraphrase, PASS)
1. `remote_work_policy.docx` chunk 0 (score 0.386): Employees who have completed 6 months of service may apply for hybrid work. Hybrid employees work from the office at least 3 days a week.
2. `remote_work_policy.docx` chunk 2 (score 0.312): The company provides a one-time home office allowance of INR 15,000 for approved remote employees. A stable internet connection of at least 25 Mbps is required.

### 10. How often do I have to change my password?  (paraphrase, PASS)
1. `it_security.txt` chunk 0 (score 0.718): Passwords must be at least 12 characters and include upper case, lower case, a number and a symbol. Passwords expire every 90 days and the last 5 passwords cannot be reused. Never share your password with anyone, including IT staff.

### 11. Who do I contact if I feel harassed at work?  (paraphrase, PASS)
1. `code_of_conduct.docx` chunk 2 (score 0.274): Retaliation against anyone who reports in good faith is prohibited. The Ethics Committee acknowledges every report within 48 hours.
2. `code_of_conduct.docx` chunk 1 (score 0.271): Concerns about misconduct can be reported to the Ethics Committee at ethics@zenvora.example or through the anonymous helpline 1800-555-0142. Retaliation against anyone who reports in good faith is prohibited.

### 12. What is the staff referral reward amount?  (paraphrase, PASS)
1. `benefits_faq.txt` chunk 3 (score 0.554): A referral bonus of INR 25,000 is paid after the referred candidate completes 3 months in the company.

### 13. What is the company's stock price?  (no-match, PASS)
*No chunk above threshold.*

### 14. Best pizza places in Chennai  (no-match, PASS)
*No chunk above threshold.*

### 15. How do I request a company car?  (no-match, PASS)
*No chunk above threshold.*

### 16. What should I do if I lose my laptop?  (multi-chunk, PARTIAL)
1. `it_security.txt` chunk 4 (score 0.389): Installing unapproved software is prohibited. If a laptop is lost or stolen, report it to the IT helpdesk at helpdesk@zenvora.example or extension 4040 within 2 hours so the device can be remotely wiped.
2. `it_security.txt` chunk 3 (score 0.259): Company laptops must have disk encryption enabled and may not be used by family members. Installing unapproved software is prohibited.

### 17. Explain sick leave and the documentation required  (multi-chunk, PASS)
1. `leave_policy.pdf` chunk 3 (score 0.408): Employees receive 10 days of paid sick leave per year. Sick leave cannot be carried forward. Employees must inform their manager before the start of the working day on which they are unwell.
2. `leave_policy.pdf` chunk 4 (score 0.377): A medical certificate from a registered doctor is required if sick leave exceeds 2 consecutive days. Certificates must be uploaded to the HR portal within 3 working days of returning to work.

### 18. How do I report a data breach?  (multi-chunk, PASS)
1. `code_of_conduct.docx` chunk 6 (score 0.411): Loss, theft or misuse of company property, or any suspected data breach, must be reported to the Ethics Committee and the IT Security team without delay. Employees are accountable for damage caused by negligence.
2. `it_security.txt` chunk 5 (score 0.361): Phishing emails, malware alerts and suspected data breaches must be reported to security@zenvora.example immediately. Do not delete the suspicious email; use the Report Phishing button. The Security team responds within 1 hour.
3. `code_of_conduct.docx` chunk 5 (score 0.344): Laptops, access cards and other company property remain the property of Zenvora. Loss, theft or misuse of company property, or any suspected data breach, must be reported to the Ethics Committee and the IT Security team without delay.

### 19. Rules for connecting from public Wi-Fi while working remotely  (multi-chunk, PARTIAL)
1. `remote_work_policy.docx` chunk 4 (score 0.404): Remote employees must connect to the company VPN when accessing internal systems. Public Wi-Fi may only be used with the VPN enabled.

### 20. What do I need to finish in my first month?  (multi-chunk, FAIL)
*No chunk above threshold.*
