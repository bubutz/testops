import os
import sys
import requests
import hashlib


class ArtifactoryTester:
    def __init__(self, url, username, password, repository):
        self.url = url.rstrip('/')
        self.username = username
        self.password = password
        self.repository = repository
        self.auth = (username, password)
        self.test_file = "test_artifact.txt"
        self.test_content = "This is a test artifact for Artifactory operations"

    def run_all_tests(self):
        """Run all Artifactory tests"""
        print("=" * 60)
        print("Starting Artifactory Operations Tests")
        print("=" * 60)

        tests_passed = 0
        tests_failed = 0

        # Test 1: Push
        if self.test_push():
            tests_passed += 1
        else:
            tests_failed += 1

        # Test 2: Pull
        if self.test_pull():
            tests_passed += 1
        else:
            tests_failed += 1

        # Test 3: Delete
        if self.test_delete():
            tests_passed += 1
        else:
            tests_failed += 1

        # Summary
        print("\n" + "=" * 60)
        print(f"Tests Passed: {tests_passed}")
        print(f"Tests Failed: {tests_failed}")
        print("=" * 60)

        return tests_failed == 0

    def test_push(self):
        """Test pushing an artifact to Artifactory"""
        print("\n[TEST] Push Artifact")
        print("-" * 60)

        try:
            artifact_path = f"{self.repository}/test/{self.test_file}"
            url = f"{self.url}/{artifact_path}"

            print(f"Pushing to: {url}")

            # Calculate checksum
            checksum = hashlib.sha256(self.test_content.encode()).hexdigest()

            headers = {
                'X-Checksum-Sha256': checksum
            }

            response = requests.put(
                url,
                auth=self.auth,
                data=self.test_content,
                headers=headers
            )

            if response.status_code in [200, 201]:
                print(f"✓ Push successful (Status: {response.status_code})")
                return True
            else:
                print(f"✗ Push failed (Status: {response.status_code})")
                print(f"Response: {response.text}")
                return False

        except Exception as e:
            print(f"✗ Push failed with exception: {str(e)}")
            return False

    def test_pull(self):
        """Test pulling an artifact from Artifactory"""
        print("\n[TEST] Pull Artifact")
        print("-" * 60)

        try:
            artifact_path = f"{self.repository}/test/{self.test_file}"
            url = f"{self.url}/{artifact_path}"

            print(f"Pulling from: {url}")

            response = requests.get(url, auth=self.auth)

            if response.status_code == 200:
                content = response.text
                if content == self.test_content:
                    print("✓ Pull successful, content matches")
                    return True
                else:
                    print("✗ Pull successful but content mismatch")
                    return False
            else:
                print(f"✗ Pull failed (Status: {response.status_code})")
                print(f"Response: {response.text}")
                return False

        except Exception as e:
            print(f"✗ Pull failed with exception: {str(e)}")
            return False

    def test_delete(self):
        """Test deleting an artifact from Artifactory"""
        print("\n[TEST] Delete Artifact")
        print("-" * 60)

        try:
            artifact_path = f"{self.repository}/test/{self.test_file}"
            url = f"{self.url}/{artifact_path}"

            print(f"Deleting: {url}")

            response = requests.delete(url, auth=self.auth)

            if response.status_code in [200, 204]:
                print(f"✓ Delete successful (Status: {response.status_code})")

                # Verify deletion
                verify = requests.get(url, auth=self.auth)
                if verify.status_code == 404:
                    print("✓ Verified artifact no longer exists")
                    return True
                else:
                    print("✗ Artifact still exists after deletion")
                    return False
            else:
                print(f"✗ Delete failed (Status: {response.status_code})")
                print(f"Response: {response.text}")
                return False

        except Exception as e:
            print(f"✗ Delete failed with exception: {str(e)}")
            return False


def main():
    """Main function to run tests"""
    # Get configuration from environment variables
    artifactory_url = os.getenv('ARTIFACTORY_URL')
    artifactory_username = os.getenv('ARTIFACTORY_USERNAME')
    artifactory_password = os.getenv('ARTIFACTORY_PASSWORD')
    artifactory_repo = os.getenv('ARTIFACTORY_REPOSITORY', 'generic-local')

    # Validate required environment variables
    if not all([artifactory_url, artifactory_username, artifactory_password]):
        print("Error: Missing required environment variables:")
        print("  - ARTIFACTORY_URL")
        print("  - ARTIFACTORY_USERNAME")
        print("  - ARTIFACTORY_PASSWORD")
        print("  - ARTIFACTORY_REPOSITORY (optional, defaults to 'generic-local')")
        sys.exit(1)

    # Create tester instance and run tests
    tester = ArtifactoryTester(
        url=artifactory_url,
        username=artifactory_username,
        password=artifactory_password,
        repository=artifactory_repo
    )

    success = tester.run_all_tests()

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
