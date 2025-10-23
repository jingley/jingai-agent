"""
Test suite for main.py - AI Agent CLI interface

Tests command-line argument parsing, help functionality, and error handling.
"""

import unittest
import sys
import os
from io import StringIO
from unittest.mock import patch, MagicMock

# Add the parent directory to the path so we can import main
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestMainArguments(unittest.TestCase):
    """Test class for main.py argument parsing and CLI functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Mock the dependencies that require external packages
        self.mock_genai = MagicMock()
        self.mock_load_dotenv = MagicMock()
        self.mock_run_agent = MagicMock()
        
        # Patch the imports
        self.genai_patcher = patch('main.genai', self.mock_genai)
        self.dotenv_patcher = patch('main.load_dotenv', self.mock_load_dotenv)
        self.run_agent_patcher = patch('main.run_agent', self.mock_run_agent)
        
        self.genai_patcher.start()
        self.dotenv_patcher.start() 
        self.run_agent_patcher.start()
        
        # Mock environment variable
        os.environ['GEMINI_API_KEY'] = 'test_api_key'
    
    def tearDown(self):
        """Clean up after tests"""
        self.genai_patcher.stop()
        self.dotenv_patcher.stop()
        self.run_agent_patcher.stop()
        
        # Clean up environment
        if 'GEMINI_API_KEY' in os.environ:
            del os.environ['GEMINI_API_KEY']
    
    @patch('sys.argv', ['main.py', '--help'])
    def test_help_argument_long(self):
        """Test --help argument shows help message and exits"""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            with self.assertRaises(SystemExit) as cm:
                import main
                main.main()
            
            self.assertEqual(cm.exception.code, 0)
            output = mock_stdout.getvalue()
            self.assertIn("AI Agent - Agentic AI with File Operations", output)
            self.assertIn("Usage:", output)
            self.assertIn("Available Agent Capabilities:", output)
            self.assertIn("Example Requests:", output)
    
    @patch('sys.argv', ['main.py', '-h'])
    def test_help_argument_short(self):
        """Test -h argument shows help message and exits"""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            with self.assertRaises(SystemExit) as cm:
                import main
                main.main()
            
            self.assertEqual(cm.exception.code, 0)
            output = mock_stdout.getvalue()
            self.assertIn("AI Agent - Agentic AI with File Operations", output)
    
    @patch('sys.argv', ['main.py', '--prompt', 'test prompt'])
    def test_prompt_argument_long(self):
        """Test --prompt argument with valid value"""
        # Mock run_agent to return no function calls to exit loop
        self.mock_run_agent.return_value = ([], False)
        
        import main
        main.main()
        
        # Verify the agent was called
        self.mock_run_agent.assert_called()
    
    @patch('sys.argv', ['main.py', '-p', 'test prompt'])
    def test_prompt_argument_short(self):
        """Test -p argument with valid value"""
        # Mock run_agent to return no function calls to exit loop
        self.mock_run_agent.return_value = ([], False)
        
        import main
        main.main()
        
        # Verify the agent was called
        self.mock_run_agent.assert_called()
    
    @patch('sys.argv', ['main.py', 'positional prompt'])
    def test_positional_argument_as_prompt(self):
        """Test positional argument treated as prompt"""
        # Mock run_agent to return no function calls to exit loop
        self.mock_run_agent.return_value = ([], False)
        
        import main
        main.main()
        
        # Verify the agent was called
        self.mock_run_agent.assert_called()
    
    @patch('sys.argv', ['main.py', '--prompt', 'test', '--verbose'])
    def test_verbose_argument_long(self):
        """Test --verbose argument"""
        # Mock run_agent to return no function calls to exit loop
        self.mock_run_agent.return_value = ([], False)
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            import main
            main.main()
        
        output = mock_stdout.getvalue()
        self.assertIn("User's prompt: test", output)
    
    @patch('sys.argv', ['main.py', '-p', 'test', '-v'])
    def test_verbose_argument_short(self):
        """Test -v argument"""
        # Mock run_agent to return no function calls to exit loop
        self.mock_run_agent.return_value = ([], False)
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            import main
            main.main()
        
        output = mock_stdout.getvalue()
        self.assertIn("User's prompt: test", output)
    
    @patch('sys.argv', ['main.py', '--prompt'])
    def test_prompt_missing_value(self):
        """Test --prompt without value shows error"""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            with self.assertRaises(SystemExit) as cm:
                import main
                main.main()
            
            self.assertEqual(cm.exception.code, 1)
            output = mock_stdout.getvalue()
            self.assertIn("Error: --prompt requires a value", output)
    
    @patch('sys.argv', ['main.py'])
    def test_no_prompt_error(self):
        """Test missing prompt shows error"""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            with self.assertRaises(SystemExit) as cm:
                import main
                main.main()
            
            self.assertEqual(cm.exception.code, 1)
            output = mock_stdout.getvalue()
            self.assertIn("Error: --prompt is required.", output)
    
    @patch('sys.argv', ['main.py', '--prompt', '--verbose'])
    def test_prompt_followed_by_flag(self):
        """Test --prompt followed by another flag (invalid)"""
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            with self.assertRaises(SystemExit) as cm:
                import main
                main.main()
            
            self.assertEqual(cm.exception.code, 1)
            output = mock_stdout.getvalue()
            self.assertIn("Error: --prompt requires a value", output)
    
    @patch('sys.argv', ['main.py', 'test prompt', '--verbose'])
    def test_argument_order_independence(self):
        """Test that argument order doesn't matter"""
        # Mock run_agent to return no function calls to exit loop
        self.mock_run_agent.return_value = ([], False)
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            import main
            main.main()
        
        output = mock_stdout.getvalue()
        self.assertIn("User's prompt: test prompt", output)
    
    @patch('sys.argv', ['main.py', '--prompt', 'test'])
    def test_max_iterations_warning(self):
        """Test maximum iterations warning"""
        # Mock run_agent to always return function calls (infinite loop scenario)
        self.mock_run_agent.return_value = ([], True)
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            import main
            main.main()
        
        output = mock_stdout.getvalue()
        self.assertIn("Warning: Maximum iterations reached", output)
    
    @patch('sys.argv', ['main.py', '--prompt', 'test'])
    def test_agent_initialization(self):
        """Test that agent is properly initialized with correct parameters"""
        # Mock run_agent to return no function calls to exit loop
        self.mock_run_agent.return_value = ([], False)
        
        import main
        main.main()
        
        # Verify dotenv was loaded
        self.mock_load_dotenv.assert_called_once()
        
        # Verify genai client was created
        self.mock_genai.Client.assert_called_once_with(api_key='test_api_key')
        
        # Verify run_agent was called with correct parameters
        self.mock_run_agent.assert_called()
        args, kwargs = self.mock_run_agent.call_args
        self.assertEqual(len(args), 4)  # client, messages, available_functions, verbose_flag


