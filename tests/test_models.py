from models import User


def test_user_password_hashing_behaves_correctly():
    # Arrange
    user = User(username="testuser")
    password = "MySecurePassword123"

    # Act
    user.set_password(password)

    # Assert
    # Check that the password is not stored as plain text
    assert user.password_hash != password
    # Check that the correct password works
    assert user.check_password(password) is True
    # Check that the wrong password is rejected
    assert user.check_password("WrongPassword") is False