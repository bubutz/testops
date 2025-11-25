#!/usr/bin/env python3
"""
Artifactory Operations Test Script
Tests pull, push, and delete operations against Artifactory
"""

import os
import sys
import requests
import hashlib


# Configuration
ARTIFACTORY_URL = os.getenv('ARTIFACTORY_URL')
ARTIFACTORY_USERNAME = os.getenv('ARTIFACTORY_USERNAME')
ARTIFACTORY_PASSWORD = os.getenv('ARTIFACTORY_PASSWORD')
ARTIFACTORY_REPOSITORY = os.getenv('ARTIFACTORY_REPOSITORY', 'generic-local')

# Test data
TEST_FILE = "test_artifact.txt"
TEST_CONTENT = "This is a test artifact for Artifactory operations"


def test_push():
    """Test pushing an artifact to Artifactory"""
    print("\n[TEST] Push Artifact")
    print("-" * 60)

    try:
        artifact_path = f"{ARTIFACTORY_REPOSITORY}/test/{TEST_FILE}"
        url = f"{ARTIFACTORY_URL}/{artifact_path}"

        print(f"Pushing to: {url}")

        # Calculate checksum
        checksum = hashlib.sha256(TEST_CONTENT.encode()).hexdigest()

        headers = {
            'X-Checksum-Sha256': checksum
        }

        response = requests.put(
            url,
            auth=(ARTIFACTORY_USERNAME, ARTIFACTORY_PASSWORD),
            data=TEST_CONTENT,
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


def test_pull():
    """Test pulling an artifact from Artifactory"""
    print("\n[TEST] Pull Artifact")
    print("-" * 60)

    try:
        artifact_path = f"{ARTIFACTORY_REPOSITORY}/test/{TEST_FILE}"
        url = f"{ARTIFACTORY_URL}/{artifact_path}"

        print(f"Pulling from: {url}")

        response = requests.get(
            url,
            auth=(ARTIFACTORY_USERNAME, ARTIFACTORY_PASSWORD)
        )

        if response.status_code == 200:
            content = response.text
            if content == TEST_CONTENT:
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


def test_delete():
    """Test deleting an artifact from Artifactory"""
    print("\n[TEST] Delete Artifact")
    print("-" * 60)

    try:
        artifact_path = f"{ARTIFACTORY_REPOSITORY}/test/{TEST_FILE}"
        url = f"{ARTIFACTORY_URL}/{artifact_path}"

        print(f"Deleting: {url}")

        response = requests.delete(
            url,
            auth=(ARTIFACTORY_USERNAME, ARTIFACTORY_PASSWORD)
        )

        if response.status_code in [200, 204]:
            print(f"✓ Delete successful (Status: {response.status_code})")

            # Verify deletion
            verify = requests.get(
                url,
                auth=(ARTIFACTORY_USERNAME, ARTIFACTORY_PASSWORD)
            )
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
    # Validate required environment variables
    if not all([ARTIFACTORY_URL, ARTIFACTORY_USERNAME, ARTIFACTORY_PASSWORD]):
        print("Error: Missing required environment variables:")
        print("  - ARTIFACTORY_URL")
        print("  - ARTIFACTORY_USERNAME")
        print("  - ARTIFACTORY_PASSWORD")
        print("  - ARTIFACTORY_REPOSITORY (optional, defaults to 'generic-local')")
        sys.exit(1)

    print("=" * 60)
    print("Starting Artifactory Operations Tests")
    print("=" * 60)
    print(f"URL: {ARTIFACTORY_URL}")
    print(f"Repository: {ARTIFACTORY_REPOSITORY}")
    print(f"Username: {ARTIFACTORY_USERNAME}")

    tests_passed = 0
    tests_failed = 0

    # Test 1: Push
    if test_push():
        tests_passed += 1
    else:
        tests_failed += 1

    # Test 2: Pull
    if test_pull():
        tests_passed += 1
    else:
        tests_failed += 1

    # Test 3: Delete
    if test_delete():
        tests_passed += 1
    else:
        tests_failed += 1

    # Summary
    print("\n" + "=" * 60)
    print(f"Tests Passed: {tests_passed}")
    print(f"Tests Failed: {tests_failed}")
    print("=" * 60)

    # Exit with number of failed tests (0 = success)
    sys.exit(tests_failed)


if __name__ == "__main__":
    main()
