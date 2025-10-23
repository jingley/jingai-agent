# aiagent/tests/test_agent_functions.py

import unittest
import os
import sys

# Add the parent directory to the path so we can import the function
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.functions.agent_functions import run_python_file, get_files_info, get_file_content, write_file


class TestGetFilesInfo(unittest.TestCase):
    """Test cases for get_files_info function"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    def test_get_files_info_root_directory(self):
        """Test listing files in root directory"""
        result = get_files_info(self.base_dir, ".")
        
        # Verify expected files are present
        self.assertIn("main.py", result)
        self.assertIn("is_dir=False", result)  # main.py should be a file
        self.assertIn("agent", result)
        self.assertIn("is_dir=True", result)   # agent should be a directory
    
    def test_get_files_info_subdirectory(self):
        """Test listing files in subdirectory"""
        result = get_files_info(self.base_dir, "calculator")
        
        # Verify expected files are present
        self.assertIn("main.py", result)
        self.assertIn("pkg", result)
        self.assertIn("lorem.txt", result)
    
    def test_get_files_info_nested_directory(self):
        """Test listing files in nested directory"""
        result = get_files_info(self.base_dir, "calculator/pkg")
        
        # Verify expected files are present
        self.assertIn("calculator.py", result)
        self.assertIn("render.py", result)
        self.assertIn("__init__.py", result)
    
    def test_get_files_info_nonexistent_directory(self):
        """Test listing files in nonexistent directory"""
        result = get_files_info(self.base_dir, "nonexistent")
        
        self.assertIn("does not exist", result)
    
    def test_get_files_info_security_path_traversal(self):
        """Test security: path traversal prevention"""
        result = get_files_info(self.base_dir, "../")
        
        self.assertIn("Access denied", result)


class TestGetFileContent(unittest.TestCase):
    """Test cases for get_file_content function"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    def test_get_file_content_existing_file(self):
        """Test reading content from existing file"""
        result = get_file_content(self.base_dir, "README.md")
        
        # Verify content contains expected text
        self.assertIn("AI Agent", result)
    
    def test_get_file_content_python_file(self):
        """Test reading content from Python file"""
        result = get_file_content(self.base_dir, "main.py")
        
        # Verify content contains expected Python code
        self.assertIn("import", result)
        self.assertIn("def main", result)
    
    def test_get_file_content_nested_file(self):
        """Test reading content from nested file"""
        result = get_file_content(self.base_dir, "calculator/pkg/calculator.py")
        
        # Verify content contains expected class
        self.assertIn("class Calculator", result)
    
    def test_get_file_content_nonexistent_file(self):
        """Test reading content from nonexistent file"""
        result = get_file_content(self.base_dir, "nonexistent.txt")
        
        self.assertIn("not found", result)
    
    def test_get_file_content_security_path_traversal(self):
        """Test security: path traversal prevention"""
        result = get_file_content(self.base_dir, "../some_file.txt")
        
        self.assertIn("Access denied", result)


