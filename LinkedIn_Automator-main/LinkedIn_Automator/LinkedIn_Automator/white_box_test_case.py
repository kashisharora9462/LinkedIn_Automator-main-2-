import unittest
from unittest.mock import patch, MagicMock, mock_open
import os
import pandas as pd
import sys
import io
from main import main

class TestResumeAnalyzerWhiteBox(unittest.TestCase):
    
    def setUp(self):
        # Mock session state
        self.session_state_patch = patch('streamlit.session_state', {})
        self.mock_session_state = self.session_state_patch.start()
        
        # Mock Streamlit components
        self.st_patch = patch('streamlit.title')
        self.mock_st = self.st_patch.start()
        
        # Mock RepositoryFactory
        self.repo_factory_patch = patch('data_access_layer.RepositoryFactory.create_resume_repository')
        self.mock_repo_factory = self.repo_factory_patch.start()
        self.mock_repo = MagicMock()
        self.mock_repo_factory.return_value = self.mock_repo
        
    def tearDown(self):
        self.session_state_patch.stop()
        self.st_patch.stop()
        self.repo_factory_patch.stop()
        
    @patch('streamlit.radio')
    def test_navigation_page_selection(self, mock_radio):
        """Test the page navigation logic"""
        # Test each page selection
        for page in ["Upload Resume", "Job Search", "LinkedIn Login", "Auto Apply", "Application History"]:
            mock_radio.return_value = page
            with patch('main.st') as mock_st:
                # This will trigger different code paths based on the page value
                main()
                # Verify the subheader was called with appropriate text for the page
                expected_calls = {
                    "Upload Resume": "📄 Upload Your Resume",
                    "Job Search": "🔎 Find Relevant Jobs",
                    "LinkedIn Login": "🔐 Login to LinkedIn",
                    "Auto Apply": "🤖 Automated Job Applications",
                    "Application History": "📊 Application History"
                }
                mock_st.subheader.assert_any_call(expected_calls[page])
    
    @patch('os.makedirs')
    @patch('builtins.open', new_callable=mock_open)
    @patch('streamlit.file_uploader')
    @patch('streamlit.session_state', {"user_data": {"user_id": None, "resume_id": None}})
    @patch('resume_processing.extract_text_from_pdf')
    @patch('resume_processing.analyze_resume')
    def test_resume_upload_and_save(self, mock_analyze, mock_extract, mock_uploader, mock_file, mock_makedirs):
        """Test the resume upload and save logic path"""
        # Set up mocks
        mock_file_obj = MagicMock()
        mock_file_obj.name = "test_resume.pdf"
        mock_file_obj.getvalue.return_value = b"fake pdf content"
        mock_uploader.return_value = mock_file_obj
        
        mock_extract.return_value = ("Sample resume text", ["http://example.com"])
        mock_analyze.return_value = {
            "personal_information": {"name": "John", "surname": "Doe", "email": "john@example.com"},
            "skills": ["Python", "Data Analysis"]
        }
        
        with patch('streamlit.radio') as mock_radio:
            mock_radio.return_value = "Upload Resume"
            with patch('streamlit.radio', return_value="Yes") as mock_apply_radio:
                with patch('streamlit.button') as mock_button:
                    mock_button.return_value = True  # Simulate clicking "Save Resume Data"
                    
                    # Run the function
                    main()
                    
                    # Verify directory creation
                    mock_makedirs.assert_called_with("uploads", exist_ok=True)
                    
                    # Verify file was opened for writing
                    mock_file.assert_called_with(os.path.join("uploads", "test_resume.pdf"), "wb")
                    
                    # Verify repository save methods were called
                    self.mock_repo.save_user.assert_called_once()
                    self.mock_repo.save_resume.assert_called_once()
                    self.mock_repo.save_resume_as_yaml.assert_called_once()
    
    @patch('streamlit.button')
    @patch('streamlit.session_state', {"user_data": {"user_id": "123", "resume_id": "456"}})
    def test_job_application_history_display(self, mock_button):
        """Test the job application history display logic"""
        # Setup mock applications data
        mock_applications = [
            {
                "job_title": "Software Engineer", 
                "status": "Successfully Applied",
                "applied_at": "2023-03-30",
                "job_url": "https://linkedin.com/jobs/123"
            }
        ]
        self.mock_repo.get_job_applications.return_value = mock_applications
        
        with patch('streamlit.radio') as mock_radio:
            mock_radio.return_value = "Application History"
            
            with patch('pandas.DataFrame') as mock_df:
                with patch('streamlit.table') as mock_table:
                    # Run the function
                    main()
                    
                    # Verify repository method was called
                    self.mock_repo.get_job_applications.assert_called_with("456")
                    
                    # Verify DataFrame was created and displayed
                    mock_df.assert_called_once()
                    mock_table.assert_called_once()
    
    @patch('streamlit.button')
    @patch('job_suggestion.suggest_jobs')
    @patch('linkedin.generate_linkedin_url')
    def test_job_search_functionality(self, mock_gen_url, mock_suggest, mock_button):
        """Test the job search functionality path"""
        # Setup mocks
        mock_button.return_value = True
        mock_suggest.return_value = ["Software Engineer", "Data Scientist"]
        mock_gen_url.side_effect = lambda job, loc: f"https://linkedin.com/jobs/search?keywords={job}&location={loc}"
        
        # Setup session state with extracted data
        with patch('streamlit.session_state', {
            "user_data": {"user_id": "123", "resume_id": "456"},
            "jobs_fetched": False
        }):
            with patch('streamlit.radio') as mock_radio:
                mock_radio.return_value = "Job Search"
                
                # Mock extracted data for job search
                extracted_data = {
                    "skills": ["Python", "SQL", "Machine Learning"],
                    "experience_details": [{"position": "Developer", "company": "ABC Corp"}]
                }
                
                with patch('main.extracted_data', extracted_data):
                    with patch('streamlit.markdown') as mock_markdown:
                        # Run the function
                        main()
                        
                        # Verify job suggestion was called
                        mock_suggest.assert_called_once()
                        
                        # Verify URL generation
                        mock_gen_url.assert_any_call("Software Engineer", "India")
                        mock_gen_url.assert_any_call("Data Scientist", "India")
                        
                        # Verify markdown table was created
                        mock_markdown.assert_called_once()
    
    @patch('streamlit.text_input')
    @patch('streamlit.button')
    @patch('linkedin_auth.setup_and_login')
    def test_linkedin_login_flow(self, mock_login, mock_button, mock_text_input):
        """Test the LinkedIn login functionality path"""
        # Setup mocks
        mock_text_input.side_effect = ["test@example.com", "password123"]
        mock_button.return_value = True
        
        # Mock successful login
        mock_driver = MagicMock()
        mock_wait = MagicMock()
        mock_login.return_value = (mock_driver, mock_wait)
        
        with patch('streamlit.radio') as mock_radio:
            mock_radio.return_value = "LinkedIn Login"
            
            with patch('streamlit.session_state', {}):
                with patch('streamlit.success') as mock_success:
                    # Run the function
                    main()
                    
                    # Verify login was attempted
                    mock_login.assert_called_with("test@example.com", "password123")
                    
                    # Verify success message
                    mock_success.assert_called_once()

    @patch('streamlit.button')
    @patch('streamlit.slider')
    @patch('streamlit.text_input')
    @patch('streamlit.progress')
    @patch('job_navigation.navigate_to_job')
    @patch('fill_linkedin_form.fill_linkedin_form')
    @patch('time.sleep')
    def test_auto_apply_functionality(self, mock_sleep, mock_fill, mock_navigate, 
                                      mock_progress, mock_text_input, mock_slider, mock_button):
        """Test the auto-apply functionality path"""
        # Setup mocks
        mock_text_input.return_value = "resume.pdf"
        mock_slider.return_value = 2  # Apply to 2 jobs
        mock_button.return_value = True
        
        mock_driver = MagicMock()
        mock_wait = MagicMock()
        mock_progress_bar = MagicMock()
        mock_progress.return_value = mock_progress_bar
        
        # Mock successful navigation and form filling
        mock_navigate.return_value = True
        
        # Setup session state with driver and job links
        with patch('streamlit.session_state', {
            "driver": mock_driver,
            "wait": mock_wait,
            "user_data": {"user_id": "123", "resume_id": "456"},
            "job_links": [
                {"Job Title": "Software Engineer", "Apply Link": "https://linkedin.com/jobs/123"},
                {"Job Title": "Data Scientist", "Apply Link": "https://linkedin.com/jobs/456"}
            ]
        }):
            with patch('streamlit.radio') as mock_radio:
                mock_radio.return_value = "Auto Apply"
                
                with patch('streamlit.table') as mock_table:
                    # Run the function
                    main()
                    
                    # Verify navigation was attempted for both jobs
                    self.assertEqual(mock_navigate.call_count, 2)
                    
                    # Verify form filling was attempted for both jobs
                    self.assertEqual(mock_fill.call_count, 2)
                    
                    # Verify job applications were saved to database
                    self.assertEqual(self.mock_repo.save_job_application.call_count, 2)
                    
                    # Verify results table was displayed
                    mock_table.assert_called_once()
    
    @patch('streamlit.button')
    @patch('streamlit.slider')
    @patch('streamlit.text_input')
    @patch('streamlit.progress')
    @patch('job_navigation.navigate_to_job')
    def test_auto_apply_navigate_failure(self, mock_navigate, mock_progress, 
                                        mock_text_input, mock_slider, mock_button):
        """Test the auto-apply functionality with navigation failure"""
        # Setup mocks
        mock_text_input.return_value = "resume.pdf"
        mock_slider.return_value = 1  # Apply to 1 job
        mock_button.return_value = True
        
        mock_driver = MagicMock()
        mock_wait = MagicMock()
        mock_progress_bar = MagicMock()
        mock_progress.return_value = mock_progress_bar
        
        # Mock failed navigation
        mock_navigate.return_value = False
        
        # Setup session state with driver and job links
        with patch('streamlit.session_state', {
            "driver": mock_driver,
            "wait": mock_wait,
            "user_data": {"user_id": "123", "resume_id": "456"},
            "job_links": [
                {"Job Title": "Software Engineer", "Apply Link": "https://linkedin.com/jobs/123"}
            ]
        }):
            with patch('streamlit.radio') as mock_radio:
                mock_radio.return_value = "Auto Apply"
                
                with patch('streamlit.warning') as mock_warning:
                    # Run the function
                    main()
                    
                    # Verify navigation was attempted
                    mock_navigate.assert_called_once()
                    
                    # Verify warning was displayed
                    mock_warning.assert_called_once()
                    
                    # Verify job application was saved with failure status
                    self.mock_repo.save_job_application.assert_called_once()
                    call_args = self.mock_repo.save_job_application.call_args[0]
                    self.assertEqual(call_args[0], "456")  # resume_id
                    self.assertEqual(call_args[1]["status"], "Easy Apply not available")


if __name__ == '__main__':
    unittest.main()