class TestMainFunctionality(unittest.TestCase):
    """Test class for main.py core functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Mock the dependencies
        self.mock_genai = MagicMock()
        self.mock_load_dotenv = MagicMock()
        self.mock_run_agent = MagicMock()
        
        # Patch the imports
        self.genai_patcher = patch('main.genai', self.mock_genai)
        self.dotenv_patcher = patch('main.load_dotenv', self.mock_load_dotenv)
        self.run_agent_patcher = patch('main.run_agent', self.mock_run_agent)
        
        self.genai_patcher.start()
        self.dotenv_patcher.start()
        self.run_agent_patcher.start()
        
        os.environ['GEMINI_API_KEY'] = 'test_api_key'
    
    def tearDown(self):
        """Clean up after tests"""
        self.genai_patcher.stop()
        self.dotenv_patcher.stop()
        self.run_agent_patcher.stop()
        
        if 'GEMINI_API_KEY' in os.environ:
            del os.environ['GEMINI_API_KEY']
    
    @patch('sys.argv', ['main.py', '--prompt', 'test', '--verbose'])
    def test_verbose_iteration_counting(self):
        """Test verbose mode shows iteration counting"""
        # Mock run_agent to return function calls for 3 iterations, then stop
        call_count = 0
        def mock_run_agent_side_effect(*args):
            nonlocal call_count
            call_count += 1
            return ([], call_count < 3)  # Return True for first 2 calls, False for 3rd
        
        self.mock_run_agent.side_effect = mock_run_agent_side_effect
        
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            import main
            main.main()
        
        output = mock_stdout.getvalue()
        self.assertIn("Agent iteration 1 completed", output)
        self.assertIn("Agent iteration 2 completed", output)
        self.assertNotIn("Agent iteration 3 completed", output)  # Should stop after 2


def run_tests_with_logging():
    """Run tests with enhanced logging output"""
    print("=" * 80)
    print("🚀 STARTING MAIN.PY TEST SUITE")
    print("=" * 80)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes in order
    suite.addTests(loader.loadTestsFromTestCase(TestMainArguments))
    suite.addTests(loader.loadTestsFromTestCase(TestMainFunctionality))
    
    # Run with custom runner
    runner = unittest.TextTestRunner(
        verbosity=2,
        stream=sys.stdout,
        descriptions=True,
        failfast=False
    )
    
    result = runner.run(suite)
    
    print("\n" + "=" * 80)
    print("📊 TEST SUITE RESULTS")
    print("=" * 80)
    print(f"✅ Tests run: {result.testsRun}")
    print(f"❌ Failures: {len(result.failures)}")
    print(f"💥 Errors: {len(result.errors)}")
    print(f"⏭️  Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    
    if result.failures:
        print(f"\n❌ FAILURES ({len(result.failures)}):")
        for i, (test, traceback) in enumerate(result.failures, 1):
            print(f"  {i}. {test}")
    
    if result.errors:
        print(f"\n💥 ERRORS ({len(result.errors)}):")
        for i, (test, traceback) in enumerate(result.errors, 1):
            print(f"  {i}. {test}")
    
    success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100) if result.testsRun > 0 else 0
    print(f"\n🎯 Success Rate: {success_rate:.1f}%")
    
    if result.wasSuccessful():
        print("🎉 ALL TESTS PASSED!")
    else:
        print("⚠️  Some tests failed - check output above")
    
    print("=" * 80)
    return result.wasSuccessful()


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--enhanced':
        # Run with enhanced logging
        success = run_tests_with_logging()
        sys.exit(0 if success else 1)
    else:
        # Run standard unittest
        unittest.main()
