# import unittest
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time
# import os
# import requests

# class TestResumeAnalyzerBlackBox(unittest.TestCase):
    
#     @classmethod
#     def setUpClass(cls):
#         # Set up headless Chrome driver
#         chrome_options = Options()
#         chrome_options.add_argument("--headless")
#         chrome_options.add_argument("--no-sandbox")
#         chrome_options.add_argument("--disable-dev-shm-usage")
        
#         # Assuming Streamlit app is running on port 8501
#         cls.base_url = "http://localhost:8501"
#         cls.driver = webdriver.Chrome(options=chrome_options)
#         cls.wait = WebDriverWait(cls.driver, 10)
        
#         # Create test resume file if needed
#         cls.test_resume_path = os.path.join(os.getcwd(), "test_resume.pdf")
#         if not os.path.exists(cls.test_resume_path):
#             # Create a simple PDF for testing
#             cls._create_test_pdf()
    
#     @classmethod
#     def tearDownClass(cls):
#         cls.driver.quit()
        
#         # Clean up test files
#         if os.path.exists(cls.test_resume_path):
#             os.remove(cls.test_resume_path)
    
#     @classmethod
#     def _create_test_pdf(cls):
#         # This is a placeholder. In a real test, you would create an actual PDF.
#         # For this example, we'll just touch the file
#         with open(cls.test_resume_path, 'w') as f:
#             f.write("Test PDF content")
    
#     def test_01_application_loads(self):
#         """Test if the Streamlit application loads successfully"""
#         try:
#             response = requests.get(self.base_url)
#             self.assertEqual(response.status_code, 200)
            
#             # Navigate to the page
#             self.driver.get(self.base_url)
            
#             # Wait for title to appear
#             title = self.wait.until(
#                 EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Automated Resume Analyzer')]"))
#             )
#             self.assertIsNotNone(title)
            
#             # Check if the sidebar navigation exists
#             sidebar = self.wait.until(
#                 EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'sidebar')]"))
#             )
#             self.assertIsNotNone(sidebar)
            
#             print("✅ Test 01: Application loads successfully")
#         except Exception as e:
#             self.fail(f"Application did not load correctly: {str(e)}")
    
#     def test_02_resume_upload(self):
#         """Test the resume upload functionality"""
#         try:
#             # Navigate to the page
#             self.driver.get(self.base_url)
            
#             # Click on Upload Resume in the sidebar if needed
#             upload_option = self.wait.until(
#                 EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Upload Resume')]"))
#             )
#             upload_option.click()
            
#             # Select "Yes" for apply directly
#             yes_radio = self.wait.until(
#                 EC.element_to_be_clickable((By.XPATH, "//label[contains(text(), 'Yes')]"))
#             )
#             yes_radio.click()
            
#             # Upload a file
#             upload_input = self.wait.until(
#                 EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
#             )
#             upload_input.send_keys(self.test_resume_path)
            
#             # Wait for processing to complete
#             time.sleep(5)  # Simple wait for processing
            
#             # Check if form fields appeared
#             personal_info = self.wait.until(
#                 EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Personal Information')]"))
#             )
#             self.assertIsNotNone(personal_info)
            
#             print("✅ Test 02: Resume upload functionality works")
#         except Exception as e:
#             self.fail(f"Resume upload functionality failed: {str(e)}")
    
#     def test_03_form_filling(self):
#         """Test the form filling and data saving"""
#         try:
#             # Navigate to the page and upload resume first
#             self.test_02_resume_upload()
            
#             # Fill in some sample data
#             name_field = self.wait.until(
#                 EC.presence_of_element_located((By.XPATH, "//label[contains(text(), 'Name')]/../input"))
#             )
#             name_field.clear()
#             name_field.send_keys("John Doe")
            
#             email_field = self.wait.until(
#                 EC.presence_of_element_located((By.XPATH, "//label[contains(text(), 'Email')]/../input"))
#             )
#             email_field.clear()
#             email_field.send_keys("john.doe@example.com")
            
#             # Open skills section if not already open
#             try:
#                 skills_header = self.wait.until(
#                     EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Skills')]"))
#                 )
#                 skills_header.click()
#             except:
#                 pass  # Section might already be open
            
#             # Add skills
#             skills_field = self.wait.until(
#                 EC.presence_of_element_located((By.XPATH, "//label[contains(text(), 'Skills')]/../textarea"))
#             )
#             skills_field.clear()
#             skills_field.send_keys("Python, JavaScript, Data Analysis, Machine Learning")
            
#             # Click save button
#             save_button = self.wait.until(
#                 EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Save Resume Data')]"))
#             )
#             save_button.click()
            
#             # Wait for success message
#             success_message = self.wait.until(
#                 EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Data saved')]"))
#             )
#             self.assertIsNotNone(success_message)
            
#             print("✅ Test 03: Form filling and data saving works")
#         except Exception as e:
#             self.fail(f"Form filling and data saving failed: {str(e)}")
    
#     def test_04_job_search_functionality(self):
#         """Test the job search functionality"""
#         try:
#             # Navigate to the page
#             self.driver.get(self.base_url)
            
#             # Click on Job Search in the sidebar
#             job_search_option = self.wait.until(
#                 EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Job Search')]"))
#             )
#             job_search_option.click()
            
#             # Click Find Relevant Jobs button
#             find_jobs_button = self.wait.until(
#                 EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Find Relevant Jobs')]"))
#             )
#             find_jobs_button.click()
            
#             # Wait for job results
#             time.sleep(10)  # Longer wait for job processing
            
#             # Check if job listings appeared
#             try:
#                 job_listings = self.wait.until(
#                     EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Recommended Jobs')]"))
#                 )
#                 self.assertIsNotNone(job_listings)
                
