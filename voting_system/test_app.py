import unittest
from app import app

class VotingSystemTestCase(unittest.TestCase):
    def setUp(self):
        # Set up the test client and the application context
        self.app = app.test_client()
        self.app.testing = True

    def test_add_candidate(self):
        # Test adding a candidate
        response = self.app.post('/add_candidate', data={'name': 'Alice'})
        self.assertEqual(response.status_code, 302)  # Check for redirect
        response = self.app.get('/')
        self.assertIn(b'Alice', response.data)  # Check if Alice is in the index page

    def test_vote(self):
        # First, add a candidate
        self.app.post('/add_candidate', data={'name': 'Bob'})
        
        # Now, vote for the candidate
        response = self.app.post('/vote', data={'candidate': 'Bob'})
        self.assertEqual(response.status_code, 302)  # Check for redirect
        
        # Check if the vote was counted
        response = self.app.get('/results')
        self.assertIn(b'Bob: 1 votes', response.data)  # Check if Bob has 1 vote

    def test_results(self):
        # Add candidates and vote
        self.app.post('/add_candidate', data={'name': 'Charlie'})
        self.app.post('/vote', data={'candidate': 'Charlie'})
        
        # Check results page
        response = self.app.get('/results')
        self.assertIn(b'Charlie: 1 votes', response.data)  # Check if Charlie has 1 vote

    def test_vote_for_nonexistent_candidate(self):
        # Attempt to vote for a candidate that doesn't exist
        response = self.app.post('/vote', data={'candidate': 'Nonexistent'})
        self.assertEqual(response.status_code, 302)  # Check for redirect
        response = self.app.get('/results')
        self.assertNotIn(b'Nonexistent', response.data)  # Ensure they are not in the results

if __name__ == '__main__':
    unittest.main()