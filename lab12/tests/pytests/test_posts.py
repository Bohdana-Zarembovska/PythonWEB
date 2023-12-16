import pytest
from flask import url_for
from app import create_app, db
from app.auth.models import User
from app.posts.models import Post, PostCategory, Tag, EnumPriority
from datetime import date
import io


TEST_USERNAME = "username"
TEST_EMAIL = "username@gmail.com"
TEST_PASSWORD = "12345678"

TEST_POST_TITLE = "Random title"
TEST_POST_TEXT = "Random text"


def create_tag_cat(db):
    cat = PostCategory(id=23, name="cat")
    tag = Tag(id=23, name="tag")
    db.session.add(cat)
    db.session.add(tag)


@pytest.fixture
def app():
    """Fixture for app"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    return app


@pytest.fixture
def client(app):
    """Fixture for app client"""
    with app.test_client() as client:
        with app.app_context():
            db.create_all()

            create_tag_cat(db)

            yield client

            db.session.remove()
            db.drop_all()


@pytest.fixture
def login(client):
    """Fixture for login test user"""
    data = {'name': TEST_USERNAME,
            'email': TEST_EMAIL,
            'password': TEST_PASSWORD}

    test_user = User(**data)

    test_user.password = TEST_PASSWORD

    if User.query.filter_by(username=TEST_USERNAME).first() is None:
        db.session.add(test_user)

    client.post("/login",
                data=dict(
                    login=TEST_USERNAME,
                    password=TEST_PASSWORD,
                    remember='y'
                ))



@pytest.fixture
def post_id(client, login):
    response = client.post(
        "/posts/new",
        data=dict(
            title=TEST_POST_TITLE,
            text=TEST_POST_TEXT,
            category=1,
            tags=1
        )
    )
    assert response.status_code == 302  
    post = Post.query.filter_by(title=TEST_POST_TITLE).first()
    return post.id if post else None

@pytest.mark.usefixtures("login")
def test_main_page(client):
    """Test for posts page"""
    response = client.get("/posts", follow_redirects=True)
    assert response.status_code == 200
    assert b"Create post" in response.data

def test_create_post(client, login):
    """Test for creating post"""
    response = client.post(
        "/posts/new",
        data=dict(
            title=TEST_POST_TITLE,
            text=TEST_POST_TEXT,
            category=1,
            tags=1
        )
    )
    assert response.status_code == 302
    assert Post.query.filter_by(title=TEST_POST_TITLE).first() is not None
    assert Post.query.filter_by(text=TEST_POST_TEXT).first().title == TEST_POST_TITLE


def test_update_post(client, login, post_id):
    """Test for updating post"""

    response = client.post(
        f"/posts/update/{post_id}",
        data=dict(
            title=TEST_POST_TITLE,
            text=TEST_POST_TEXT + " New",
            category=1,
            tags=1
        )
    )
    assert response.status_code == 302
    assert Post.query.filter_by(title=TEST_POST_TITLE).first().text == TEST_POST_TEXT + " New"


def test_delete_post(client, login, post_id):
    response = client.post(f"/posts/delete/{post_id}")

    assert response.status_code == 302
    assert Post.query.filter_by(id=post_id).first() is None


def test_create_tag(client, login):
    res = client.post(
        "/posts/tags/new",
        data=dict(
            tag_name="test_tag"
        )
    )

    assert res.status_code == 302
    assert Tag.query.filter_by(name="test_tag").first() is not None


def test_create_cat(client, login):
    res = client.post(
        "/posts/categories/new",
        data=dict(
            cat_name="test_cat"
        )
    )

    assert res.status_code == 302
    assert PostCategory.query.filter_by(name="test_cat").first() is not None


def test_post_page(client, login, post_id):
    assert post_id is not None 

    res = client.get(f"/posts/{post_id}")

    data = res.get_data(as_text=True)

    assert res.status_code == 200
    assert TEST_POST_TITLE in data
    assert TEST_POST_TEXT in data
    assert "#newtag" in data
    assert "newcat" in data

def test_create_post_empty_text(client, login):
    response = client.post(
        "/posts/new",
        data=dict(
            title=TEST_POST_TITLE,
            text="",
            category=1,
            tags=1
        )
    )
    assert response.status_code == 200 
    assert b"Text is required" in response.data    

def test_failed_login(client):
    response = client.post("/login", data=dict(
        login="nonexistent_user",
        password="wrong_password",
        remember='y'
    ))
    assert response.status_code == 200 
    assert b"Invalid username or password" in response.data

def test_update_nonexistent_post(client, login):
    response = client.post(
        "/posts/update/999",
        data=dict(
            title=TEST_POST_TITLE,
            text=TEST_POST_TEXT + " New",
            category=1,
            tags=1
        )
    )
    assert response.status_code == 404

def test_delete_nonexistent_post(client, login):
    response = client.post("/posts/delete/999")
    assert response.status_code == 404

def test_create_post_no_category(client, login):
    response = client.post(
        "/posts/new",
        data=dict(
            title=TEST_POST_TITLE,
            text=TEST_POST_TEXT,
            category=None,
            tags=1
        )
    )
    assert response.status_code == 200 
    assert b"Category is required" in response.data    

def test_create_invalid_category(client, login):
    response = client.post("/posts/categories/new", data=dict(
        cat_name=""
    ))
    assert response.status_code == 200
    assert b"Invalid form!" in response.data

def test_delete_category(client, login):
    category = PostCategory(name="Test Category")
    db.session.add(category)
    db.session.commit()

    response = client.post(f"/posts/categories/delete/{category.id}")

    assert response.status_code == 302
    assert not PostCategory.query.get(category.id)
    assert b'Test Category' not in response.data
    assert b'Category (Test Category) deleted!' in response.data

def test_delete_tag(client, login):
    tag = Tag(name="Test Tag")
    db.session.add(tag)
    db.session.commit()

    response = client.post(f"/posts/tags/delete/{tag.id}")

    assert response.status_code == 302
    assert not Tag.query.get(tag.id)
    assert b'Test Tag' not in response.data
    assert b'Tag (#Test Tag) deleted!' in response.data

def test_delete_category_error(client, login):
    response = client.post("/posts/categories/delete/999")

    assert response.status_code == 302
    assert b'Error!' in response.data
    assert not PostCategory.query.get(999)

def test_delete_tag_error(client, login):
    response = client.post("/posts/tags/delete/999")

    assert response.status_code == 302
    assert b'Error!' in response.data
    assert not Tag.query.get(999)