#                 # Try to find at least one job link
#                 job_link = self.driver.find_element(By.XPATH, "//a[contains(text(), 'Apply Here')]")
#                 self.assertIsNotNone(job_link)
                
#                 print("✅ Test 04: Job search functionality works")
#             except Exception as e:
#                 self.fail(f"Job listings not displayed: {str(e)}")
#         except Exception as e:
#             self.fail(f"Job search functionality failed: {str(e)}")
    
#     def test_05_linkedin_login_page(self):
#         """Test if LinkedIn login page loads correctly"""
#         try:
#             # Navigate to the page
#             self.driver.get(self.base_url)
            
#             # Click on LinkedIn Login in the sidebar
#             login_option = self.wait.until(
#                 EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'LinkedIn Login')]"))
#             )
#             login_option.click()
            
#             # Check if login form fields are present
#             username_field = self.wait.until(
#                 EC.presence_of_element_located((By.XPATH, "//label[contains(text(), 'Username')]/../input"))
#             )
#             self.assertIsNotNone(username_field)
            
#             password_field = self.wait.until(
#                 EC.presence_of_element_located((By.XPATH, "//label[contains(text(), 'Password')]/../input"))
#             )
#             self.assertIsNotNone(password_field)
            
#             login_button = self.wait.until(
#                 EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Submit and Login')]"))
#             )
#             self.assertIsNotNone(login_button)
            
#             print("✅ Test 05: LinkedIn login page loads correctly")
#         except Exception as e:
#             self.fail(f"LinkedIn login page failed to load: {str(e)}")
    
#     def test_06_application_history_page(self):
#         """Test if application history page loads correctly"""
#         try:
#             # Navigate to the page
#             self.driver.get(self.base_url)
            
#             # Click on Application History in the sidebar
#             history_option = self.wait.until(
#                 EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Application History')]"))
#             )
#             history_option.click()
            
#             # Check if the header is present
#             header = self.wait.until(
#                 EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Application History')]"))
#             )
#             self.assertIsNotNone(header)
            
#             # We don't know if there will be data, so either a table or a message should appear
#             try:
#                 table = self.driver.find_element(By.TAG_NAME, "table")
#                 self.assertIsNotNone(table)
#                 print("✅ Test 06: Application history page shows table")
#             except:
#                 message = self.driver.find_element(By.XPATH, "//div[contains(text(), 'No application history')]")
#                 self.assertIsNotNone(message)
#                 print("✅ Test 06: Application history page shows 'no data' message")
                
#         except Exception as e:
#             self.fail(f"Application history page failed to load: {str(e)}")
    
#     def test_07_auto_apply_page_no_login(self):
#         """Test auto apply page without login"""
#         try:
#             # Navigate to the page
#             self.driver.get(self.base_url)
            
#             # Click on Auto Apply in the sidebar
#             auto_apply_option = self.wait.until(
#                 EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Auto Apply')]"))
#             )
#             auto_apply_option.click()
            
#             # Check for warning message about login
#             warning = self.wait.until(
#                 EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Please login to LinkedIn first')]"))
#             )
#             self.assertIsNotNone(warning)
            
#             print("✅ Test 07: Auto apply page shows correct warning when not logged in")
#         except Exception as e:
#             self.fail(f"Auto apply page failed to display warning: {str(e)}")
    
#     def test_08_input_validation(self):
#         """Test input validation for various fields"""
#         try:
#             # Navigate to the page and go to upload section
#             self.driver.get(self.base_url)
            
#             # Click on Upload Resume in the sidebar if needed
#             upload_option = self.wait.until(
#                 EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Upload Resume')]"))
#             )
#             upload_option.click()
            
#             # Select "Yes" for apply directly
#             yes_radio = self.wait.until(
#                 EC.element_to_be_clickable((By.XPATH, "//label[contains(text(), 'Yes')]"))
#             )
#             yes_radio.click()
            
#             # Try to click save without uploading a resume
#             save_button = self.wait.until(
#                 EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Save Resume Data')]"))
#             )
#             save_button.click()
            
#             # Should see a warning
#             warning = self.wait.until(
#                 EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'No resume file uploaded')]"))
#             )
#             self.assertIsNotNone(warning)
            
#             print("✅ Test 08: Input validation works correctly")
#         except Exception as e:
#             self.fail(f"Input validation test failed: {str(e)}")
    
#     def test_09_ui_elements_responsiveness(self):
#         """Test the UI responsiveness by resizing window"""
#         try:
#             # Navigate to the page
#             self.driver.get(self.base_url)
            
#             # Test different window sizes
#             for width, height in [(800, 600), (1024, 768), (1280, 800)]:
#                 self.driver.set_window_size(width, height)
#                 time.sleep(1)  # Allow time for UI to adjust
                
#                 # Verify the title is still visible
#                 title = self.driver.find_element(By.XPATH, "//h1[contains(text(), 'Automated Resume Analyzer')]")
#                 self.assertTrue(title.is_displayed())
                
#                 # Verify the sidebar is present
#                 sidebar = self.driver.find_element(By.XPATH, "//div[contains(@class, 'sidebar')]")
#                 self.assertTrue(sidebar.is_displayed())
            
#             print("✅ Test 09: UI is responsive at different window sizes")
#         except Exception as e:
#             self.fail(f"UI responsiveness test failed: {str(e)}")
    
#     def test_10_boundary_value_tests(self):
#         """Test boundary values and edge cases"""
#         try:
#             # Navigate to the page and go to job search
#             self.driver.get(self.base_url)
            
#             # Click on Auto Apply in the sidebar
#             auto_apply_option = self.wait.until(
#                 EC.element_to_be_clickable