class TestWriteFile(unittest.TestCase):
    """Test cases for write_file function"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.test_file = "test_write_file.txt"
        self.test_dir = "test_directory"
        
    def tearDown(self):
        """Clean up test files after each test method."""
        # Clean up test files
        test_file_path = os.path.join(self.base_dir, self.test_file)
        if os.path.exists(test_file_path):
            os.remove(test_file_path)
            
        # Clean up test directory and files
        test_dir_path = os.path.join(self.base_dir, self.test_dir)
        if os.path.exists(test_dir_path):
            import shutil
            shutil.rmtree(test_dir_path)
    
    def test_write_file_new_file(self):
        """Test creating a new file"""
        content = "Hello, World!\nThis is a test file."
        result = write_file(self.base_dir, self.test_file, content)
        
        # Verify file was created
        test_file_path = os.path.join(self.base_dir, self.test_file)
        self.assertTrue(os.path.exists(test_file_path))
        
        # Verify content is correct
        with open(test_file_path, 'r', encoding='utf-8') as f:
            written_content = f.read()
        self.assertEqual(written_content, content)
    
    def test_write_file_nested_directory(self):
        """Test creating file in nested directory (auto-create directories)"""
        nested_file = f"{self.test_dir}/nested/test.txt"
        content = "Nested file content"
        
        result = write_file(self.base_dir, nested_file, content)
        
        # Verify file and directories were created
        nested_file_path = os.path.join(self.base_dir, self.test_dir, "nested", "test.txt")
        self.assertTrue(os.path.exists(nested_file_path))
        
        # Verify content is correct
        with open(nested_file_path, 'r', encoding='utf-8') as f:
            written_content = f.read()
        self.assertEqual(written_content, content)
    
    def test_write_file_overwrite_existing(self):
        """Test overwriting existing file"""
        # First create a file
        original_content = "Original content"
        write_file(self.base_dir, self.test_file, original_content)
        
        # Now overwrite it
        new_content = "New content that overwrites the original"
        result = write_file(self.base_dir, self.test_file, new_content)
        
        # Verify content was overwritten
        test_file_path = os.path.join(self.base_dir, self.test_file)
        with open(test_file_path, 'r', encoding='utf-8') as f:
            written_content = f.read()
        self.assertEqual(written_content, new_content)
    
    def test_write_file_security_path_traversal(self):
        """Test security: path traversal prevention"""
        content = "Malicious content"
        result = write_file(self.base_dir, "../malicious.txt", content)
        
        self.assertIn("Access denied", result)


class TestRunPythonFile(unittest.TestCase):
    """Test cases for run_python_file function"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Use the actual project structure for testing
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        
    def test_run_python_file_cases(self):
        """Test all run_python_file cases"""
        
        # Test 1: run_python_file("calculator", "main.py") - should print usage instructions
        result1 = run_python_file(self.base_dir, "calculator/main.py")
        
        # Test 2: run_python_file("calculator", "main.py", ["3 + 5"]) - should run calculator
        result2 = run_python_file(self.base_dir, "calculator/main.py", ["3 + 5"])
        
        # Test 3: run_python_file("calculator", "tests.py") - should run tests
        result3 = run_python_file(self.base_dir, "calculator/tests.py")
        
        # Test 4: run_python_file("calculator", "../main.py") - should return error (outside directory)
        # Need to use calculator as working directory to test path traversal
        calculator_dir = os.path.join(self.base_dir, "calculator")
        result4 = run_python_file(calculator_dir, "../main.py")
        
        # Test 5: run_python_file("calculator", "nonexistent.py") - should return error (file not found)
        result5 = run_python_file(self.base_dir, "calculator/nonexistent.py")
        
        # Test 6: run_python_file("calculator", "lorem.txt") - should return error (not a Python file)
        result6 = run_python_file(self.base_dir, "calculator/lorem.txt")


class TestAllFunctions(unittest.TestCase):
    """Integration tests for all agent functions"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    def test_function_integration_workflow(self):
        """Test a complete workflow using multiple functions"""
        
        # 1. List files in root directory
        files_result = get_files_info(self.base_dir, ".")
        self.assertIn("main.py", files_result)
        
        # 2. Read content of a file
        content_result = get_file_content(self.base_dir, "main.py")
        self.assertIn("def main", content_result)
        
        # 3. Create a test file
        test_content = "# Test integration file\nprint('Integration test successful!')\n"
        write_result = write_file(self.base_dir, "integration_test.py", test_content)
        
        # 4. Run the created file
        run_result = run_python_file(self.base_dir, "integration_test.py")
        self.assertIn("Integration test successful!", run_result)
        
        # 5. Clean up
        test_file_path = os.path.join(self.base_dir, "integration_test.py")
        if os.path.exists(test_file_path):
            os.remove(test_file_path)


def run_all_tests():
    """Run all test classes in order"""
    print("=" * 100)
    print("RUNNING COMPREHENSIVE AGENT FUNCTIONS TEST SUITE")
    print("=" * 100)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestGetFilesInfo))
    suite.addTests(loader.loadTestsFromTestCase(TestGetFileContent))
    suite.addTests(loader.loadTestsFromTestCase(TestWriteFile))
    suite.addTests(loader.loadTestsFromTestCase(TestRunPythonFile))
    suite.addTests(loader.loadTestsFromTestCase(TestAllFunctions))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 100)
    print("TEST SUITE SUMMARY")
    print("=" * 100)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    print("=" * 100)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_all_tests()
