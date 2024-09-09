#!/usr/bin/env python3

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """TestGithubOrgClient class"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test org method"""
        expected_result = {"org_name": org_name}
        mock_get_json.return_value = expected_result
        github_client = GithubOrgClient(org_name)
        result = github_client.org()
        mock_get_json.assert_called_once_with("https://api.github.com/orgs/" + org_name)
        self.assertEqual(result, expected_result)

    @patch('client.get_json')
    def test_public_repos_url(self, mock_get_json):
        """Test public_repos_url method"""
        mock_payload = {"repos_url": "https://api.github.com/orgs/exampleorg/repos"}
        mock_get_json.return_value = mock_payload
        org_client = GithubOrgClient("exampleorg")
        expected_url = "https://api.github.com/orgs/exampleorg/repos"
        self.assertEqual(org_client._public_repos_url, expected_url)

    @patch('client.GithubOrgClient.get_json')
    def test_public_repos(self, mock_get_json):
        """Test public_repos method"""
        mock_get_json.return_value = [{"name": "repo1"}, {"name": "repo2"}, {"name": "repo3"}]
        with patch('client.GithubOrgClient._public_repos_url', PropertyMock(return_value="www.no.com")) as y:
            github_org_client = GithubOrgClient("www.no.com")
            repos = github_org_client.public_repos()
            mock_get_json.assert_called_once_with('www.no.com')
            expected_repos = ["repo1", "repo2", "repo3"]
            self.assertEqual(repos, expected_repos)
            y.assert_called_once_with()


    @parameterized.expand([
        ({'license': {'key': 'my_license'}}, 'my_license', True),
        ({'license': {'key': 'other_license'}}, 'my_license', False)
    ])
    def test_has_license(self, repo, license, expected):
        """Test has_license method"""
        self.assertEqual(GithubOrgClient.has_license(repo, license), expected)


@parameterized_class(
    ('org_payload', 'repos_payload', 'expected_repos', 'apache2_repos'),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test class"""
    
    @classmethod
    def setUpClass(cls):
        """Set up class"""
        org = TEST_PAYLOAD[0][0]
        repos = TEST_PAYLOAD[0][1]
        mock_organisation = Mock()
        mock_organisation.json = Mock(return_value=org)
        cls.organisation_mock = mock_organisation
        mock_repo = Mock()
        mock_repo.json = Mock(return_value=repos)
        cls.repo_mock = mock_repo
        cls.get_patcher = patch('requests.get')
        cls.get = cls.get_patcher.start()
        options = {cls.org_payload["repos_url"]: mock_repo}
        cls.get.side_effect = lambda y: options.get(y, mock_organisation)

    @classmethod
    def tearDownClass(cls):
        """Tear down class"""
        cls.get_patcher.stop()
