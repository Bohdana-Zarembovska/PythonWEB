from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from sqlalchemy import desc
from ..extensions import db
from ..util import save_picture
from .forms import PostForm, CategoryForm, TagForm, SearchForm
from .models import Post, EnumPriority, PostCategory, Tag
from . import posts_bp

 

@posts_bp.route('/', methods=["GET"])
@login_required
def posts_page():
    category_id = request.args.get('category', -1, type=int)
    page = request.args.get('page', 1, type=int)
    
    form=SearchForm()
    form.category.data = category_id

    pagination  = Post.query
    
    if category_id > 0:
        pagination  = pagination.filter(Post.category_id == category_id)
    
    pagination  = pagination.filter(db.or_(Post.enabled == True, Post.user_id == current_user.id)).order_by(desc(Post.created)).paginate(page = page, per_page = 2)


    return render_template("posts/posts.html", form=form, pagination=pagination)
 

@posts_bp.route('/<int:id>', methods=["GET"])
@login_required
def post_page(id):
    post = Post.query.get_or_404(id)
    user_id = post.user_id  # Access the user ID

    
    if not post.enabled and user_id != current_user.id:
        return redirect(url_for("posts.posts_page"))

    return render_template("posts/post.html", post=post, user_id=user_id)


@posts_bp.route("/new", methods=["GET", "POST"])
@login_required
def add_post():
    form = PostForm()

    if form.validate_on_submit():
        new_post = Post(
            title = form.title.data, 
            text = form.text.data,
            image = save_picture(form.image.data, f'{posts_bp.root_path}/static/posts_image') if form.image.data else None,
            type = EnumPriority(int(form.type.data)).name, 
            enabled = form.enabled.data,
            user_id = current_user.id,
            category_id = form.categories.data,
            tags = [tag for tag in Tag.query.filter(Tag.id.in_(form.tags.data)).all()]
        )
        try: 
            db.session.add(new_post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for("posts.post_page", id=new_post.id))
        except:
            db.session.rollback()
            flash('Error!', category='danger')
        
        return redirect(url_for("posts.add_post"))
    
    return render_template("posts/create_post.html", form=form)


@posts_bp.route("/update/<int:id>", methods=["GET", "POST"])
@login_required
def update_post(id):
    post = Post.query.get_or_404(id)

    # Check if the current user is the author of the post
    if current_user.id != post.user_id:
        return redirect(url_for("posts.posts_page", id=id))
    
    form = PostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.text = form.text.data         
        post.type = EnumPriority(int(form.type.data)).name
        post.enabled = form.enabled.data
        post.category_id = form.categories.data
        post.tags = [tag for tag in Tag.query.filter(Tag.id.in_(form.tags.data)).all()]
       
        if form.image.data:
            post.image = save_picture(form.image.data, f'{posts_bp.root_path}/static/posts_image')

        try: 
            db.session.commit()
            flash(f'Post ({post.title}) updated!', category='success')
            return redirect(url_for("posts.post_page", id=id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', category='danger')    
        
        return redirect(url_for("posts.update_post", id=id))
    
    form.type.data = str(post.type.value)
    form.enabled.data = post.enabled
    form.categories.data = post.category.id
    form.tags.data = [tag.id for tag in post.tags]

    return render_template("posts/update_post.html", form=form, post=post)
 

@posts_bp.route("/delete/<int:id>", methods=["GET", "POST"])
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)

    if current_user.id == post.user_id:
        try:
            db.session.delete(post)
            db.session.commit()
            flash(f'Пост ({post.title}) успішно видалено!', category='success')
        except Exception as e:
            db.session.rollback()
            flash(f'Помилка: {str(e)}', category='danger')

    return redirect(url_for("posts.posts_page"))



@posts_bp.route('/categories', methods=["GET"])
@login_required
def categories_page():
    return render_template("posts/categories.html", categories=PostCategory.query.all(), form=CategoryForm())

@posts_bp.route("/categories/new", methods=["POST"])
@login_required
def add_category():
    form=CategoryForm()
    
    if form.validate_on_submit():
        new_category = PostCategory(name = form.name.data)
        try:
            db.session.add(new_category)
            db.session.commit()
            flash(f'Category ({new_category.name}) created!', category='success')
        except:
            flash('Error!', category='danger')
            db.session.rollback()
    else:
        flash('Invalid form!', category='danger')

    return redirect(url_for('posts.categories_page'))

@posts_bp.route("/categories/delete/<int:id>", methods=["POST"])
@login_required
def delete_category(id):
    category = PostCategory.query.get_or_404(id)
    try:
        db.session.delete(category)
        db.session.commit()
        flash(f'Category ({category.name}) deleted!', category='success')
    except:
        flash('Error!', category='danger')
        db.session.rollback()
    return redirect(url_for("posts.categories_page"))




@posts_bp.route('/tags', methods=["GET"])
@login_required
def tags_page():
    return render_template("posts/tags.html", tags=Tag.query.all(), form=TagForm())

@posts_bp.route("/tags/new", methods=["POST"])
@login_required
def add_tag():
    form=TagForm()
    
    if form.validate_on_submit():
        new_tag = Tag(name = form.name.data)
        try:
            db.session.add(new_tag)
            db.session.commit()
            flash(f'Tag (#{new_tag.name}) created!', category='success')
        except:
            flash('Error!', category='danger')
            db.session.rollback()
    else:
        flash('Invalid form!', category='danger')

    return redirect(url_for('posts.tags_page'))

@posts_bp.route("/tags/delete/<int:id>", methods=["POST"])
@login_required
def delete_tag(id):
    tag = Tag.query.get_or_404(id)
    try:
        db.session.delete(tag)
        db.session.commit()
        flash(f'Tag (#{tag.name}) deleted!', category='success')
    except:
        flash('Error!', category='danger')
        db.session.rollback()
    return redirect(url_for("posts.tags_page"))