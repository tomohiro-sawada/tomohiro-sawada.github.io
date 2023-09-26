import os
import json

BLOG_INDEX_PATH = 'index.html'
POSTS_DIR_PATH = 'posts'

def extract_metadata(post_dir):
    """Extract metadata for a given post directory."""
    metadata_path = os.path.join(post_dir, 'metadata.json')
    with open(metadata_path, 'r') as f:
        return json.load(f)

def get_all_posts():
    """Get all posts from the posts directory."""
    return [dir_name for dir_name in os.listdir(POSTS_DIR_PATH) if os.path.isdir(os.path.join(POSTS_DIR_PATH, dir_name))]

def update_blog_index(posts_metadata):
    """Update the blog index page with the given posts metadata."""
    with open(BLOG_INDEX_PATH, 'r') as f:
        content = f.read()

    new_posts_html = ''
    for metadata in posts_metadata:
        new_posts_html += f"""
        <li>
            <div class="post">
                <span class="post-meta">{metadata['post created date']}</span>
                <div class="post-title">
                    <a class="post-link" href="/posts/{metadata['filename']}/index.html">{metadata['title']}</a>
                </div>
            </div>
        </li>
        """

    # Identify the section within <div class='blog'> to replace
    start_str = '<div class=\'blog\'>'
    end_str = '</ul>'
    start_index = content.find(start_str) + content[content.find(start_str):].find('<ul>') + len('<ul>')
    end_index = content.find(end_str, start_index)

    new_content = content[:start_index] + new_posts_html + content[end_index:]

    # Save the updated content
    with open(BLOG_INDEX_PATH, 'w') as f:
        f.write(new_content)

def main():
    all_posts = get_all_posts()
    posts_metadata = []
    for post in all_posts:
        post_dir = os.path.join(POSTS_DIR_PATH, post)
        metadata = extract_metadata(post_dir)
        metadata['filename'] = post  # adding the filename to the metadata for easier linking
        posts_metadata.append(metadata)

    # Sort posts by date before updating the index
    posts_metadata = sorted(posts_metadata, key=lambda x: x['post created date'], reverse=True)

    update_blog_index(posts_metadata)

if __name__ == "__main__":
    main()
